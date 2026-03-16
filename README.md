# 🎮 Game Glitch Investigator: The Impossible Guesser

## 🚨 The Situation

You asked an AI to build a simple "Number Guessing Game" using Streamlit.
It wrote the code, ran away, and now the game is unplayable.

- You can't win.
- The hints lie to you.
- The secret number seems to have commitment issues.

## 🛠️ Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run the broken app: `python -m streamlit run app.py`

## 🕵️‍♂️ Your Mission

1. **Play the game.** Open the "Developer Debug Info" tab in the app to see the secret number. Try to win.
2. **Find the State Bug.** Why does the secret number change every time you click "Submit"? Ask ChatGPT: _"How do I keep a variable from resetting in Streamlit when I click a button?"_
3. **Fix the Logic.** The hints ("Higher/Lower") are wrong. Fix them.
4. **Refactor & Test.** - Move the logic into `logic_utils.py`.
   - Run `pytest` in your terminal.
   - Keep fixing until all tests pass!

## 📝 Document Your Experience

- [x] Describe the game's purpose.
  - A number guessing game where the player picks a difficulty, then guesses a secret number within a limited number of attempts. The game gives higher/lower hints and tracks a score that goes up for winning early and down for wrong guesses.
- [x] Detail which bugs you found.
  - The secret number changed on every button click
  - The hints were backwards, guessing too high said "Go HIGHER!" and vice versa
  - The Hard difficulty range was easier than Normal (1–50 instead of 1–200)
  - Attempts started at 1 instead of 0, wasting one attempt before the game began
  - The win banner showed the wrong (stale) score because it read from session state before the update was written back
  - With hints off, there was no confirmation that a guess was registered
  - Invalid guesses (floats, empty input) were being accepted or added to history as blank entries
  - New Game didn't reset status or history, and used a hardcoded range of 1–100 ignoring difficulty
- [x] Explain what fixes you applied.
  - Wrapped secret generation in `if "secret" not in st.session_state`
  - Flipped the hint return values in `check_guess`
  - Corrected Hard range to 1–200 in `get_range_for_difficulty`
  - Changed attempts initialization from 1 to 0
  - Stored `update_score` result in a local `new_score` variable and used that in the win banner
  - Added a confirmation message when hints are hidden
  - Added strict whole-number validation in `parse_guess`
  - Fixed New Game to reset status, history, and use the difficulty-based range

## 📸 Demo

- [x] 

## 🚀 Stretch Features

- [x] Challenge 1: Tests
      
