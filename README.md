# Pyndemic

## Description
This is a future digital implementation of the original [Pandemic board game][official].
This project is started after [this repository][ref] and is expected to be written in Python with perspectives to become a standalone application.

## Project status
_v0.2.0_

This release implements MVP providing minimalistic console client with limited gameplay and hotseat multiplayer introduced.
Also, it's now adapted for being wrapped in a simple server application.

Here's part of how a console game session looks for now:

![gameplay screenshot](/doc/readme/game_screenshot_1.png)

Game mechanics:
 - [x] Basic player actions
 - [x] Epidemic events
 - [x] Outbreak events
 - [x] Win and Fail conditions
 - [x] Effective treats for cured diseases
 - [ ] Special characters and their actions
 - [ ] Event Cards
 - [ ] Hand Limit

## How to

### Requirements
For now, the application requires a Python version 3.6 or higher to be installed on your computer for a console playing.

### Run the game in console
To play a game, run a console client in an interactive mode:
```bash
python3 pyndemic.py
```

### Possible commands
The console mode supports the following commands:

 * `move <location>` - perform a standard move action
 * `fly <location>` - perform a direct flight action
 * `charter <location>` - perform a charter flight action
 * `shuttle <location>` - perform a shuttle flight action
 * `build` - perform a laboratory build action
 * `treat <colour>` - perform a treat disease action
 * `cure <card_1> ... <card_5>` - perform a cure disease action
 * `share <card> <player name>` - perform a share knowledge action
 * `pass` - end turn

Also you can do `Ctrl`+`C` to terminate the game.

### Test run
For tests run:
```bash
python3 -m unittest
```

And for running test game session you can type:
```bash
python3 pyndemic.py 42 <test/test_input.txt
```

---
## From [Developer Zero][ref-user]
**What is this?**

This is a simple project I started a while ago to help learn how to use vim, python and github. It has changed a bit from it's original form, and is now an attempt to create a version of the game Pandemic with AI players who try to complete the game, and is now written in Java rather than python.


[official]: https://www.zmangames.com/en/games/pandemic/ "Official page"
[ref]: https://github.com/Joesalmon1985/PandemicBoardGame "Base repository"
[ref-user]: https://github.com/Joesalmon1985 "Joe Salmon"
