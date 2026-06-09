import requests
import io
import chess.pgn

from openings import load_openings, find_opening

# -----------------------------------
# LOAD OPENING DATABASE ONCE
# -----------------------------------

OPENING_BOOK = load_openings()

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

# -----------------------------------
# BEHAVIOR SIGNALS
# -----------------------------------

def early_queen(moves, limit=6):
    for move in moves[:limit]:
        if move.startswith("Q"):
            return True
    return False


def development_delay(moves):
    developed = 0

    for move in moves[:8]:

        if move.startswith("N") or move.startswith("B"):
            developed += 1

    return developed < 2


def castling_delay(moves):
    for move in moves[:10]:

        if move == "O-O" or move == "O-O-O":
            return False

    return True


# -----------------------------------
# MAIN ANALYZER
# -----------------------------------

def analyze_openings(username,num_games=50,time_class="all"):
    
    archives_url = f"https://api.chess.com/pub/player/{username}/games/archives"

    response = requests.get(archives_url, headers=HEADERS)

    if response.status_code != 200:
        return {
            "error": "Failed to fetch archives"
        }

    archives = response.json().get("archives", [])

    if not archives:
        return {
            "error": "No games found"
        }

    # -----------------------------------
    # ONLY LAST MONTH
    # -----------------------------------

    games = []

    for archive_url in reversed(archives):

        response = requests.get(
            archive_url,
            headers=HEADERS
        )

        if response.status_code != 200:
            continue

        monthly_games = response.json().get(
            "games",
            []
        )

        for game in monthly_games:
            

            # FORMAT FILTER
            if time_class != "all":

                if game.get("time_class") != time_class:
                    continue

            # RULES FILTER
            if game.get("rules") != "chess":
                continue

            # PGN FILTER
            if "pgn" not in game:
                continue

            games.append(game)

            if len(games) >= num_games:
                break

        if len(games) >= num_games:
            break
    # -----------------------------------
    # STATS
    # -----------------------------------

    opening_stats = {}
    opening_results = {}
    grouped_openings={}
    total_games = 0
    total_moves = 0

    early_queen_games = 0
    development_delay_games = 0
    castling_delay_games = 0
    early_losses = 0

    # -----------------------------------
    # PROCESS GAMES
    # -----------------------------------
    username_lower = username.lower()
    for game in games:
        is_white = game["white"]["username"].lower() == username_lower

# SAN moves are interleaved: white, black, white, black...
        
        # if time_class != "all":
        #     pass

        #     if game.get("time_class") != time_class:
        #         continue
        # # if not game.get("rated"):
        # #     continue

        # # if game.get("time_class") != "rapid":
        # #     continue

        # if game.get("rules") != "chess":
        #     continue

        # if "pgn" not in game:
        #     continue

        pgn = game["pgn"]

        try:

            game_obj = chess.pgn.read_game(
                io.StringIO(game["pgn"])
            )

            if game_obj is None:
                continue

        except:
            continue

        if game_obj is None:
            continue

        board = game_obj.board()

        moves = []

        for move in game_obj.mainline_moves():
            

            try:

                san = board.san(move)

            except:
                continue
            moves.append(san)
            board.push(move)
        player_moves = moves[::2] if is_white else moves[1::2]

        opening_summary = {}
        for opening, stats in opening_results.items():

            total = (
                stats["win"]
                + stats["loss"]
                + stats["draw"]
            )

            if total == 0:
                continue

            opening_summary[opening] = {

                "win_pct": round(
                    stats["win"] * 100 / total,
                    1
                ),

                "draw_pct": round(
                    stats["draw"] * 100 / total,
                    1
                ),

                "loss_pct": round(
                    stats["loss"] * 100 / total,
                    1
                ),

                "games": total
            }
        # -----------------------------------
        # GAME LENGTH
        # -----------------------------------

        game_length = len(moves)

        total_games += 1
        total_moves += game_length

        # -----------------------------------
        # OPENING DETECTION
        # -----------------------------------

        opening_data = find_opening(moves, OPENING_BOOK)

        if opening_data:
            opening_name = opening_data["name"]
        else:
            opening_name = "Unknown"
        
        # -------------------------
        # Parent Opening + Variation
        # -------------------------
       
        if ":" in opening_name:

            parent_opening = opening_name.split(":")[0].strip()

            variation = opening_name.split(":", 1)[1].strip()

        else:

            parent_opening = opening_name

            variation = "Main Line"
        
        opening_stats[opening_name] = (opening_stats.get(opening_name, 0) + 1)

        # -------------------------
        # Create opening bucket
        # -------------------------

        if parent_opening not in grouped_openings:

            grouped_openings[parent_opening] = {

                "games": 0,
                "win": 0,
                "draw": 0,
                "loss": 0,

                "variations": {}
            }


        grouped_openings[parent_opening]["games"] += 1


        # -------------------------
        # Create variation bucket
        # -------------------------

        if variation not in grouped_openings[parent_opening]["variations"]:

            grouped_openings[parent_opening]["variations"][variation] = {

                "games": 0,
                "win": 0,
                "draw": 0,
                "loss": 0
            }


        grouped_openings[parent_opening]["variations"][variation]["games"] += 1

        opening_stats[opening_name] = opening_stats.get(opening_name, 0) + 1
        if opening_name not in opening_results:

            opening_results[opening_name] = {
                "win": 0,
                "loss": 0,
                "draw": 0
            }

        

        if is_white:

            result = game["white"]["result"]

        else:

            result = game["black"]["result"]


        if result == "win":

            opening_results[opening_name]["win"] += 1

            grouped_openings[parent_opening]["win"] += 1

            grouped_openings[parent_opening]["variations"][variation]["win"] += 1

        elif result in [
            "agreed",
            "repetition",
            "stalemate",
            "timevsinsufficient",
            "insufficient",
            "50move"
        ]:

            opening_results[opening_name]["draw"] += 1

            grouped_openings[parent_opening]["draw"] += 1

            grouped_openings[parent_opening]["variations"][variation]["draw"] += 1

        else:

            opening_results[opening_name]["loss"] += 1

            grouped_openings[parent_opening]["loss"] += 1

            grouped_openings[parent_opening]["variations"][variation]["loss"] += 1
                
        
        # return {
        #     "opening_stats": opening_stats,
        #     "opening_results": opening_results,
        #     ...
        # }
    

        # for opening, data in opening_results.items():

        #     total = (
        #         data["win"]
        #         + data["loss"]
        #         + data["draw"]
        #     )

        # winrate = (
        #     data["win"] / total * 100
        #     if total > 0
        #     else 0
        # )
        # -----------------------------------
        # EARLY QUEEN
        # -----------------------------------

        if early_queen(player_moves):
            early_queen_games += 1

        # -----------------------------------
        # DEVELOPMENT DELAY
        # -----------------------------------

        if development_delay(player_moves):
            development_delay_games += 1

        # -----------------------------------
        # CASTLING DELAY
        # -----------------------------------

        if castling_delay(player_moves):
            castling_delay_games += 1

        # -----------------------------------
        # EARLY LOSS DETECTION
        # -----------------------------------
        full_moves = len(moves) / 2

        username_lower = username.lower()

        if game["white"]["username"].lower() == username_lower:

            if game["white"]["result"] == "lose":

                if full_moves < 15:
                    early_losses += 1

        elif game["black"]["username"].lower() == username_lower:

            if game["black"]["result"] == "lose":

                if full_moves < 15:
                    early_losses += 1

    # -----------------------------------
    # FINAL METRICS
    # -----------------------------------

    if total_games == 0:
        return {
            "error": "No valid games found"
        }

    early_queen_rate = round(early_queen_games / total_games, 2)

    development_delay_rate = round(
        development_delay_games / total_games, 2
    )

    castling_delay_rate = round(
        castling_delay_games / total_games, 2
    )

    early_loss_rate = round(
        early_losses / total_games, 2
    )

    avg_game_length = round(
        total_moves / total_games, 1
    )

    for opening, data in grouped_openings.items():

        total = data["games"]

        data["win_pct"] = round(
            data["win"] * 100 / total,
            1
        )

        data["draw_pct"] = round(
            data["draw"] * 100 / total,
            1
        )

        data["loss_pct"] = round(
            data["loss"] * 100 / total,
            1
        )

        for variation, vdata in data["variations"].items():

            vtotal = vdata["games"]

            vdata["win_pct"] = round(
                vdata["win"] * 100 / vtotal,
                1
            )

            vdata["draw_pct"] = round(
                vdata["draw"] * 100 / vtotal,
                1
            )

            vdata["loss_pct"] = round(
                vdata["loss"] * 100 / vtotal,
                1
            )

    # -----------------------------------
    # RETURN EVERYTHING
    # -----------------------------------

    return {

        "opening_stats": opening_stats,

        "opening_results": opening_results,

        "grouped_openings": grouped_openings,

        "early_queen_rate": early_queen_rate,

        "opening_summary": opening_summary,

        "development_delay_rate": development_delay_rate,

        "castling_delay_rate": castling_delay_rate,

        "games_analyzed": total_games,

        "early_loss_rate": early_loss_rate,

        "avg_game_length": avg_game_length
        
    }


# -----------------------------------
# TEST RUN
# -----------------------------------

if __name__ == "__main__":

    username = input("Enter Chess.com username: ")

    result = analyze_openings(username)

    print("\n===== PLAYER REPORT =====\n")

    if "error" in result:
        print(result["error"])

    else:

        print("OPENINGS:\n")

        for opening, count in sorted(
            result["opening_stats"].items(),
            key=lambda x: x[1],
            reverse=True
        ):

            summary = result["opening_summary"].get(opening)

            if summary:

                print(
                    f"{opening} "
                    f"W:{summary['win_pct']}% "
                    f"D:{summary['draw_pct']}% "
                    f"L:{summary['loss_pct']}% "
                    f"({summary['games']} games)"
                )

            else:

                print(opening)

        print("\n===== BEHAVIOR =====\n")

        print("Early Queen Rate:", result["early_queen_rate"])

        print("Development Delay Rate:",
              result["development_delay_rate"])

        print("Castling Delay Rate:",
              result["castling_delay_rate"])

        print("Early Loss Rate:",
              result["early_loss_rate"])

        print("Avserage Game Length:",
              result["avg_game_length"])