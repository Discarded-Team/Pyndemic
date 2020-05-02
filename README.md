# Pandemic Board Game (digital version)

## Description
This is an attempt to create a digital version of the original [Pandemic board game][official].
This version is forked from [original repository][ref] and is expected to be written in Python with perspectives to become a standalone application.

## Project status
Current release version is 0.1. This release is focused on implementing MPV. Minimalistic console client with limited gameplay and hotseat multiplayer introduced.
Here's part of a game log:
![gameplay screenshot](/assets/readme/game_screenshot_1.png)

Game mechanics:
 - [x] Basic player actions
 - [x] Epidemic event
 - [x] Outbreak event
 - [x] Win and Fail conditions
 - [ ] Special character actions
 - [ ] Event Cards
 - [ ] Hand Limit

## How to
Run console client in interactive mode:
```bash
python3 pyndemic.py
```
or read commands form file:
```bash
python3 pyndemic.py commands.txt
```

Run tests:
```bash
python3 -m unittest
```

---
## From Developer Zero
**What is this?**

This is a simple project I started a while ago to help learn how to use vim, python and github. It has changed a bit from it's original form, and is now an attempt to create a version of the game Pandemic with AI players who try to complete the game, and is now written in Java rather than python.


[official]: https://www.zmangames.com/en/games/pandemic/ "Official page"
[ref]: https://github.com/Joesalmon1985/PandemicBoardGame "Base repository"

