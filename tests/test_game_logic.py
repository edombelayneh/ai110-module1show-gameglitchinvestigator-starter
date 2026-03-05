
import sys
import os
from unittest.mock import MagicMock
from logic_utils import check_guess, get_range_for_difficulty, parse_guess, update_score

# Mock streamlit before importing app so the module-level st calls don't fail.
# st.sidebar.selectbox must return a valid difficulty so attempt_limit_map lookup works.
st_mock = MagicMock()
st_mock.sidebar.selectbox.return_value = "Normal"
# session_state needs attribute-style access (like a namespace), not a plain dict
st_mock.session_state = MagicMock()
st_mock.session_state.__contains__ = MagicMock(return_value=True)

# st.columns(n) / st.columns([w1, w2]) must return exactly n MagicMock items
def _columns(arg):
    n = len(arg) if hasattr(arg, "__len__") else int(arg)
    return [MagicMock() for _ in range(n)]

st_mock.columns.side_effect = _columns

# st.stop() raises StopException in real Streamlit; a plain return is fine for mocking
st_mock.stop.side_effect = SystemExit(0)

sys.modules["streamlit"] = st_mock

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    outcome, _ = check_guess(50, 50)
    assert outcome == "Win"

def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too Low"
    outcome, _ = check_guess(60, 50)
    assert outcome == "Too Low"

def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too High"
    outcome, _ = check_guess(40, 50)
    assert outcome == "Too High"

# --- get_range_for_difficulty ---

def test_easy_range():
    assert get_range_for_difficulty("Easy") == (1, 20)

def test_normal_range():
    assert get_range_for_difficulty("Normal") == (1, 100)

def test_hard_range():
    assert get_range_for_difficulty("Hard") == (1, 200)

def test_unknown_difficulty_defaults_to_normal():
    assert get_range_for_difficulty("Extreme") == (1, 100)


# --- parse_guess ---

def test_valid_guess():
    ok, value, err = parse_guess("42")
    assert ok is True
    assert value == 42
    assert err is None

def test_valid_guess_with_whitespace():
    ok, value, err = parse_guess("  7  ")
    assert ok is True
    assert value == 7

def test_empty_string_returns_error():
    ok, value, err = parse_guess("")
    assert ok is False
    assert value is None
    assert err == "Enter a guess."

def test_none_input_returns_error():
    ok, value, err = parse_guess(None)
    assert ok is False
    assert value is None
    assert err == "Enter a guess."

def test_non_numeric_returns_error():
    ok, value, err = parse_guess("abc")
    assert ok is False
    assert value is None
    assert err == "Please enter a whole number."

def test_float_returns_error():
    ok, value, err = parse_guess("3.14")
    assert ok is False
    assert value is None

def test_negative_number_is_valid():
    ok, value, err = parse_guess("-5")
    assert ok is True
    assert value == -5


# --- check_guess ---

def test_correct_guess_returns_win():
    outcome, message = check_guess(50, 50)
    assert outcome == "Win"
    assert "Correct" in message

def test_guess_too_high_says_go_lower():
    # guess > secret => "Too Low" with message "Go LOWER"
    outcome, message = check_guess(80, 50)
    assert outcome == "Too Low"
    assert "LOWER" in message

def test_guess_too_low_says_go_higher():
    # guess < secret => "Too High" with message "Go HIGHER"
    outcome, message = check_guess(20, 50)
    assert outcome == "Too High"
    assert "HIGHER" in message

def test_guess_one_above_secret():
    outcome, _ = check_guess(51, 50)
    assert outcome == "Too Low"

def test_guess_one_below_secret():
    outcome, _ = check_guess(49, 50)
    assert outcome == "Too High"


# --- update_score ---

def test_win_on_first_attempt_gives_90_points():
    # points = 100 - 10*1 = 90
    new_score = update_score(0, "Win", 1)
    assert new_score == 90

def test_win_on_tenth_attempt_gives_minimum_10_points():
    # 100 - 10*10 = 0, clamped to 10
    new_score = update_score(0, "Win", 10)
    assert new_score == 10

def test_win_adds_to_existing_score():
    new_score = update_score(50, "Win", 1)
    assert new_score == 140  # 50 + 90

def test_wrong_guess_deducts_5_for_too_high():
    new_score = update_score(100, "Too High", 1)
    assert new_score == 95

def test_wrong_guess_deducts_5_for_too_low():
    new_score = update_score(100, "Too Low", 1)
    assert new_score == 95

def test_score_does_not_change_for_unknown_outcome():
    new_score = update_score(100, "Unknown", 1)
    assert new_score == 100

def test_score_minimum_clamped_at_10_for_late_win():
    # attempt_number=12: 100 - 120 = -20, clamped to 10
    new_score = update_score(0, "Win", 12)
    assert new_score == 10
