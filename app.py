from flask import Flask, render_template, request
import json
import os

app = Flask(__name__)

def load_players():
    data_path = os.path.join(app.root_path, "data", "players.json")
    with open(data_path, "r", encoding="utf-8") as f:
        return json.load(f)

@app.route("/")
def index():
    players = load_players()
    total_goals = sum(p["goals"] for p in players)
    total_assists = sum(p["assists"] for p in players)

    return render_template(
        "index.html",
        players=players,
        total_goals=total_goals,
        total_assists=total_assists
    )

@app.route("/players")
def players():
    players = load_players()
    return render_template("players.html", players=players)

@app.route("/compare", methods=["GET", "POST"])
def compare():
    players = load_players()
    player1 = player2 = None

    if request.method == "POST":
        name1 = request.form.get("player1")
        name2 = request.form.get("player2")

        player1 = next((p for p in players if p["name"] == name1), None)
        player2 = next((p for p in players if p["name"] == name2), None)

    return render_template(
        "compare.html",
        players=players,
        player1=player1,
        player2=player2
    )

if __name__ == "__main__":
    app.run(debug=True)
