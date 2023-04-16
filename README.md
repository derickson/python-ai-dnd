# python-ai-dnd

```txt
####################################################################
   _____  .___  ________                                            
  /  _  \ |   | \______ \  __ __  ____    ____   ____  ____   ____  
 /  /_\  \|   |  |    |  \|  |  \/    \  / ___\_/ __ \/  _ \ /    \ 
/    |    \   |  |    `   \  |  /   |  \/ /_/  >  ___(  <_> )   |  \
\____|__  /___| /_______  /____/|___|  /\___  / \___  >____/|___|  /
        \/              \/           \//_____/      \/           \/ 
#####################################################################
```

## Setup
```sh
source env/bin/activate
pip install -r requirements.txt
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
