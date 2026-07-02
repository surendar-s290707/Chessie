import chess
import chess.pgn
import io
from collections import Counter

def get_next_moves(games, moves):

    next_moves = Counter()

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

        game_moves = list(game_obj.mainline_moves())

        san_moves = []

        for move in game_moves:

            san = board.san(move)

            san_moves.append(san)

            board.push(move)

        if san_moves[:len(moves)] != moves:

            continue


        if len(san_moves) > len(moves):

            next_move = san_moves[len(moves)]

            next_moves[next_move] += 1

    return next_moves       


