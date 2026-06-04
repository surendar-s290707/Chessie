from flask import Flask, request
from chessie import analyze_openings

app = Flask(__name__)

# -----------------------------------
# HOME PAGE
# -----------------------------------

@app.route("/")
def home():

    return """
    <html>

    <head>

        <title>Chessie</title>

        <style>

            body{
                background-color:#1e1e1e;
                color:white;
                font-family:Arial;
                text-align:center;
                padding-top:50px;
            }

            .box{
                background:#2c2c2c;
                width:500px;
                margin:auto;
                padding:30px;
                border-radius:15px;
                box-shadow:0px 0px 20px black;
            }

            input, select{
                padding:10px;
                width:80%;
                margin-top:10px;
                border:none;
                border-radius:8px;
                font-size:16px;
            }

            button{
                margin-top:20px;
                padding:12px 25px;
                border:none;
                border-radius:10px;
                background:#769656;
                color:white;
                font-size:18px;
                cursor:pointer;
            }

            button:hover{
                background:#5f7d46;
            }

            h1{
                color:#f0d9b5;
            }

        </style>

    </head>

    <body>

        <div class="box">

            <h1>♟ Chessie</h1>

            <h3>Behavior-Based Chess Analyzer</h3>

            <form action="/analyze">

                <input
                    type="text"
                    name="username"
                    placeholder="Enter Chess.com Username"
                    required
                >

                <br>

                <input
                    type="number"
                    name="num_games"
                    value="50"
                    min="1"
                    max="500"
                >

                <br>

                <select name="time_class">

                    <option value="all">All Formats</option>
                    <option value="rapid">Rapid</option>
                    <option value="blitz">Blitz</option>
                    <option value="bullet">Bullet</option>

                </select>

                <br>

                <button type="submit">
                    Analyze Player
                </button>

            </form>

        </div>

    </body>

    </html>
    """


# -----------------------------------
# ANALYZE PAGE
# -----------------------------------

@app.route("/analyze")
def analyze():

    username = request.args.get("username")

    num_games = int(
        request.args.get("num_games", 50)
    )

    time_class = request.args.get("time_class","all").lower()

    result = analyze_openings(
        username,
        num_games,
        time_class
    )

    # -----------------------------------
    # ERROR HANDLING
    # -----------------------------------

    if "error" in result:

        return f"""
        <h2>Error</h2>
        <p>{result['error']}</p>
        <a href="/">Go Back</a>
        """

    # -----------------------------------
    # OPENINGS HTML
    # -----------------------------------
    
    opening_html = ""

    for opening, count in sorted(
        result["opening_stats"].items(),
        key=lambda x: x[1],
        reverse=True
    ):

        search_query = opening.replace(" ", "+")

        url = (
            "https://www.google.com/search?q="
            + search_query
            + "+chess.com"
        )

        opening_html += f"""
        <p>
        <a href="{url}" target="_blank">
        {opening}
        </a>: {count}
        </p>
        """

        # -----------------------------------
        # FINAL PAGE
        # -----------------------------------

    return f"""

    <html>

    <head>

        <title>{username} Report</title>

        <style>

            body{{
                background:#1e1e1e;
                color:white;
                font-family:Arial;
                padding:40px;
            }}

            .container{{
                width:700px;
                margin:auto;
                background:#2c2c2c;
                padding:30px;
                border-radius:15px;
            }}

            h1,h2{{
                color:#f0d9b5;
            }}

            .metric{{
                background:#3a3a3a;
                padding:15px;
                margin-top:10px;
                border-radius:10px;
            }}

            a{{
                color:#90caf9;
                text-decoration:none;
            }}

        </style>

    </head>

    <body>

        <div class="container">

            <h1>♟ {username}</h1>

            <h3>Format: {time_class}</h3>

            <h3>Games Analyzed: {result['games_analyzed']}</h3>

            <h2>Opening Breakdown</h2>

            {opening_html}

            <h2>Behavior Metrics</h2>

            <div class="metric">
                Early Queen Rate:
                {result['early_queen_rate']}
            </div>

            <div class="metric">
                Development Delay Rate:
                {result['development_delay_rate']}
            </div>

            <div class="metric">
                Castling Delay Rate:
                {result['castling_delay_rate']}
            </div>

            <div class="metric">
                Early Loss Rate:
                {result['early_loss_rate']}
            </div>

            <div class="metric">
                Average Game Length:
                {result['avg_game_length']}
            </div>

            <br><br>

            <a href="/">← Analyze Another Player</a>

        </div>

    </body>

    </html>

    """


# -----------------------------------
# RUN APP
# -----------------------------------

if __name__ == "__main__":

    app.run(debug=True, port=5001)