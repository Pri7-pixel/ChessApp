import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import json
import os

# Page configuration
st.set_page_config(
    page_title="Chess Rating Calculator",
    page_icon="♟️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .player-card {
        background-color: #ffffff;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #e0e0e0;
        margin: 0.5rem 0;
    }
    .game-result {
        padding: 0.5rem;
        border-radius: 0.25rem;
        margin: 0.25rem 0;
    }
    .win { background-color: #d4edda; color: #155724; }
    .loss { background-color: #f8d7da; color: #721c24; }
    .draw { background-color: #fff3cd; color: #856404; }
</style>
""", unsafe_allow_html=True)

class ChessRatingCalculator:
    def __init__(self):
        self.k_factor = 32  # K-factor for rating calculations
        self.initial_rating = 1200  # Starting rating for new players
        
    def calculate_expected_score(self, rating_a, rating_b):
        """Calculate expected score for player A against player B"""
        return 1 / (1 + 10 ** ((rating_b - rating_a) / 400))
    
    def calculate_new_rating(self, current_rating, expected_score, actual_score, k_factor=None):
        """Calculate new rating based on game result"""
        if k_factor is None:
            k_factor = self.k_factor
        return current_rating + k_factor * (actual_score - expected_score)
    
    def calculate_rating_change(self, current_rating, expected_score, actual_score, k_factor=None):
        """Calculate rating change for a game"""
        if k_factor is None:
            k_factor = self.k_factor
        return k_factor * (actual_score - expected_score)

def load_data():
    """Load existing data from JSON files"""
    players = {}
    games = []
    
    if os.path.exists('players.json'):
        with open('players.json', 'r') as f:
            players = json.load(f)
    
    if os.path.exists('games.json'):
        with open('games.json', 'r') as f:
            games = json.load(f)
    
    return players, games

def save_data(players, games):
    """Save data to JSON files"""
    with open('players.json', 'w') as f:
        json.dump(players, f, indent=2)
    
    with open('games.json', 'w') as f:
        json.dump(games, f, indent=2)

def main():
    # Initialize calculator
    calculator = ChessRatingCalculator()
    
    # Load existing data
    players, games = load_data()
    
    # Main header
    st.markdown('<h1 class="main-header">♟️ Chess Rating Calculator</h1>', unsafe_allow_html=True)
    
    # Sidebar for navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox(
        "Choose a page:",
        ["Dashboard", "Add Player", "Record Game", "View Players", "Game History", "Statistics"]
    )
    
    if page == "Dashboard":
        show_dashboard(players, games, calculator)
    elif page == "Add Player":
        add_player_page(players)
    elif page == "Record Game":
        record_game_page(players, games, calculator)
    elif page == "View Players":
        view_players_page(players, games)
    elif page == "Game History":
        game_history_page(games, players)
    elif page == "Statistics":
        statistics_page(players, games, calculator)

def show_dashboard(players, games, calculator):
    """Display the main dashboard"""
    st.header("📊 Dashboard")
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Players", len(players))
    
    with col2:
        st.metric("Total Games", len(games))
    
    with col3:
        if players:
            avg_rating = np.mean([player['rating'] for player in players.values()])
            st.metric("Average Rating", f"{avg_rating:.0f}")
        else:
            st.metric("Average Rating", "N/A")
    
    with col4:
        if games:
            recent_games = [g for g in games if g.get('date')]
            if recent_games:
                latest_date = max(g['date'] for g in recent_games)
                st.metric("Latest Game", latest_date)
            else:
                st.metric("Latest Game", "N/A")
        else:
            st.metric("Latest Game", "N/A")
    
    # Top players
    if players:
        st.subheader("🏆 Top Players")
        sorted_players = sorted(players.items(), key=lambda x: x[1]['rating'], reverse=True)
        
        cols = st.columns(3)
        for i, (player_name, player_data) in enumerate(sorted_players[:6]):
            with cols[i % 3]:
                st.markdown(f"""
                <div class="player-card">
                    <h4>{player_name}</h4>
                    <p><strong>Rating:</strong> {player_data['rating']:.0f}</p>
                    <p><strong>Games:</strong> {player_data.get('games_played', 0)}</p>
                </div>
                """, unsafe_allow_html=True)
    
    # Recent games
    if games:
        st.subheader("📝 Recent Games")
        recent_games = sorted(games, key=lambda x: x.get('date', ''), reverse=True)[:5]
        
        for game in recent_games:
            player1 = game['player1']
            player2 = game['player2']
            result = game['result']
            
            if result == '1-0':
                result_text = f"{player1} defeated {player2}"
                result_class = "win"
            elif result == '0-1':
                result_text = f"{player2} defeated {player1}"
                result_class = "loss"
            else:
                result_text = f"{player1} drew with {player2}"
                result_class = "draw"
            
            st.markdown(f"""
            <div class="game-result {result_class}">
                <strong>{result_text}</strong> - {game.get('date', 'No date')}
            </div>
            """, unsafe_allow_html=True)

def add_player_page(players):
    """Page for adding new players"""
    st.header("👤 Add New Player")
    
    with st.form("add_player_form"):
        player_name = st.text_input("Player Name", placeholder="Enter player name")
        initial_rating = st.number_input("Initial Rating", value=1200, min_value=0, max_value=3000)
        
        submitted = st.form_submit_button("Add Player")
        
        if submitted and player_name:
            if player_name in players:
                st.error("Player already exists!")
            else:
                players[player_name] = {
                    'rating': initial_rating,
                    'games_played': 0,
                    'wins': 0,
                    'losses': 0,
                    'draws': 0,
                    'date_added': datetime.now().strftime("%Y-%m-%d")
                }
                save_data(players, [])  # Empty games list for now
                st.success(f"Player '{player_name}' added successfully!")
                st.rerun()

def record_game_page(players, games, calculator):
    """Page for recording game results"""
    st.header("🎮 Record Game")
    
    if len(players) < 2:
        st.warning("You need at least 2 players to record a game. Please add players first.")
        return
    
    with st.form("record_game_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            player1 = st.selectbox("Player 1", list(players.keys()))
            player1_rating = players[player1]['rating']
            st.info(f"Current rating: {player1_rating:.0f}")
        
        with col2:
            player2 = st.selectbox("Player 2", [p for p in players.keys() if p != player1])
            player2_rating = players[player2]['rating']
            st.info(f"Current rating: {player2_rating:.0f}")
        
        result = st.selectbox("Game Result", ["1-0", "0-1", "1/2-1/2"])
        game_date = st.date_input("Game Date", value=datetime.now().date())
        
        submitted = st.form_submit_button("Record Game")
        
        if submitted:
            # Calculate expected scores
            expected_score_1 = calculator.calculate_expected_score(player1_rating, player2_rating)
            expected_score_2 = calculator.calculate_expected_score(player2_rating, player1_rating)
            
            # Determine actual scores
            if result == "1-0":
                actual_score_1 = 1.0
                actual_score_2 = 0.0
            elif result == "0-1":
                actual_score_1 = 0.0
                actual_score_2 = 1.0
            else:  # Draw
                actual_score_1 = 0.5
                actual_score_2 = 0.5
            
            # Calculate new ratings
            new_rating_1 = calculator.calculate_new_rating(player1_rating, expected_score_1, actual_score_1)
            new_rating_2 = calculator.calculate_new_rating(player2_rating, expected_score_2, actual_score_2)
            
            # Update player statistics
            players[player1]['rating'] = new_rating_1
            players[player2]['rating'] = new_rating_2
            players[player1]['games_played'] += 1
            players[player2]['games_played'] += 1
            
            if result == "1-0":
                players[player1]['wins'] += 1
                players[player2]['losses'] += 1
            elif result == "0-1":
                players[player1]['losses'] += 1
                players[player2]['wins'] += 1
            else:
                players[player1]['draws'] += 1
                players[player2]['draws'] += 1
            
            # Record the game
            game_record = {
                'player1': player1,
                'player2': player2,
                'result': result,
                'date': game_date.strftime("%Y-%m-%d"),
                'player1_old_rating': player1_rating,
                'player2_old_rating': player2_rating,
                'player1_new_rating': new_rating_1,
                'player2_new_rating': new_rating_2,
                'rating_change_1': new_rating_1 - player1_rating,
                'rating_change_2': new_rating_2 - player2_rating
            }
            
            games.append(game_record)
            save_data(players, games)
            
            # Display results
            st.success("Game recorded successfully!")
            
            col1, col2 = st.columns(2)
            with col1:
                st.subheader(f"{player1}")
                st.metric("Rating Change", f"{new_rating_1 - player1_rating:+.0f}")
                st.metric("New Rating", f"{new_rating_1:.0f}")
            
            with col2:
                st.subheader(f"{player2}")
                st.metric("Rating Change", f"{new_rating_2 - player2_rating:+.0f}")
                st.metric("New Rating", f"{new_rating_2:.0f}")

def view_players_page(players, games):
    """Page for viewing all players"""
    st.header("👥 All Players")
    
    if not players:
        st.info("No players added yet. Add some players to get started!")
        return
    
    # Create DataFrame for better display
    player_data = []
    for name, data in players.items():
        player_data.append({
            'Name': name,
            'Rating': data['rating'],
            'Games Played': data.get('games_played', 0),
            'Wins': data.get('wins', 0),
            'Losses': data.get('losses', 0),
            'Draws': data.get('draws', 0),
            'Win Rate': f"{data.get('wins', 0) / max(data.get('games_played', 1), 1) * 100:.1f}%"
        })
    
    df = pd.DataFrame(player_data)
    df = df.sort_values('Rating', ascending=False)
    
    st.dataframe(df, use_container_width=True)
    
    # Rating distribution chart
    if len(players) > 1:
        st.subheader("📈 Rating Distribution")
        fig = px.histogram(df, x='Rating', nbins=10, title="Player Rating Distribution")
        st.plotly_chart(fig, use_container_width=True)

def game_history_page(games, players):
    """Page for viewing game history"""
    st.header("📚 Game History")
    
    if not games:
        st.info("No games recorded yet. Record some games to see the history!")
        return
    
    # Create DataFrame for better display
    game_data = []
    for game in games:
        game_data.append({
            'Date': game.get('date', 'Unknown'),
            'Player 1': game['player1'],
            'Player 2': game['player2'],
            'Result': game['result'],
            'Rating Change 1': f"{game.get('rating_change_1', 0):+.0f}",
            'Rating Change 2': f"{game.get('rating_change_2', 0):+.0f}"
        })
    
    df = pd.DataFrame(game_data)
    df = df.sort_values('Date', ascending=False)
    
    st.dataframe(df, use_container_width=True)
    
    # Game results chart
    st.subheader("📊 Game Results Distribution")
    result_counts = df['Result'].value_counts()
    fig = px.pie(values=result_counts.values, names=result_counts.index, title="Game Results")
    st.plotly_chart(fig, use_container_width=True)

def statistics_page(players, games, calculator):
    """Page for detailed statistics"""
    st.header("📊 Statistics")
    
    if not players:
        st.info("No data available. Add players and record games to see statistics!")
        return
    
    # Player statistics
    st.subheader("👥 Player Statistics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Highest rated player
        if players:
            highest_rated = max(players.items(), key=lambda x: x[1]['rating'])
            st.metric("Highest Rated Player", f"{highest_rated[0]} ({highest_rated[1]['rating']:.0f})")
        
        # Most active player
        if players:
            most_active = max(players.items(), key=lambda x: x[1].get('games_played', 0))
            st.metric("Most Active Player", f"{most_active[0]} ({most_active[1].get('games_played', 0)} games)")
    
    with col2:
        # Average rating
        if players:
            avg_rating = np.mean([p['rating'] for p in players.values()])
            st.metric("Average Rating", f"{avg_rating:.0f}")
        
        # Total games played
        if players:
            total_games = sum(p.get('games_played', 0) for p in players.values())
            st.metric("Total Games", total_games)
    
    # Rating progression chart
    if games:
        st.subheader("📈 Rating Progression")
        
        # Create rating history for each player
        rating_history = {}
        for game in sorted(games, key=lambda x: x.get('date', '')):
            date = game.get('date', 'Unknown')
            
            # Update player 1 history
            if game['player1'] not in rating_history:
                rating_history[game['player1']] = []
            rating_history[game['player1']].append({
                'date': date,
                'rating': game['player1_new_rating']
            })
            
            # Update player 2 history
            if game['player2'] not in rating_history:
                rating_history[game['player2']] = []
            rating_history[game['player2']].append({
                'date': date,
                'rating': game['player2_new_rating']
            })
        
        # Create plot
        fig = go.Figure()
        
        for player, history in rating_history.items():
            if history:
                dates = [h['date'] for h in history]
                ratings = [h['rating'] for h in history]
                fig.add_trace(go.Scatter(x=dates, y=ratings, mode='lines+markers', name=player))
        
        fig.update_layout(
            title="Rating Progression Over Time",
            xaxis_title="Date",
            yaxis_title="Rating",
            hovermode='x unified'
        )
        
        st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    main()
