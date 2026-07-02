from flask import Flask, request,render_template
from chessie import analyze_openings

app = Flask(__name__)

# -----------------------------------
# HOME PAGE
# -----------------------------------
@app.route("/studio")
def studio():

    return render_template(
        "analysis_studio.html"
    )


@app.route("/")
def home():

    return """
    <html>

    <head>
        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
        <title>Chessie</title>
        <style>
            .copy-btn {

        background: #2a2a2a;

        color: #e8d8b5;

        border: 1px solid #444;

        padding: 12px 20px;

        border-radius: 12px;

        font-size: 16px;

        font-weight: 600;

        cursor: pointer;

        transition: 0.2s;
    }

    .copy-btn:hover {

        background: #3a3a3a;

        border-color: #e8d8b5;

        transform: translateY(-2px);
    }

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


    .filters{
    display:flex;
    align-items:flex-end;
    gap:32px;
    flex-wrap:wrap;
    }

    .filter-group{
        display:flex;
        flex-direction:column;
        gap:10px;
    }

    .filter-group label{
        font-size:18px;
        font-weight:600;
        color:#f4e3c1;
    }

    .filter-group input,
    .filter-group select{

        width:180px;
        height:56px;

        border-radius:14px;

        background:#1d1d1d;

        color:white;

        border:1px solid #555;

        padding:0 18px;

        font-size:22px;
    }   

    .update-btn{

        height:56px;

        padding:0 30px;

        border-radius:14px;

        background:#5da6ff;

        color:white;

        border:none;

        font-size:20px;

        font-weight:600;

        cursor:pointer;

        transition:.2s;
    }

    .update-btn:hover{

        background:#3d8cff;

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
                    placeholder="Chess.com Username"
                    required
                >

                <button type="submit">
                    Analyze
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

    num_games = int(request.args.get("num_games", 100))

    time_class = request.args.get("time_class", "all").lower()

    color = request.args.get("color", "all")

    rated_filter = request.args.get("rated", "all").lower()

    result = analyze_openings(
        username,
        num_games,
        color,
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

    for opening, data in sorted(
        result["grouped_openings"].items(),
        key=lambda x: x[1]["games"],
        reverse=True
    ):

        opening_html += f"""
        <details>

            <summary>

                <b>{opening}</b>

                ({data['games']} games)

                W:{data['win_pct']}%

                D:{data['draw_pct']}%

                L:{data['loss_pct']}%

            </summary>
        """

        for variation, vdata in sorted(
            data["variations"].items(),
            key=lambda x: x[1]["games"],
            reverse=True
        ):

            opening_html += f"""
            <p style="margin-left:20px;">

                {variation}

                ({vdata['games']} games)

                W:{vdata['win_pct']}%

                D:{vdata['draw_pct']}%

                L:{vdata['loss_pct']}%

            </p>
            """

        opening_html += "</details><br>"
        

        # -----------------------------------
        # FINAL PAGE
        # -----------------------------------

    chart_labels = []
    chart_wins = []
    chart_draws = []
    chart_losses = []

    for opening, data in sorted(
        result["grouped_openings"].items(),
        key=lambda x: x[1]["games"],
        reverse=True
    )[:10]:

        chart_labels.append(opening)

        chart_wins.append(data["win"])

        chart_draws.append(data["draw"])

        chart_losses.append(data["loss"])

    import json

    labels_js = json.dumps(chart_labels)
    wins_js = json.dumps(chart_wins)
    draws_js = json.dumps(chart_draws)
    losses_js = json.dumps(chart_losses)

    return f"""

    <html>

    <head>

        <title>{username} Report</title>
        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
        <style>
            .copy-btn {{

        background: #2a2a2a;

        color: #e8d8b5;

        border: 1px solid #444;

        padding: 12px 20px;

        border-radius: 12px;

        font-size: 16px;

        font-weight: 600;

        cursor: pointer;

        transition: 0.2s;
    }}

    .copy-btn:hover {{

        background: #3a3a3a;

        border-color: #e8d8b5;

        transform: translateY(-2px);
    }}

            # body{{
            #     background-color:#1e1e1e;
            #     color:white;
            #     font-family:Arial;
            #     text-align:center;
            #     padding-top:50px;
            # }}

            # .box{{
            #     background:#2c2c2c;
            #     width:500px;
            #     margin:auto;
            #     padding:30px;
            #     border-radius:15px;
            #     box-shadow:0px 0px 20px black;
            # }}

            # input, select{{
            #     padding:10px;
            #     width:80%;
            #     margin-top:10px;
            #     border:none;
            #     border-radius:8px;
            #     font-size:16px;
            # }}

            # button{{
            #     margin-top:20px;
            #     padding:12px 25px;
            #     border:none;
            #     border-radius:10px;
            #     background:#769656;
            #     color:white;
            #     font-size:18px;
            #     cursor:pointer;
            # }}

            # button:hover{{
            #     background:#5f7d46;
            # }}

            # h1{{
            #     color:#f0d9b5;
            # }}
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

        .filter-bar{{

    background:#343434;

    padding:20px;

    border-radius:12px;

    margin:25px 0;
}}

.filter-bar form{{

    display:flex;

    gap:20px;

    align-items:end;

    flex-wrap:wrap;
}}

.filter-item{{

    display:flex;

    flex-direction:column;
}}

.filter-item label{{

    margin-bottom:6px;

    color:#f0d9b5;

    font-weight:bold;
}}

.filter-item select{{

    padding:10px;

    border-radius:8px;

    background:#222;

    color:white;

    border:1px solid #555;
}}

        </style>

    </head>

    <body>

        <div class="container">


            <h1>♟ {username}</h1>

            <div class="filter-bar">

                <form action="/analyze" method="GET">

                    <input
                        type="hidden"
                        name="username"
                        value="{username}"
                    >

                    <div class="filter-item">

                        <label>Games</label>

                        <input
                            type="number"
                            name="num_games"
                            value="{num_games}"
                            min="1"
                            max="1000"
                            style="
                                width:90px;
                                padding:8px;
                                border-radius:8px;
                                border:none;
                                text-align:center;
                                background:#3a3a3a;
                                color:white;
                            "
                        >

                    </div>

                    <div class="filter-item">

                        <label>Time Control</label>

                        <select name="time_class">

                            <option value="all" {"selected" if time_class=="all" else ""}>All</option>

                            <option value="rapid" {"selected" if time_class=="rapid" else ""}>Rapid</option>

                            <option value="blitz" {"selected" if time_class=="blitz" else ""}>Blitz</option>

                            <option value="bullet" {"selected" if time_class=="bullet" else ""}>Bullet</option>

                        </select>

                    </div>

                    <div class="filter-item">

                        <label>Rated</label>

                        <select name="rated">

                            <option value="all" {"selected" if rated_filter=="all" else ""}>All</option>

                            <option value="rated" {"selected" if rated_filter=="rated" else ""}>Rated</option>

                            <option value="unrated" {"selected" if rated_filter=="unrated" else ""}>Unrated</option>

                        </select>

                    </div>
                    <div class="filter-item">
                        <label>Played As</label>

                        <select name="color" class="filter-select">
                            <option value="all"
                                {"selected" if color=="all" else ""}>
                                All
                            </option>

                            <option value="white"
                                {"selected" if color=="white" else ""}>
                                White
                            </option>

                            <option value="black"
                                {"selected" if color=="black" else ""}>
                                Black
                            </option>
                        </select>
                    </div>

                    <button class="update-btn">
                        Update Report
                    </button>

                </form>

            </div>
                    

            <p><b>Games Analyzed:</b> {result['games_analyzed']}</p>

            <button
                id="copyBtn"
                class="copy-btn"
                onclick="copyReport()"
            >
                📋 Copy Report Link
            </button>


            <h2>Opening Distribution</h2>

            <div style="
                background:#2d2d2d;
                padding:20px;
                border-radius:15px;
                margin-bottom:30px;
            ">
                <canvas id="openingChart"></canvas>
            </div>

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

        <script>

    function copyReport() {{

        navigator.clipboard.writeText(
            window.location.href
        );
        const btn = document.getElementById("copyBtn");

        btn.innerText = "✅ Link Copied";

        setTimeout(() => {{

            btn.innerText = "📋 Copy Report Link";

        }}, 2000);
    }}

    </script>
    <script>

    const ctx = document.getElementById('openingChart');

    new Chart(ctx, {{

        type: 'bar',

        data: {{

            labels: {labels_js},

            datasets: [

                {{
                    label: 'Wins',
                    data: {wins_js},
                    backgroundColor: '#22c55e'
                }},

                {{
                    label: 'Draws',
                    data: {draws_js},
                    backgroundColor: '#9ca3af'
                }},

                {{
                    label: 'Losses',
                    data: {losses_js},
                    backgroundColor: '#ef4444'
                }}

            ]
        }},

        options: {{

            responsive: true,

            indexAxis: 'y',

            scales: {{

                x: {{
                    stacked: true
                }},

                y: {{
                    stacked: true
                }}
            }},

            plugins: {{

                legend: {{
                    labels: {{
                        color: 'white'
                    }}
                }}
            }}
        }}
    }});

    </script>
    </body>

    </html>

    """


# -----------------------------------
# RUN APP
# -----------------------------------

if __name__ == "__main__":

    app.run(debug=True, port=5001)