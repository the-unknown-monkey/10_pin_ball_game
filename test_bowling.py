import pytest
from main import calculate_score

def test_standard_games():
    """Validates the core scoring mechanics for various complete games."""
    # Simple open frames
    assert calculate_score("9-9-9-9-9-9-9-9-9-9-") == 90
    # Perfect game (12 strikes)
    assert calculate_score("XXXXXXXXXXXX") == 300
    # Consecutive spares
    assert calculate_score("5/5/5/5/5/5/5/5/5/5/5") == 150
    # Complex mixed game with strikes and spares
    assert calculate_score("X7/9-X-88/-6X8/X11") == 142

def test_tenth_frame_variations():
    """Specifically targets the complex 3-roll bonus logic of the 10th frame."""
    # Strike followed by two numeric rolls
    assert calculate_score("------------------X52") == 17
    # Spare followed by a strike bonus
    assert calculate_score("------------------5/X") == 20
    # Three strikes in the 10th frame
    assert calculate_score("------------------XXX") == 30

def test_invalid_sequences():
    """Ensures the parser catches physically impossible bowling sequences."""
    # A spare cannot mathematically follow a strike in one frame
    with pytest.raises(ValueError, match="must follow a numeric roll"):
        calculate_score("X/------------------")

def test_frame_exceeds_ten():
    """Validates that a single frame cannot have more than 10 pins."""
    with pytest.raises(ValueError, match="exceeds 10 pins"):
        calculate_score("83------------------")

def test_incomplete_games():
    """Ensures the calculator detects when a game string ends too early."""
    # Missing the mandatory bonus rolls after a 10th frame strike
    with pytest.raises(ValueError, match="Incomplete game"):
        calculate_score("------------------X5")
    
    # Missing several frames entirely
    with pytest.raises(ValueError, match="Incomplete game"):
        calculate_score("XXXXXXXX")

def test_trailing_data_validation():
    """Ensures no extra 'junk' data follows a complete game."""
    # A full game with one extra character at the end
    with pytest.raises(ValueError, match="Trailing data"):
        calculate_score("9-9-9-9-9-9-9-9-9-9-1")
    
    # Perfect game with an extra strike
    with pytest.raises(ValueError, match="Trailing data"):
        calculate_score("XXXXXXXXXXXXX")

def test_input_sanitization():
    """Checks for robustness against messy user formatting."""
    # Handles lowercase 'x' and extra spaces
    assert calculate_score("x x x x x x x x x x x x") == 300

def test_advanced_scoring_scenarios():
    """Edge cases for zero-value spares and specific 10th frame bonus patterns."""
    # Miss followed by a spare (0 + 10)
    assert calculate_score("-/------------------") == 10
    # 10th frame strike followed by a spare bonus (X + 8 + 2)
    assert calculate_score("------------------X8/") == 20
    # All misses
    assert calculate_score("--------------------") == 0

def test_extreme_spare_game():
    """A high-value spare game to check consecutive spare carry-over logic."""
    # 9 pins then a spare every frame, plus a 9 pin bonus
    assert calculate_score("9/9/9/9/9/9/9/9/9/9/9") == 190