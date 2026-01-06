class BowlingGame:
    MAX_FRAMES = 10
    PINS_PER_FRAME = 10

    def __init__(self, game_str: str):
        """
        Initializes the bowling game and parses the input string.
        """
        if not game_str or not game_str.strip():
            raise ValueError("Game string cannot be empty.")
        
        # convert to uppercase and remove all whitespace
        self.game_str = game_str.upper().replace(" ", "")
        self.rolls = self._parse_rolls(self.game_str)

    def _parse_rolls(self, s: str) -> list[int]:
        """
        Converts the game string into a list of integer pinfalls with enhanced validation.
        """
        rolls = []
        # Track frame logic during parsing to validate mid-frame totals
        current_frame = 1
        first_roll_in_frame = True

        for i, char in enumerate(s):
            if char == 'X':
                # Strike: 10 pins
                rolls.append(self.PINS_PER_FRAME)
                if current_frame < self.MAX_FRAMES:
                    # Non-10th frame strikes end the frame immediately
                    first_roll_in_frame = True
                    current_frame += 1
                else:
                    # In 10th frame, 'X' is just a roll; frame ends after 3 rolls or 2 non-strikes
                    first_roll_in_frame = False 

            elif char == '-':
                # Miss: 0 pins
                rolls.append(0)
                self._update_frame_state(current_frame, first_roll_in_frame)
                first_roll_in_frame = not first_roll_in_frame
                if first_roll_in_frame: current_frame += 1

            elif char == '/':
                # Spare logic: Must follow a numeric roll (0-9)
                if not rolls or s[i-1] == 'X' or s[i-1] == '-':
                    # Note: '-' is technically 0, but usually notation uses '0/' not '-/' 
                    # for clarity; however, your requirement allows '-'.
                    if not rolls or s[i-1] == 'X':
                         raise ValueError("Spare '/' must follow a numeric roll (0-9).")
                
                rolls.append(self.PINS_PER_FRAME - rolls[-1])
                
                if current_frame < self.MAX_FRAMES:
                    first_roll_in_frame = True
                    current_frame += 1
                else:
                    first_roll_in_frame = False

            elif char.isdigit():
                val = int(char)
                if val >= self.PINS_PER_FRAME:
                    raise ValueError(f"Digit {val} must be less than {self.PINS_PER_FRAME}.")
                
                #Check if two rolls in a frame exceed 10 pins (Fail-Fast)
                if not first_roll_in_frame and current_frame <= self.MAX_FRAMES:
                    if (rolls[-1] + val) > self.PINS_PER_FRAME and s[i-1] != 'X':
                        raise ValueError(f"Frame {current_frame} exceeds {self.PINS_PER_FRAME} pins.")
                
                rolls.append(val)
                first_roll_in_frame = not first_roll_in_frame
                if first_roll_in_frame: current_frame += 1
            else:
                raise ValueError(f"Invalid character in game string: {char}")
                
        return rolls

    def _update_frame_state(self, current_frame, first_roll):
        # Helper to manage frame transitions if needed for complex validation
        pass

    def calculate_score(self) -> int:
        """
        Calculates the total score based on ten-pin bowling rules.
        """
        total_score = 0
        roll_idx = 0
        
        for frame in range(1, self.MAX_FRAMES + 1):
            if roll_idx >= len(self.rolls):
                raise ValueError("Incomplete game: Missing required rolls.")

            # STRIKE logic
            if self.rolls[roll_idx] == self.PINS_PER_FRAME:
                total_score += self._get_strike_score(roll_idx)
                roll_idx += 1
                if frame == self.MAX_FRAMES:
                    roll_idx += 2 # Consume 10th frame bonuses
            
            # SPARE logic
            elif self._is_spare(roll_idx):
                total_score += self.PINS_PER_FRAME + self._get_roll_safe(roll_idx + 2)
                roll_idx += 2
                if frame == self.MAX_FRAMES:
                    roll_idx += 1 # Consume 10th frame bonus
            
            # OPEN FRAME logic
            else:
                total_score += self.rolls[roll_idx] + self.rolls[roll_idx + 1]
                roll_idx += 2
        
        # Strict validation for extra rolls
        if roll_idx < len(self.rolls):
            raise ValueError(f"Trailing data: Found {len(self.rolls) - roll_idx} extra roll(s).")
            
        return total_score

    def _is_spare(self, idx: int) -> bool:
        if idx + 1 >= len(self.rolls): return False
        return self.rolls[idx] + self.rolls[idx+1] == self.PINS_PER_FRAME

    def _get_strike_score(self, idx: int) -> int:
        return self.PINS_PER_FRAME + self._get_roll_safe(idx + 1) + self._get_roll_safe(idx + 2)

    def _get_roll_safe(self, idx: int) -> int:
        if idx >= len(self.rolls):
            raise ValueError("Incomplete game: Missing bonus rolls.")
        return self.rolls[idx]

def calculate_score(game_str: str) -> int:
    return BowlingGame(game_str).calculate_score()