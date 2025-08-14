# ♟️ Chess Rating Calculator

A comprehensive Streamlit application for calculating and tracking chess ratings for offline games using the Elo rating system.

## Features

- **Player Management**: Add and manage chess players with customizable initial ratings
- **Game Recording**: Record game results and automatically calculate rating changes
- **Elo Rating System**: Implements the standard Elo rating formula with K-factor of 32
- **Dashboard**: Overview of key metrics, top players, and recent games
- **Statistics**: Detailed analytics including rating progression charts
- **Game History**: Complete history of all recorded games
- **Data Persistence**: All data is saved locally in JSON format

## Installation

1. **Clone or download the project files**

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   streamlit run chess_rating_calculator.py
   ```

4. **Open your browser** and navigate to the URL shown in the terminal (usually `http://localhost:8501`)

## How to Use

### 1. Getting Started
- The app will open to the Dashboard page
- Start by adding players using the "Add Player" page in the sidebar

### 2. Adding Players
- Navigate to "Add Player" in the sidebar
- Enter player name and initial rating (default: 1200)
- Click "Add Player" to save

### 3. Recording Games
- Go to "Record Game" in the sidebar
- Select two players from the dropdown menus
- Choose the game result (1-0, 0-1, or 1/2-1/2 for draw)
- Set the game date
- Click "Record Game" to calculate and save rating changes

### 4. Viewing Data
- **Dashboard**: Overview of all players and recent activity
- **View Players**: Complete list of all players with statistics
- **Game History**: Chronological list of all recorded games
- **Statistics**: Detailed analytics and rating progression charts

## Elo Rating System

The app uses the standard Elo rating system:

- **Expected Score**: `E = 1 / (1 + 10^((Rb - Ra) / 400))`
- **New Rating**: `R' = R + K * (S - E)`

Where:
- `R` = Current rating
- `E` = Expected score (0-1)
- `S` = Actual score (1 for win, 0.5 for draw, 0 for loss)
- `K` = K-factor (set to 32 for this application)

## Data Storage

The application stores data in two JSON files:
- `players.json`: Player information and current ratings
- `games.json`: Complete game history

These files are automatically created when you first add players or record games.

## Features in Detail

### Dashboard
- Total players and games count
- Average rating across all players
- Latest game date
- Top 6 players by rating
- Recent game results with color coding

### Player Management
- Add new players with custom initial ratings
- Track wins, losses, draws, and total games
- Calculate win percentages
- View rating distribution charts

### Game Recording
- Automatic rating calculations
- Real-time display of rating changes
- Support for wins, losses, and draws
- Date tracking for all games

### Statistics
- Rating progression over time
- Player performance metrics
- Game results distribution
- Interactive charts using Plotly

## Customization

You can modify the following parameters in the `ChessRatingCalculator` class:
- `k_factor`: Controls how much ratings change per game (default: 32)
- `initial_rating`: Starting rating for new players (default: 1200)

## Requirements

- Python 3.7+
- Streamlit 1.28.1
- Pandas 2.1.3
- NumPy 1.24.3
- Plotly 5.17.0

## Troubleshooting

1. **Port already in use**: If port 8501 is busy, Streamlit will automatically use the next available port
2. **Data not saving**: Ensure the application has write permissions in the directory
3. **Charts not displaying**: Check that all dependencies are properly installed

## Future Enhancements

Potential improvements for future versions:
- Tournament support
- Multiple rating systems (Glicko, TrueSkill)
- Export functionality (CSV, Excel)
- Player photos and profiles
- Game notation support
- Advanced analytics and predictions

## License

This project is open source and available under the MIT License.

---

**Enjoy tracking your chess ratings! ♟️**
