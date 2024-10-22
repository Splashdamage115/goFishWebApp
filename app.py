from flask import Flask, render_template, session, flash, redirect, request
import cards
import random

app = Flask(__name__)

app.secret_key = " b0981x2'7rbpxr09483r431x 0nN740P9T4XNC8243-ny8p29fn32480-2n8p249-3fg24ny0fn209]'234]#of432n2f[08]"

def checkPlayerHasCard(selected_value):
    """
    check if the player has the card requested
    """
    value = session["computerRequest"][: session["computerRequest"].find(" ")]
    if selected_value == value.lower():
        return True
    return False

def checkPlayerGoFish():
    """
    check if the player has the card requested
    """
    value = session["computerRequest"][: session["computerRequest"].find(" ")]
    # swap code
    for n, card in enumerate(session["player"]):
        if card.startswith(value):
            return True
    return False

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
        deck = len(session["deck"]),
        playerPair = len(session["player_pairs"]),
        computerPair = len(session["computer_pairs"]),
        resolveCard = "none.png",
        animateCard = "none.png",
        disolveCard = "welcomCard.png"
    )



@app.get("/select/<value>")
def processCardSelection(value):
    found_it = False
    drawn = "none.png"
    drawType = "none.png"
    for n, card in enumerate(session["computer"]):
        if card.startswith(value):
            found_it = n
            break

    if isinstance(found_it, bool):
        # go fish code
        flash("\nGo Fish\n")
        session["player"].append(session["deck"].pop())
        flash(f"You drew a {session["player"][-1]}")
        drawType = "goFishCard.png"
    else:
        # swap code
        flash(f"Here is your card: {session["computer"][n]}.")
        session["player"].append(session["computer"].pop(n))

    drawn = session["player"][-1]

    session["player"], pairs = cards.identify_remove_pairs(session["player"])
    session["player_pairs"].extend(pairs)

    if len(session["player"]) == 0 or len(session["computer"]) == 0 or len(session["deck"]) == 0:
         return redirect("/gameOver")

    drawn = drawn.lower().replace(" ", "_") + ".png"
    card_images = [card.lower().replace(" ", "_") + ".png" for card in session["player"]]

    
    card = random.choice(session["computer"])
    session["computerRequest"] = card
    the_value = card[: card.find(" ")]
    chosen = the_value.lower() + "_request.png"
    

    return render_template(
        "pickCard.html",
        title = "The Computer wants to Know",
        value = the_value,
        cards = card_images, # available in the template as {{  cards  }}
        n_computer = len(session["computer"]), # available in the template as {{  n_computer  }}
        deck = len(session["deck"]),
        playerPair = len(session["player_pairs"]),
        computerPair = len(session["computer_pairs"]),
        resolveCard = chosen,
        animateCard = drawn,
        disolveCard = drawType
    )

@app.get("/liarPage")
def liarPage():
    drawType = "none.png"
    drawn = session["player"][-1]
    drawn = drawn.lower().replace(" ", "_") + ".png"
    card_images = [card.lower().replace(" ", "_") + ".png" for card in session["player"]]

    
    card = session["computerRequest"]
    the_value = card[: card.find(" ")]
    chosen = the_value.lower() + "_request.png"
    

    return render_template(
        "pickCard.html",
        title = "The Computer wants to Know",
        value = the_value,
        cards = card_images, # available in the template as {{  cards  }}
        n_computer = len(session["computer"]), # available in the template as {{  n_computer  }}
        deck = len(session["deck"]),
        playerPair = len(session["player_pairs"]),
        computerPair = len(session["computer_pairs"]),
        resolveCard = chosen,
        animateCard = drawn,
        disolveCard = drawType
    )

@app.get("/pick/<value>")
def processCardHandOver(value):
    face = "back.png"
    if value == "0":
        session["computer"].append(session["deck"].pop())
        if checkPlayerGoFish():
            return redirect("/liarPage")
    else:
        if not checkPlayerHasCard(value):
            return redirect("/liarPage")
        for n, card in enumerate(session["player"]):
                if card.startswith(value.title()):
                    break
        session["computer"].append(session["player"].pop(n))
        face = session["computer"][-1].lower().replace(" ", "_") + ".png"

    session["computer"], pairs = cards.identify_remove_pairs(session["computer"])
    session["computer_pairs"].extend(pairs)

    if len(session["player"]) == 0 or len(session["computer"]) == 0 or len(session["deck"]) == 0:
        return redirect("/gameOver")

    card_images = [card.lower().replace(" ", "_") + ".png" for card in session["player"]]


    
    return render_template(
        "startgame.html",
        title = "Keep Playing!",
        cards = card_images, # available in the template as {{  cards  }}
        n_computer = len(session["computer"]), # available in the template as {{  n_computer  }}
        deck = len(session["deck"]),
        playerPair = len(session["player_pairs"]),
        computerPair = len(session["computer_pairs"]),
        resolveCard = "none.png",
        animateCard = face,
        disolveCard = "none.png"
    )


@app.get("/gameOver")
def gameOver():
    text = ""
    if len(session["player_pairs"]) > len(session["computer_pairs"]):
        text = "You Won!"
    elif len(session["player_pairs"]) < len(session["computer_pairs"]):
        text = "You Lost!"
    else:
        text = "It was a Draw!"
    return render_template(
        "gameOver.html",
        title = text,
        playerPair = len(session["player_pairs"]),
        computerPair = len(session["computer_pairs"])
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