# ♟ Chessie

> **Chess Improvement Engine**

Chessie is an AI-powered chess analysis platform focused on helping players improve through **personalized insights**, **opening analytics**, and an upcoming **interactive analysis studio**.

Unlike traditional chess analysis tools that only evaluate moves, Chessie aims to understand **how you play**, identify recurring patterns, and recommend improvements based on your own games.

---

# 🚀 Current Features

## 📊 Opening Analysis

- Opening distribution
- Opening win/draw/loss percentages
- Opening grouping (e.g. Sicilian → Najdorf)
- Variation statistics
- Most played openings
- Opening success rates

---

## 🎯 Player Metrics

- Early Queen Development Rate
- Development Delay Rate
- Castling Delay Rate
- Early Loss Rate
- Average Game Length

---

## 🎮 Game Filters

Analyze games by

- Time Control
    - Bullet
    - Blitz
    - Rapid
    - Daily
    - All

- Rated Status
    - Rated
    - Unrated
    - All

- Played As
    - White
    - Black
    - All

- Number of Games

---

## 📈 Interactive Charts

- Opening Distribution
- Win / Draw / Loss Graphs
- Opening Performance Comparison

---

## 🔗 Shareable Reports

Generate report links that can be shared with other players.

---

# 🛠 Current Architecture

```
Chess.com API
        │
        ▼
get_games()
        │
        ├──────────────┐
        ▼              ▼
Opening Analysis   Position Tree
        │              │
        ▼              ▼
 Report Page     Analysis Studio
```

---

# 🚧 Currently Under Development

## ♟ Analysis Studio

An interactive chess workspace inspired by professional chess software.

Planned layout:

```
Explorer │ Chess Board │ Position Statistics

────────────────────────────────────────

Games Reaching Current Position
```

Features:

- Interactive Board
- Personal Opening Explorer
- Position Statistics
- Engine Evaluation
- Best Move
- ACPL
- Example Games
- Opening Tree

---

## 🌳 Position Tree

A custom database built from your own games.

Instead of showing what Masters play, Chessie will show:

- Your most common moves
- Your win rate
- Your average ACPL
- Your preferred continuations
- Your example games

---

# 🔬 Planned Features

## Analysis

- Average Centipawn Loss (ACPL)
- Blunder Density
- Tactical Miss Detection
- Fork Detection
- Pin Detection
- Skewer Detection
- Hanging Piece Detection
- Open File Detection
- Candidate Move Analysis
- Move Classification
- Brilliant Move Finder

---

## Machine Learning

Future ML-powered features include

- Playing Style Classification
- Weakness Prediction
- Personalized Training Recommendations
- Rating Prediction
- Opening Recommendation Engine
- Opponent Style Matching
- Automatic Game Clustering

---

## Personal Opening Explorer

Build your own opening database.

Example:

```
After e4

e5      37 games
Win Rate: 62%

d6      20 games
Win Rate: 49%

c5       3 games
Win Rate: 67%
```

Navigate your entire repertoire using an interactive board.

---

# 🏗 Tech Stack

Backend

- Python
- Flask

Libraries

- python-chess
- Requests
- Chart.js

Data Source

- Chess.com Public API

---

# Vision

Chessie is being built as a personal chess improvement platform—not just another analysis website.

The goal is to combine:

- Report Generation
- Interactive Analysis
- Personal Opening Explorer
- Engine Analysis
- Machine Learning
- Training Tools

into one seamless experience.

---

# Roadmap

## ✅ Phase 1

- Opening Analysis
- Player Metrics
- Filtering
- Charts
- Shareable Reports

## 🚧 Phase 2

- Analysis Studio
- Position Tree
- Interactive Board
- Opening Explorer

## 🔜 Phase 3

- Stockfish Integration
- ACPL
- Move Classification
- Brilliant Move Detection

## 🔮 Phase 4

- Machine Learning
- Personalized Coaching
- Training System
- Opening Recommendation Engine

---

# Author

**Surya Surendar**

Building Chessie one move at a time.
