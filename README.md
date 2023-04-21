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

## Setup Linux / Mac
```sh
python3 -m venv env
source env/bin/activate
python3 -m pip install --upgrade pip
pip install -r requirements.txt
```


### create a run.sh script with the following
```sh
#!/bin/sh
export OPENAI_API_KEY="YOUR OPENAI API KEY"
export TOKENIZERS_PARALLELISM=false
python3 app.py
```

## Setup Windows
```sh
python3.exe -m venv env
.\\env\Scripts\activate
python.exe -m pip install --upgrade pip
pip install -r requirements-win.txt
```
### create a run.sbat script with the following
```bat
@echo off
set OPENAI_API_KEY="YOUR OPENAI API KEY"
set TOKENIZERS_PARALLELISM=false
python.exe app.py
```



Run this script to play D&D with an AI player.  
You must be the game master

The game doesn't have a natural ending, so ctrl-c to get out.


## Releases and Progress


v3 - 2023-04-19 - AI Dungeon master -- not very smart
v2 - 2023-04-17 - Multiple NPCs play with a human GM, lots of cleanup
v1 - 2023-04-16 - AI NPC plays D&D with a human GM in search of treasure. The AI NPC is a warrior.