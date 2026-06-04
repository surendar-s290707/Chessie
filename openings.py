import csv
import os
import re

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def normalize_move(move):
    return (
        move.replace("+", "")
            .replace("#", "")
            .replace("!", "")
            .replace("?", "")
            .replace("0-0", "O-O")
            .lower()
    )

def clean_pgn_moves(pgn):
    # Removes move numbers like "1." "2."
    cleaned = re.sub(r"\d+\.", "", pgn)
    # Removes extra spaces
    cleaned = " ".join(cleaned.split())
    return cleaned.strip()

def load_openings():
    opening_book = {}

    # Included all files including a_2.tsv as requested
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
                # THE FIX: We keep the raw string exactly as it is in the database.
                # The simplify_opening_name function has been entirely deleted.
                full_name = row[1].strip() 
                pgn_moves = row[2]

                cleaned_moves = clean_pgn_moves(pgn_moves)

                opening_book[cleaned_moves] = {
                    "eco": eco,
                    "name": full_name  # Stores exact variation name
                }

    return opening_book

def find_opening(moves, opening_book):
    # Increased depth to 30 to catch extremely deep variation lines
    game_moves = moves[:30]
    candidates = []

    for opening_moves, data in opening_book.items():
        opening_list = opening_moves.split()
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
            "eco": data["eco"],
            "name": data["name"], 
            "match_depth": depth,
            "opening_length": opening_length,
            "match_percentage": match_percentage
        })

    if not candidates:
        return None

    # THE CORE ALGORITHM:
    # 1. Match Depth: Always prioritize the line that matches the most actual moves in the game.
    # 2. Match Percentage: If two variations match the same number of moves, 
    #    pick the one where the book line perfectly ends at that move (100%).
    # 3. Opening Length: Shortest line wins absolute ties to prevent false positive branching.
    candidates.sort(
        key=lambda x: (
            x["match_depth"], 
            x["match_percentage"], 
            -x["opening_length"]
        ),
        reverse=True
    )

    best_match = candidates[0]

    return {
        "eco": best_match["eco"],
        "name": best_match["name"], # Returns the exact variation to chessie.py
        "match_depth": best_match["match_depth"],
        "match_percentage": round(best_match["match_percentage"], 1)
    }