# python-ai-dnd

```txt
######################################################
  /$$$$$$  /$$$$$$       /$$   /$$ /$$$$$$$   /$$$$$$ 
 /$$__  $$|_  $$_/      | $$$ | $$| $$__  $$ /$$__  $$
| $$  \ $$  | $$        | $$$$| $$| $$  \ $$| $$  \__/
| $$$$$$$$  | $$        | $$ $$ $$| $$$$$$$/| $$      
| $$__  $$  | $$        | $$  $$$$| $$____/ | $$      
| $$  | $$  | $$        | $$\  $$$| $$      | $$    $$
| $$  | $$ /$$$$$$      | $$ \  $$| $$      |  $$$$$$/
|__/  |__/|______/      |__/  \__/|__/       \______/ 
######################################################
```

## Setup
```sh
source env/bin/activate
python3 -m pip install --upgrade pip
pip install -r requirements.txt
```

## create a run.sh script with the following
```sh
#!/bin/sh
export OPENAI_API_KEY="YOUR OPENAI API KEY"
python3 app.py
```

Run this script to play D&D with an AI player.  
You must be the game master

The game doesn't have a natural ending, so ctrl-c to get out.


## Releases and Progress

v1 - 2023-04-16 - AI NPC plays D&D with a human GM in search of treasure. The AI NPC is a warrior.