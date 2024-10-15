from flask import Flask, render_template, session
import cards
import random

app = Flask(__name__)

app.secret_key = " b0981x2'7rbpxr09483r431x 0nN740P9T4XNC8243-ny8p29fn32480-2n8p249-3fg24ny0fn209]'234]#of432n2f[08]"

PATH = "static/cards/"

@app.get("/startgame")
def start():
    resetGame()
    card_images = [PATH + card.lower().replace(" ", "_") + ".png" for card in session["player"]]
    return render_template(
        "startgame.html",
        title = "Welcome to GoFish for the web!",
        cards = card_images, # available in the template as {{  cards  }}
        n_computer = len(session["computer"]) # available in the template as {{  n_computer  }}
    )

def resetGame():
    session["computer"] = []
    session["player"] = []
    session["player_pairs"] = []
    session["computer_pairs"] = []
    session["deck"] = cards.generateDeck()

    for _ in range(7):
        session["computer"].append(session["deck"].pop())
        session["player"].append(session["deck"].pop())

    session["player"], pairs = cards.identify_remove_pairs(session["player"])
    session["player_pairs"].extend(pairs)
    session["computer"], pairs = cards.identify_remove_pairs(session["computer"])
    session["computer_pairs"].extend(pairs)

app.run(debug=True)