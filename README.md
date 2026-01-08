# Overview

  1. What does this project do?
  2. How do I set it up?
  3. What settings can I change?
  4. What is coming next?


## 1. What does this project do?

This picks a random opening, generates the corresponding FEN and can invite a friend to an unranked match on lichess.org. You can switch up your games with friends if you feel like playing without starting with the same openings you already know your friends for.

## 2. How do I set it up?

  1. Clone the repository to your local machine.
  2. Create a virtual environment in the corresponding folder.
  3. Activate the environment.
  4. Run "pip install -r requirements.txt" to install the needed packages.
  5. Run the script. If the terminal displays an opening name and a corresponding FEN everything works.

  At this point the skript is basically a random opening generator and can be used as such, to automatically invite a friend with this script follow the next steps.
     
  6. Open lichess.org logged in with your account.
  7. Go to settings -> API access tokens -> generate a personal access token
  8. Generate a token with the "challenge:write" option selected (others can also be selected) and safe the token somewhere.
  9. Open the python script "main.py" and find the variable lichess_API_key and change it from the default None to "INSERT_YOUR_TOKEN_HERE". The "" are important since it is treated as a string in the code.

  When running the code like this you generate a random opening and challenge the bot maia1 to a game with this opening.

## 3. What settings can I change?
   
   friend_ID:     This variable can be changed to the lichess username of the friend you want to challenge.
   
   start_time:     This is the time every player has at the beginning of the game in seconds. default = 300
   
   increment:     This is the time increment given to the player when making a move. default = 3
   
   color:     You can chose which color you want to play. default = "random" ("white", "black")
   
   engine_difference_threshold:     Since some openings create a strong imbalance in engine evaluation some players might want to filter for "bad" openings (e.g. the Goblin starts at -2.1 eval). If an opening presents a bad position for one of the players a new opening is drawn. default = 1 (if all openings should be included set the threshold higher)

## 4. What is coming next?
   
   1. Add a blacklist for openings in case you want to blacklist an opening like e.g. the Sicilian since it has a lot of variations and if you don't like it it may appear too often.
   2. A weighting system for the openings will be implemented to make openings with increasing numbers of variations less likely to be picked.
   3. Setting up a Browser Extension to increase accessability.
