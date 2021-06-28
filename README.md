# Kuba (Traboulet)
This project features a recreation of the Kuba (aka Traboulet) board game in Python. 

### Overview
This is a CLI-based board game for 2 players. The objective of the game is for one of the player to push off & capture 7 neutral red marbles or by pushing off all of the opponent's marbles. A player who has no legal moves available has lost the game. For further detail, please reference ![here](https://sites.google.com/site/boardandpieces/list-of-games/kuba).

This game features also ![ko rule](https://sites.google.com/site/boardandpieces/terminology/ko-rule?authuser=0) which prevents players from repeating the same move back-and-fourth (to prevent stalemate). This has been implemented by creating deep copies of existing board and comparing the current board state with stored (previous) state.

Please note that this iteration of the game does not feature some of the rules defined in the original game.
- Player may **not** take extra turn when their last move pushes off a neutral or opposing marble 

---

### Installation
Using your Terminal/Command Line, clone the repository into your local Python workspace.
```
$ git clone https://github.com/fusakoo/kuba_game.git
$ cd kuba_game
```

---

### Features
TBD

### TODO
- Implement a preview of the board when user makes a move.

---

### Bug Log
07/27/2021 - Currently there is a specific scenario where the turn tracking is not working as expected.
1. Initialize game
2. make_move(playerA, (6, 5), “F”)
3. make_move(playerA, (5, 5), “F”) >> Player A should not be allowed to move twice
Require fix implementation.
