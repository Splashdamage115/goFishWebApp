from flask import Flask, render_template, session, flash
import cards
import random

app = Flask(__name__)

app.secret_key = " b0981x2'7rbpxr09483r431x 0nN740P9T4XNC8243-ny8p29fn32480-2n8p249-3fg24ny0fn209]'234]#of432n2f[08]"

@app.get("/startgame")
@app.get("/")
def start():
    resetGame()
    card_images = [card.lower().replace(" ", "_") + ".png" for card in session["player"]]
    return render_template(
        "startgame.html",
        title = "Welcome to GoFish for the web!",
        cards = card_images, # available in the template as {{  cards  }}
        n_computer = len(session["computer"]), # available in the template as {{  n_computer  }}
        deck = len(session["deck"])
    )

@app.get("/select/<value>")
def processCardSelection(value):
    found_it = False
    for n, card in enumerate(session["computer"]):
        if card.startswith(value):
            found_it = n
            break

    if isinstance(found_it, bool):
        # go fish code
        flash("\nGo Fish\n")
        session["player"].append(session["deck"].pop())
        flash(f"You drew a {session["player"][-1]}")
        ## what to do when there are no more cards in the deck
        ## if len(session["deck"]) == 0:
        ##     break
    else:
        # swap code
        flash(f"Here is your card: {session["computer"][n]}.")
        session["player"].append(session["computer"].pop(n))
    
    session["player"], pairs = cards.identify_remove_pairs(session["player"])
    session["player_pairs"].extend(pairs)

    ## what to do when the player or computer has won!
    ## if len(player) == 0:
    ##     print("The game is over. The player Won!")
    ##     break
    ## if len(computer) == 0:
    ##     print("The game is over. The computer Won!")
    ##     break

    card_images = [card.lower().replace(" ", "_") + ".png" for card in session["player"]]

    card = random.choice(session["computer"])
    the_value = card[: card.find(" ")]

    return render_template(
        "pickCard.html",
        title = "The Computer wants to Know",
        value = the_value,
        cards = card_images, # available in the template as {{  cards  }}
        n_computer = len(session["computer"]), # available in the template as {{  n_computer  }}
        deck = len(session["deck"])
    )

@app.get("/pick/<value>")
def processCardHandOver(value):
    if value == "0":
        session["computer"].append(session["deck"].pop())
    else:
        for n, card in enumerate(session["player"]):
                if card.startswith(value.title()):
                    break
        session["computer"].append(session["player"].pop(n))

    session["computer"], pairs = cards.identify_remove_pairs(session["computer"])
    session["computer_pairs"].extend(pairs)

    card_images = [card.lower().replace(" ", "_") + ".png" for card in session["player"]]
    
    return render_template(
        "startgame.html",
        title = "Keep Playing!",
        cards = card_images, # available in the template as {{  cards  }}
        n_computer = len(session["computer"]), # available in the template as {{  n_computer  }}
        deck = len(session["deck"])
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