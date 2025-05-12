# AprilTag Turn-Based Combat Game

This is a turn-based combat game where two players use an AprilTag to draw symbols in the air. The system recognizes the drawn symbol and triggers different attacks. Each player takes turns, and the first to reduce the opponent's HP to zero wins!

## How to Play
- **Player 1 starts.**
- Hold the **spacebar** to start drawing with the AprilTag (move the tag in front of your webcam).
- Release the **spacebar** and press **'s'** to stop drawing and trigger symbol recognition.
- The recognized symbol determines your attack:
  - **Circle:** Heal yourself (+3 HP)
  - **Triangle:** Fireball (deal 4 damage)
  - **Line:** Slash (deal 2 damage)
- The game displays HP and whose turn it is.
- The first player to reduce the opponent's HP to zero wins.
- Press **'q'** to quit at any time.

## Requirements
- Python 3.7+
- OpenCV (`opencv-python`)
- NumPy
- SciPy
- pupil_apriltags

Install dependencies with:
```
pip install opencv-python numpy scipy pupil-apriltags
```

## File Structure
- `combat_game.py` — Main game loop and UI
- `symbol_recognition.py` — Symbol recognition logic and templates
- `README.md` — This file

## Notes
- You need a webcam and a printed AprilTag (tag36h11 family recommended).
- You can generate AprilTags at [AprilTag Generator](https://apriltag.csail.mit.edu/).

Enjoy battling with symbols! 