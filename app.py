import random
import streamlit as st
from logic_utils import check_guess, get_range_for_difficulty, parse_guess, update_score

st.set_page_config(page_title="Glitchy Guesser", page_icon="🎮")

st.title("🎮 Game Glitch Investigator")
st.caption("An AI-generated guessing game. Something is off.")

st.sidebar.header("Settings")

difficulty = st.sidebar.selectbox(
    "Difficulty",
    ["Easy", "Normal", "Hard"],
    index=1,
)

attempt_limit_map = {
    "Easy": 6,
    "Normal": 8,
    "Hard": 5,
}
attempt_limit = attempt_limit_map[difficulty]

low, high = get_range_for_difficulty(difficulty)

st.sidebar.caption(f"Range: {low} to {high}")
st.sidebar.caption(f"Attempts allowed: {attempt_limit}")

if "secret" not in st.session_state:
    st.session_state.secret = random.randint(low, high)

# FIX: attempts initialized to 1, wasting one attempt before the game started. Fixed to 0 with Claude Code.
if "attempts" not in st.session_state:
    st.session_state.attempts = 0

if "score" not in st.session_state:
    st.session_state.score = 0

if "status" not in st.session_state:
    st.session_state.status = "playing"

if "history" not in st.session_state:
    st.session_state.history = []

# FIX: Added clear_count to support resetting the text input field without a full page reload. Added with Claude Code.
if "clear_count" not in st.session_state:
    st.session_state.clear_count = 0

st.subheader("Make a guess")

# FIX: Info box was hardcoded to "1 to 100". Updated to use dynamic low/high from difficulty. Fixed with Claude Code.
# FIX: Added live score metric next to the info box so users always see their running score. Added with Claude Code.
col_info, col_score = st.columns([3, 1])
with col_info:
    st.info(
        f"Guess a number between {low} and {high}. "
        f"Attempts left: {attempt_limit - st.session_state.attempts}"
    )
with col_score:
    st.metric("Score", st.session_state.score)

with st.expander("Developer Debug Info"):
    st.write("Secret:", st.session_state.secret)
    st.write("Attempts:", st.session_state.attempts)
    st.write("Score:", st.session_state.score)
    st.write("Difficulty:", difficulty)
    st.write("History:", st.session_state.history)

# FIX: Input key now includes clear_count so clicking "Clear" forces a fresh empty input. Added with Claude Code.
raw_guess = st.text_input(
    "Enter your guess:",
    key=f"guess_input_{difficulty}_{st.session_state.clear_count}"
)

col1, col2, col3, col4 = st.columns(4)
with col1:
    submit = st.button("Submit Guess 🚀")
with col2:
    new_game = st.button("New Game 🔁")
with col3:
    # FIX: Added Clear button so users can easily reset the input field. Added with Claude Code.
    clear_guess = st.button("Clear ✖")
with col4:
    show_hint = st.checkbox("Show hint", value=True)

# FIX: New Game didn't reset status or history, and used hardcoded randint(1,100) ignoring difficulty range. Fixed with Claude Code.
if new_game:
    st.session_state.attempts = 0
    st.session_state.secret = random.randint(low, high)
    st.session_state.status = "playing"
    st.session_state.history = []
    st.session_state.clear_count += 1
    st.success("New game started.")
    st.rerun()

if clear_guess:
    st.session_state.clear_count += 1
    st.rerun()

if st.session_state.status != "playing":
    if st.session_state.status == "won":
        st.success("You already won. Start a new game to play again.")
    else:
        st.error("Game over. Start a new game to try again.")
    st.stop()

if submit:
    st.session_state.attempts += 1

    ok, guess_int, err = parse_guess(raw_guess)

    if not ok:
        st.error(err)
    else:
        # FIX: Invalid guesses were being appended to history as blank entries, causing gaps. Fixed with Claude Code.
        st.session_state.history.append(guess_int)

        secret = st.session_state.secret

        outcome, message = check_guess(guess_int, secret)

        # FIX: When hints are hidden, users had no feedback that their guess was registered. Added confirmation message with Claude Code.
        if show_hint:
            st.warning(message)
        else:
            st.info(f"Guess {guess_int} registered. Keep going!")

        # FIX: Win banner read st.session_state.score before it was reliably updated in the same render pass.
        # Switched to using new_score local variable to guarantee correct value. Fixed with Claude Code.
        new_score = update_score(
            current_score=st.session_state.score,
            outcome=outcome,
            attempt_number=st.session_state.attempts,
        )
        st.session_state.score = new_score

        if outcome == "Win":
            st.balloons()
            st.session_state.status = "won"
            st.success(
                f"You won! The secret was {st.session_state.secret}. "
                f"Final score: {new_score}"
            )
        else:
            if st.session_state.attempts >= attempt_limit:
                st.session_state.status = "lost"
                st.error(
                    f"Out of attempts! "
                    f"The secret was {st.session_state.secret}. "
                    f"Score: {st.session_state.score}"
                )

st.divider()
st.caption("Built by an AI that claims this code is production-ready.")
