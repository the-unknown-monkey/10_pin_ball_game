Bowling Game Scoring

Overview
- **Solution:** Implements ten-pin bowling scoring in `main.py` using the `BowlingGame` class and a convenience function `calculate_score(game_str)`.
- **Features:** Parses standard bowling notation (X, /, -, digits), validates frame pin counts, handles 10th-frame bonus rolls, and raises `ValueError` for invalid or incomplete inputs.

Files
- [main.py](main.py): Core implementation with `BowlingGame` and `calculate_score`.
- [test_bowling.py](test_bowling.py): Pytest test suite covering typical, edge, and invalid cases.

Quick Examples
- Evaluate a perfect game (300):

  PowerShell
  ```powershell
  python -c "from main import calculate_score; print(calculate_score('XXXXXXXXXXXX'))"
  ```

- Evaluate a sample string:

  PowerShell
  ```powershell
  python -c "from main import calculate_score; print(calculate_score('9-9-9-9-9-9-9-9-9-9-'))"
  ```

How to run the tests
- Ensure you have `pytest` installed. From the project directory run:

  PowerShell
  ```powershell
  python -m pip install pytest
  pytest test_bowling.py
  ```

Notes about running the code
- The code exposes `calculate_score(game_str)` in `main.py`. You can import and call it from Python or use the `-c` examples above.
- The parser accepts uppercase or lowercase `x` for strikes and ignores spaces in the input string.

Environment
- **Python:** 3.13.11 (my current setup)
- **OS:** Windows 11 (my current setup)

Troubleshooting
- If you see `ValueError: Incomplete game`, the input string does not contain enough rolls (often missing 10th-frame bonus rolls).
- If you see `ValueError: Frame X exceeds 10 pins`, two rolls in a frame sum to more than 10.
- For test failures, run `pytest -q` to see failing assertions and tracebacks.

