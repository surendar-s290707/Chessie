import chess
import chess.pgn
import io

def build_position_tree(games):
    
    tree = {}

    for game in games:

        try:
            game_obj = chess.pgn.read_game(
                io.StringIO(game["pgn"])
            )

            if game_obj is None:
                continue

        except:
            continue

        board = game_obj.board()

        for move in game_obj.mainline_moves():

            # Position BEFORE move
            position = board.fen()

            # Move in SAN
            move_san = board.san(move)

            if position not in tree:
                tree[position] = {}

            if move_san not in tree[position]:

                tree[position][move_san] = {

                    "games": 0,
                    "wins": 0,
                    "losses": 0,
                    "draws": 0

                }

            tree[position][move_san]["games"] += 1

            board.push(move)
    print("Positions:", len(tree))
    return tree
