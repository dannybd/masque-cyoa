# CYOA bot for Masquerade

Extensions:
* `start_cyoa` defines the trapdoor behavior
* `setup_cyoa` initializes CYOA channels with their text and buttons
* `auto_delete` ensures messages are erased in CYOA channels
* `reacts` handle movement between channels by way of rooms

## Usage
```
cp config.ini-template config.ini
# set up your configuration to the DB, asyncio_server ports, etc.
nano config.ini
```

Then, run `./bot.py` to start the bot.
