
def get_range_for_difficulty(difficulty: str):
    # FIX: Hard was set to 1-50 (easier than Normal). Identified with Claude Code; corrected Hard to 1-200 so ranges scale with difficulty.
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 100
    if difficulty == "Hard":
        return 1, 200
    return 1, 100


def parse_guess(raw: str):
    # FIX: Original allowed floats (e.g. "3.5" → 3) and didn't strip whitespace. Discussed with Claude Code; replaced with strict whole-number validation.
    if raw is None or raw.strip() == "":
        return False, None, "Enter a guess."

    stripped = raw.strip()

    if not stripped.lstrip("-").isdigit():
        return False, None, "Please enter a whole number."

    return True, int(stripped), None


def check_guess(guess, secret):
    # FIX: Hint messages were swapped — guess > secret said "Go HIGHER!" instead of "Go LOWER!". Caught and corrected with Claude Code.
    if guess == secret:
        return "Win", "🎉 Correct!"

    try:
        if guess > secret:
            return "Too Low", "📉 Go LOWER!"
        else:
            return "Too High", "📈 Go HIGHER!"
    except TypeError:
        g = str(guess)
        if g == secret:
            return "Win", "🎉 Correct!"
        if g > secret:
            return "Too High", "📈 Go HIGHER!"
        return "Too Low", "📉 Go LOWER!"


def update_score(current_score: int, outcome: str, attempt_number: int):
    # FIX: "Too High" randomly awarded +5 points on even attempts instead of always deducting.
    # Also, win bonus used (attempt_number + 1) overcounting by one attempt.
    # Both bugs identified and removed with Claude Code.
    if outcome == "Win":
        points = 100 - 10 * attempt_number
        if points < 10:
            points = 10
        return current_score + points

    if outcome in ("Too High", "Too Low"):
        return current_score - 5

    return current_score
