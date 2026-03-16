# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
- List at least two concrete bugs you noticed at the start  
  (for example: "the secret number kept changing" or "the hints were backwards").
  - the hints were backwards
  - the bounds defined for the difficulty modes were not reflected correctly
  - when show hint was turned off, there was no way for the user to confirm that guesses were registered
  - scores were not reflected accurately
  - attempts were not reflected accurately
  - history wasn't registering correctly, or submit guess button wasnt registering all the guesses

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
  - I used Claude
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
  - When I first read `check_guess` in `logic_utils.py`, I suspected the hint messages were swapped. I asked Claude to review the logic, and it confirmed: the branch `guess > secret` was returning `"Too Low"` and saying `"Go HIGHER!"` — the exact opposite of what it should say. Claude suggested flipping the return values so that `guess > secret` returns `"Too Low"` with `"Go LOWER!"` and the `else` branch returns `"Too High"` with `"Go HIGHER!"`. I verified this by running the game in Streamlit, entering a number I knew was above the secret (visible in the Developer Debug Info expander), and confirming the hint now correctly said "Go LOWER!"
- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).
  - When fixing the win-score display bug, Claude initially suggested reading `st.session_state.score` directly inside the win banner message, assuming it would already hold the updated value. This was misleading — because `update_score` returns a new value that only gets written back to `st.session_state.score` on the next line, reading from `st.session_state.score` in the same render pass still showed the old (stale) score. I caught this by deliberately winning on the first guess and noticing the banner printed a score that was 90 points lower than expected. The fix was to store the return value in a local variable `new_score` and use that in the banner instead of `st.session_state.score`.

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
  - I used both pytest and visual confirmation on the streamlit website.
- Describe at least one test you ran (manual or using pytest)
  and what it showed you about your code.
  - I ran the pytest suite in `tests/test_game_logic.py`. The test `test_guess_too_high_says_go_lower` called `check_guess(80, 50)` and asserted that the outcome was `"Too Low"` and the message contained `"LOWER"`. Before the fix, this test failed because the original code returned `"Too Low"` with the message `"Go HIGHER!"` — confirming the swapped hint bug. Once I corrected the return values in `check_guess`, the test passed. Running the full suite also caught that `test_float_returns_error` failed against the original `parse_guess`, which silently accepted `"3.14"` by casting it to `3`, revealing a second input-validation bug I then fixed.
- Did AI help you design or understand any tests? How?
  - Yes AI did help me with the test designs. It gave me the initial tests and through working on the changes on the website we kept designing new tests for each change.

---

## 4. What did you learn about Streamlit and state?

- In your own words, explain why the secret number kept changing in the original app.
  - Every time I clicked a button or typed anything, Streamlit reran the entire Python script, which made the secret number changes everytime.
- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?
  - Streamlit reruns your entire script every time the user does anything. Session state is a way to save values so they survive those reruns instead of resetting.
- What change did you make that finally gave the game a stable secret number?
  - Wrapping it in if "secret" not in st.session_state so a new number only gets picked once, not on every rerun.

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
    - The human involvement in the process of prompting AI. I really liked how claude always kept me in the loop, which enabled me not only to check but also learn from the code (from the rights and wrongs it does).
- What is one thing you would do differently next time you work with AI on a coding task?
  - Write unit tests first to have a rough idea of expectations I have.
- In one or two sentences, describe how this project changed the way you think about AI generated code.
  - I used to assume AI code was mostly correct. After this project I know it can introduce subtle bugs that look right but aren't, so I treat it as a starting point that still needs to be verified.
