class Calculator:
    def __init__(self):
        self.reset()

    def reset(self):
        self.display = "0"
        self.current_val = None  # The value of the current number being typed or the previous result
        self.operator = None    # The pending operator
        self.is_new_input = True # Flag to indicate if the next number input starts a new calculation
        self.error_state = False # True if "0으로 나눌 수 없습니다" is displayed
        self.buffer = ""        # Current string being typed for the current number

    def _format_display(self, val):
        # Rule 6: Result is rounded to 10 decimal places, and trailing zeros/unnecessary decimal point are removed.
        try:
            f_val = float(val)
            s_val = f"{f_val:.10f}"
            # Remove trailing zeros and unnecessary decimal point
            if "." in s_val:
                s_val = s_val.rstrip('0').rstrip('.')
            return s_val
        except (ValueError, ZeroDivisionError):
            return str(val)

    def press(self, key: str):
        if self.error_state:
            if key == "C":
                self.reset()
            return

        if key == "C":
            self.reset()
            return

        if key == "BS":
            if self.is_new_input:
                # If we just finished a calculation, BS does nothing (Rule 9)
                # Wait, Rule 9 says: "BS는 입력 중인 수의 마지막 글자를 지운다. 한 글자만 남았을 때 누르면 '0'이 된다. 결과가 표시된 상태에서는 아무 일도 하지 않는다."
                # We need a way to distinguish "inputting a number" from "displaying result".
                # Let's refine the state.
                pass
            else:
                if len(self.buffer) <= 1:
                    self.buffer = ""
                    self.display = "0"
                    self.is_new_input = True
                else:
                    self.buffer = self.buffer[:-1]
                    self.display = self.buffer
                    self.is_new_input = False
            
            if self.buffer == "" and not self.is_new_input:
                 self.buffer = "0" # This part is tricky with the current logic
            
            # Let's rethink the state management.
            return

        # ... implementation continues below after rethinking ...
