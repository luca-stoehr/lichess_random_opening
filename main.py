# Challenge a friend on Lichess.org to a game starting from a random opening position
# Author: Luca Stöhr on 07.01.2025
import http.client
import re
import random
import chess
import chess.pgn
from io import StringIO
import urllib.parse

# User settings -----------------------------------------------------------
lichess_API_key = None     # your lichess API key with challenge permissions as string
friend_ID = "maia1"         # lichess username of friend to challenge
start_time = 300            # in seconds
increment = 3               # in seconds
color = "random"            # "white", "black", or "random"
engine_difference_threshold = 1

# Don't change below this line --------------------------------------------

def draw_random_opening(openings, engine_difference_threshold):
    random_opening = random.choice(openings)
    conn.request("GET", "/opening/{}".format(random_opening))

    res2 = conn.getresponse()
    data_opening = res2.read()

    # Extract the PGN from html of opening page
    pgn_string = re.findall(r'/analysis/pgn/([^"]+)#', data_opening.decode("utf-8"))[0]    #every opening page has a link to its pgn analysis

    # Get engine analysis and fen from pgn link
    pgn = StringIO(pgn_string)
    game = chess.pgn.read_game(pgn)
    board = game.end().board()

    fen = board.fen()
    fen_encoded = urllib.parse.quote(fen)

    conn.request("GET", "/api/cloud-eval?fen={}".format(fen_encoded))
    res3 = conn.getresponse()
    engine_data = res3.read()
    engine_rating_string = re.findall(r'"cp":(-?\d+)', engine_data.decode("utf-8"))[0]
    if abs(int(engine_rating_string)) > engine_difference_threshold*100:
        print(f"Engine rating {int(engine_rating_string)/100} is too high, redrawing opening.")
        [random_opening, fen] = draw_random_opening(openings, engine_difference_threshold)
    return random_opening, fen

conn = http.client.HTTPSConnection("lichess.org")

# Get the list of openings
conn.request("GET", "/opening/tree")

res1 = conn.getresponse()
data = res1.read()

openings = re.findall(r'/opening/([^"]+)"', data.decode("utf-8"))

[random_opening, fen] = draw_random_opening(openings, engine_difference_threshold)

print(f"Selected Opening: {random_opening}")
print(f"FEN: {fen}")

if lichess_API_key:
    headers = {
        'Content-Type': "application/x-www-form-urlencoded",
        'Authorization': "Bearer {}".format(lichess_API_key)
    }

    data = urllib.parse.urlencode({
        "clock.limit": start_time,
        "clock.increment": increment,
        "color": "random",
        "fen": fen,
        "variant": "standard"
    })

    conn.request("POST", "/api/challenge/{}".format(friend_ID), data, headers)
    conn.close()
    print(f"Challenge sent to {friend_ID}!")
