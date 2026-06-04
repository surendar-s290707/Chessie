# Chessie ♟️

Chessie is a chess analysis tool that examines a player's games and identifies behavioral patterns, playing habits, and improvement areas using PGN game data and engine analysis.

## Features

* Analyze PGN chess games
* Detect early queen development
* Detect delayed piece development
* Detect delayed castling
* Identify tactical and strategic trends
* Calculate custom player behavior metrics
* Generate player insights from game history
* Powered by Stockfish for deeper analysis

## Installation

### Prerequisites

* Python 3.10+
* Stockfish engine

### Clone the repository

```bash
git clone https://github.com/yourusername/chessie.git
cd chessie
```

### Install dependencies

```bash
pip install -r requirements.txt
```

## Project Structure

```text
chessie/
│
├── app.py                 # Main application
├── chessie.py             # Core analysis logic
├── stockfish_analysis.py  # Engine analysis
├── requirements.txt
├── data/
│   └── games.pgn
│
└── README.md
```

## Usage

### Run the application

```bash
python app.py
```

### Input

Provide a PGN file containing chess games.

### Output

Chessie generates:

* Development statistics
* Castling statistics
* Queen activity metrics
* Tactical indicators
* Player behavior summary

## Example Metrics

| Metric            | Description                             |
| ----------------- | --------------------------------------- |
| Early Queen Rate  | Frequency of moving the queen too early |
| Development Delay | Speed of minor piece development        |
| Castling Delay    | How quickly the king is secured         |
| Tactical Accuracy | Engine-based move quality               |

## Future Plans

* Web dashboard
* Chess.com integration
* Lichess integration
* Opening repertoire analysis
* Brilliant move detection
* Personalized training recommendations
* AI-generated player reports

## Technologies Used

* Python
* python-chess
* Stockfish
* Flask (if using web interface)

## Contributing

Pull requests and suggestions are welcome.

## License

MIT License

---

**Chessie's goal:** help players understand *how they play*, not just whether their moves were good or bad. ♟️📈
