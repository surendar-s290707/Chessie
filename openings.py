import csv
import os
import re

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def normalize_move(move):
    return (
        move.replace("0-0-0", "O-O-O")  # Fix: Check queenside castling first
            .replace("0-0", "O-O")      # Then check kingside castling
            .replace("+", "")
            .replace("#", "")
            .replace("!", "")
            .replace("?", "")
            .lower()
    )

def clean_pgn_moves(pgn):
    # Removes move numbers like "1." "2."
    cleaned = re.sub(r"\d+\.", "", pgn)
    # Removes extra spaces
    cleaned = " ".join(cleaned.split())
    return cleaned.strip()

def load_openings():
    # Fix: Use a list to prevent identical move lines from overwriting each other
    opening_book = []

    files = ["a.tsv", "a_2.tsv", "b.tsv", "c.tsv", "d.tsv", "e.tsv"]

    for file in files:
        path = os.path.join(BASE_DIR, file)

        if not os.path.exists(path):
            continue

        with open(path, encoding="utf-8") as f:
            reader = csv.reader(f, delimiter="\t")
            
            # Skip the header row
            next(reader, None)

            for row in reader:
                if len(row) < 3:
                    continue

                eco = row[0]
                full_name = row[1].strip() 
                pgn_moves = row[2]

                cleaned_moves = clean_pgn_moves(pgn_moves)

                opening_book.append({
                    "moves": cleaned_moves,
                    "eco": eco,
                    "name": full_name
                })

    return opening_book

def find_opening(moves, opening_book):
    # Fix: Removed arbitrary [:30] ply limitation to allow deep variation matching
    game_moves = moves
    candidates = []

    for entry in opening_book:
        opening_list = entry["moves"].split()
        opening_length = len(opening_list)

        if opening_length == 0:
            continue

        depth = 0
        for gm, om in zip(game_moves, opening_list):
            if normalize_move(gm) == normalize_move(om):
                depth += 1
            else:
                break

        if depth == 0:
            continue

        # Calculate exactly how much of the book line was matched
        match_percentage = (depth / opening_length) * 100.0

        candidates.append({
            "eco": entry["eco"],
            "name": entry["name"], 
            "match_depth": depth,
            "opening_length": opening_length,
            "match_percentage": match_percentage
        })

    if not candidates:
        return None

    # Sorts by:
    # 1. Match Depth (higher is better)
    # 2. Match Percentage (higher is better, naturally breaking length ties)
    candidates.sort(
        key=lambda x: (
            x["match_depth"], 
            x["match_percentage"]
        ),
        reverse=True
    )

    best_match = candidates[0]

    return {
        "eco": best_match["eco"],
        "name": best_match["name"],
        "match_depth": best_match["match_depth"],
        "match_percentage": round(best_match["match_percentage"], 1)
    }