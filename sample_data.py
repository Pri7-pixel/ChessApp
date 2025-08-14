"""
Sample data generator for the Chess Rating Calculator
Run this script to populate the app with example players and games
"""

import json
from datetime import datetime, timedelta
import random

def generate_sample_data():
    """Generate sample players and games for demonstration"""
    
    # Sample players
    players = {
        "Alice": {
            "rating": 1450,
            "games_played": 15,
            "wins": 10,
            "losses": 3,
            "draws": 2,
            "date_added": "2024-01-01"
        },
        "Bob": {
            "rating": 1320,
            "games_played": 12,
            "wins": 6,
            "losses": 4,
            "draws": 2,
            "date_added": "2024-01-02"
        },
        "Charlie": {
            "rating": 1580,
            "games_played": 20,
            "wins": 14,
            "losses": 4,
            "draws": 2,
            "date_added": "2024-01-03"
        },
        "Diana": {
            "rating": 1250,
            "games_played": 8,
            "wins": 3,
            "losses": 4,
            "draws": 1,
            "date_added": "2024-01-04"
        },
        "Eve": {
            "rating": 1400,
            "games_played": 18,
            "wins": 9,
            "losses": 7,
            "draws": 2,
            "date_added": "2024-01-05"
        }
    }
    
    # Sample games (these will be recalculated when the app runs)
    games = [
        {
            "player1": "Alice",
            "player2": "Bob",
            "result": "1-0",
            "date": "2024-01-15",
            "player1_old_rating": 1400,
            "player2_old_rating": 1300,
            "player1_new_rating": 1415,
            "player2_new_rating": 1285,
            "rating_change_1": 15,
            "rating_change_2": -15
        },
        {
            "player1": "Charlie",
            "player2": "Alice",
            "result": "1-0",
            "date": "2024-01-16",
            "player1_old_rating": 1550,
            "player2_old_rating": 1415,
            "player1_new_rating": 1558,
            "player2_new_rating": 1407,
            "rating_change_1": 8,
            "rating_change_2": -8
        },
        {
            "player1": "Bob",
            "player2": "Diana",
            "result": "1/2-1/2",
            "date": "2024-01-17",
            "player1_old_rating": 1285,
            "player2_old_rating": 1250,
            "player1_new_rating": 1289,
            "player2_old_rating": 1246,
            "rating_change_1": 4,
            "rating_change_2": -4
        },
        {
            "player1": "Eve",
            "player2": "Charlie",
            "result": "0-1",
            "date": "2024-01-18",
            "player1_old_rating": 1400,
            "player2_old_rating": 1558,
            "player1_new_rating": 1385,
            "player2_new_rating": 1573,
            "rating_change_1": -15,
            "rating_change_2": 15
        },
        {
            "player1": "Diana",
            "player2": "Eve",
            "result": "1-0",
            "date": "2024-01-19",
            "player1_old_rating": 1246,
            "player2_old_rating": 1385,
            "player1_new_rating": 1270,
            "player2_new_rating": 1361,
            "rating_change_1": 24,
            "rating_change_2": -24
        }
    ]
    
    # Save sample data
    with open('players.json', 'w') as f:
        json.dump(players, f, indent=2)
    
    with open('games.json', 'w') as f:
        json.dump(games, f, indent=2)
    
    print("Sample data generated successfully!")
    print(f"Created {len(players)} players and {len(games)} games")
    print("You can now run the app with: streamlit run chess_rating_calculator.py")

if __name__ == "__main__":
    generate_sample_data()
