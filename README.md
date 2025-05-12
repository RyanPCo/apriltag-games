# 1. Flappy Tag

A webcam-based game where you control a 'bird' (yellow circle) by moving an AprilTag in front of your camera. Fly through as many pipe gaps as you can—just like Flappy Bird, but with your AprilTag!

## How to Play
- Hold a printed AprilTag (tag36h11 family recommended) in front of your webcam.
- Move the tag up and down to control the bird's vertical position.
- The bird automatically moves forward; avoid hitting the pipes!
- Your score increases each time you pass a pipe.
- If you hit a pipe, the game ends and your score is displayed.
- Press **'q'** to quit at any time.

## Requirements
- Python 3.7+
- OpenCV (`opencv-python`)
- NumPy
- pupil_apriltags

Install dependencies with:
```
pip install opencv-python numpy pupil-apriltags
```

## Notes
- You need a webcam and a printed AprilTag (tag36h11 family recommended).
- You can generate AprilTags at [AprilTag Generator](https://apriltag.csail.mit.edu/).

---

# 2. PokeTag (Turn-Based Combat Game)

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
- `poke-tag.py` — Main game loop and UI
- `symbol_recognition.py` — Symbol recognition logic and templates

## Notes
- You need a webcam and a printed AprilTag (tag36h11 family recommended).
- You can generate AprilTags at [AprilTag Generator](https://apriltag.csail.mit.edu/).

Enjoy battling with symbols! 