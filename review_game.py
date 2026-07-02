import chess
import chess.pgn
import chess.engine

engine = chess.engine.SimpleEngine.popen_uci(
    "/Users/surendars/Downloads/stockfish/stockfish-macos-m1-apple-silicon"
)

pgn = open("game.pgn")

game = chess.pgn.read_game(pgn)

board = game.board()

best = 0
excellent = 0
good = 0
inaccuracy = 0
mistake = 0
blunder = 0


def classify(cp_loss):

    if cp_loss <= 10:
        return "best"

    elif cp_loss <= 30:
        return "excellent"

    elif cp_loss <= 75:
        return "good"

    elif cp_loss <= 150:
        return "inaccuracy"

    elif cp_loss <= 300:
        return "mistake"

    return "blunder"


for move in game.mainline_moves():

    before = engine.analyse(
        board,
        chess.engine.Limit(depth=12)
    )

    best_score = before["score"].white().score(
        mate_score=10000
    )

    board.push(move)

    after = engine.analyse(
        board,
        chess.engine.Limit(depth=12)
    )

    played_score = after["score"].white().score(
        mate_score=10000
    )

    cp_loss = abs(best_score - played_score)

    result = classify(cp_loss)

    if result == "best":
        best += 1

    elif result == "excellent":
        excellent += 1

    elif result == "good":
        good += 1

    elif result == "inaccuracy":
        inaccuracy += 1

    elif result == "mistake":
        mistake += 1

    else:
        blunder += 1


print("Best:", best)
print("Excellent:", excellent)
print("Good:", good)
print("Inaccuracy:", inaccuracy)
print("Mistake:", mistake)
print("Blunder:", blunder)

engine.quit()