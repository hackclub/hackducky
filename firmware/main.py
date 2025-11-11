# NOT IMPLEMENTED: BUTTON, ATTACKMODE, LED, $_RANDOM_MIN, $_RANDOM_MAX

import digitalio
import board

print("Main.py: Starting up...")
# Setup LED
status_led = digitalio.DigitalInOut(board.LED)
status_led.direction = digitalio.Direction.OUTPUT


def flash_error():
    while True:
        status_led.value = True
        time.sleep(0.1)
        status_led.value = False
        time.sleep(0.1)


import adafruit_logging as logging
from adafruit_logging import FileHandler

logger = logging.getLogger("compiler.py")
logger.setLevel(logging.DEBUG)
programming_mode = True

try:
    LOG_FILE_PATH = "/debug.log"
    filehandler = FileHandler(LOG_FILE_PATH)
    logger.addHandler(filehandler)
    import adafruit_datetime as datetime

    logger.info(f"BOOT {datetime.datetime.now()}")
    programming_mode = False
except:
    print("Debug mode active...")
    print("Logging to file is disabled.")


try:
    import time
    import usb_hid
    import os
    import random as rand
    from random_keystrokes import RANDOM_KEYSTROKES

    MODIFIER_KEYS = ["CTRL", "SHIFT", "ALT", "GUI", "WINDOWS", "COMMAND", "CONTROL"]

    SPECIAL_KEYS = [
        "ENTER",
        "DELETE",
        "ESCAPE",
        "UP_ARROW",
        "DOWN_ARROW",
        "LEFT_ARROW",
        "RIGHT_ARROW",
        "BACKSPACE",
        "SPACE",
        "TAB",
        "MENU",
        "APPLICATION",
        "PRINT_SCREEN",
        "PAUSE",
        "INSERT",
        "DELETE",
        "PAGE_DOWN",
        "PAGE_UP",
        "HOME",
        "END",
        "F1",
        "F2",
        "F3",
        "F4",
        "F5",
        "F6",
        "F7",
        "F8",
        "F9",
        "F10",
        "F11",
        "F12",
        "CAPS_LOCK",
        "NUML_OCK",
        "SCROLL_LOCK",
    ]

    class DuckyScriptError(Exception):
        pass

    # For programnubg mode
    # ================================================================
    class PseudoKeyboard:
        def press(self, a):
            pass

        def release_all(self):
            pass

    class PseudoLayout:
        def write(self, a):
            pass

    class PseudoKeycode:
        pass

    if programming_mode:

        def getattr(o, s):
            return s

    # ================================================================

    class DuckyScriptCompiler:
        def __init__(self, layout, keyboard, keycode) -> None:
            self.layout = layout
            self.keyboard = keyboard
            self.keycode = keycode
            self.default_delay = 20
            self.var_table: dict[str, int | bool] = {}
            self.const_table: dict[str, int | str] = {}
            self.if_condition_stack: list[bool] = []
            self.function_table: dict[str, list] = {}
            self.call_stack: list = []  # Track function calls for return values
            self.return_value: int | bool | None = (
                None  # Store the most recent return value
            )
            self.var_table["$_RANDOM_MIN"] = 0
            self.var_table["$_RANDOM_MAX"] = 9

            # If debug mode is active, then we should still send debug messages but not do anything.
            if programming_mode:
                self.layout = PseudoLayout()
                self.keyboard = PseudoKeyboard()
                self.keycode = PseudoKeycode()

        def sanitise(self, lines: list[str]) -> list[str]:
            """Sanitises raw duckyscript to remove comments and whitespace."""
            sanitised: list[str] = []

            iterator = iter(lines)
            for line in iterator:
                line = line.strip()

                if not line:
                    continue

                if line.startswith("REM_BLOCK"):
                    try:
                        while not next(iterator).startswith("END_REM"):
                            pass
                    except StopIteration:
                        raise DuckyScriptError(
                            "A REM_BLOCK was started but no END_REM was found."
                        )

                if line.startswith("REM"):
                    continue

                sanitised.append(line)

            return sanitised

        def compile(self, lines: list[str]) -> list:
            """Accepts duckyscript, then builds a list of functions to call in order."""
            # First pass: sanitise
            lines = self.sanitise(lines)
            # logger.debug(f"{lines}")
            # Second pass: generate constants table
            lines = self.generate_constants(lines)
            # logger.debug(f"{lines}")
            # Third pass: replace the constants
            lines = self.replace_constants(lines)
            # logger.debug(f"{lines}")
            lines = self.replace_random(lines)
            # logger.debug(f"{lines}")

            compiled_funcs = self._compile_block(lines)

            if self.if_condition_stack:
                raise DuckyScriptError(
                    "Reached end of file with unclosed IF statement(s)."
                )

            return compiled_funcs

        def _compile_block(self, lines: list[str]) -> list:
            out: list = []

            iterator = iter(lines)
            row = 0  # Track the row for reporting errs.
            for line in iterator:
                row += 1
                line = line.split()
                command = line[0]

                if command == "FUNCTION":
                    func_name = line[1] if len(line) > 1 else ""

                    # Validate function name
                    if not func_name.endswith("()") or not self._is_valid_function_name(
                        func_name
                    ):
                        raise DuckyScriptError(f"Invalid function name: {func_name}")

                    # Extract function body
                    func_body_lines = []
                    nesting_level = 1
                    for func_line in iterator:
                        stripped_line = func_line.strip()
                        if stripped_line.startswith("FUNCTION"):
                            nesting_level += 1
                        elif stripped_line == "END_FUNCTION":
                            nesting_level -= 1

                        if nesting_level == 0:
                            break

                        func_body_lines.append(func_line)
                    else:
                        raise DuckyScriptError(
                            f"FUNCTION {func_name} was not closed with END_FUNCTION."
                        )

                    # Store the function definition
                    self.function_table[func_name] = func_body_lines
                    logger.debug(f"Defined function: {func_name}")
                    continue

                # Handle function calls
                elif command.endswith("()") and command in self.function_table:
                    func_name = command
                    out.append(lambda fn=func_name: self._execute_function(fn))
                    continue

                # Handle RETURN statement
                elif command == "RETURN":
                    if len(line) > 1:
                        # Evaluate return expression
                        return_tokens = line[1:]
                        return_value = self.evaluate_expression(return_tokens)
                        out.append(lambda rv=return_value: self._do_return(rv))
                    else:
                        out.append(lambda: self._do_return(None))
                    continue

                if command == "WHILE":
                    # We are already inside a block that should be executed, so we compile the loop.
                    condition_tokens = line[1:]

                    # Gather all lines that form the body of the loop
                    loop_body_lines = []
                    nesting_level = 1
                    for loop_line in iterator:
                        if loop_line.strip().startswith("WHILE"):
                            nesting_level += 1
                        elif loop_line.strip() == "END_WHILE":
                            nesting_level -= 1

                        if nesting_level == 0:
                            break  # We found the matching END_WHILE

                        loop_body_lines.append(loop_line)
                    else:
                        # If not broken out of
                        raise DuckyScriptError(
                            "WHILE statement was not closed with END_WHILE."
                        )

                    compiled_loop_body = self._compile_block(loop_body_lines)

                    # Create a single function that runs the entire loop
                    loop_func = (
                        lambda ct=condition_tokens,
                        body=compiled_loop_body: self._execute_while_loop(ct, body)
                    )
                    out.append(loop_func)
                    continue

                # Check if blocks
                if command == "IF":
                    condition_result = self._evaluate_condition(line[1:])
                    self.if_condition_stack.append(condition_result)
                    logger.debug(
                        f"IF condition '{' '.join(line[1:])}' evaluated to {condition_result}. Stack: {self.if_condition_stack}"
                    )
                    continue

                elif command == "ELSE":
                    if not self.if_condition_stack:
                        raise DuckyScriptError(
                            f"ELSE found without a preceding IF at line {row}"
                        )
                    # Invert the condition for the current block
                    self.if_condition_stack[-1] = not self.if_condition_stack[-1]
                    logger.debug(
                        f"ELSE found. Inverting condition. Stack: {self.if_condition_stack}"
                    )
                    continue

                elif command == "END_IF":
                    if not self.if_condition_stack:
                        raise DuckyScriptError(
                            f"END_IF found without a preceding IF at line {row}"
                        )
                    _ = self.if_condition_stack.pop()
                    logger.debug(
                        f"END_IF found. Popped from stack. Stack: {self.if_condition_stack}"
                    )
                    continue

                should_execute = all(self.if_condition_stack)
                if not should_execute:
                    logger.debug(f"Skipping line {row} due to false condition.")
                    continue

                # Normal keyword / commands idk
                if command == "STRING":
                    logger.debug(f"Processing STRING statement at row {row} , {line}")
                    if len(line) >= 2:
                        s = " ".join(line[1:])
                        out.append(lambda s=s: self.string(s))
                    else:
                        logger.debug("STRING block found,")
                        string: list[str] = []
                        n = next(iterator)
                        while n != "END_STRING":
                            string.append(n)
                            n = next(iterator)
                        s = "".join(string)
                        logger.debug(f"END STRING block with value {s}")
                        out.append(lambda s=s: self.string(s))

                if command == "STRINGLN":
                    logger.debug(f"Processing STRINGLN statement at row {row} , {line}")
                    if len(line) >= 2:
                        s = " ".join(line[1:])
                        out.append(lambda s=s: self.stringln(s))
                    else:
                        logger.debug("STRINGLN block found,")
                        string: list[str] = []
                        n = next(iterator)
                        while n != "END_STRINGLN":
                            out.append(lambda s=n: self.stringln(s))
                            n = next(iterator)
                        logger.debug("END STRINGLN block with value")

                elif command == "DELAY":
                    if len(line) > 1:
                        try:
                            val = self.get_value(line[1])
                            if type(val) != int:
                                raise DuckyScriptError(f"Invalid integer {val}")
                            out.append(lambda t=val: self.delay(t))
                        except ValueError:
                            raise DuckyScriptError(
                                f"Invalid integer found at line {row}"
                            )
                    else:
                        out.append(lambda t=self.default_delay: self.delay(t))

                elif command in MODIFIER_KEYS or command in SPECIAL_KEYS:
                    keys = line
                    out.append(lambda k=keys: self.do_key(k))

                elif command == "INJECT_MOD":
                    key = line[1]
                    out.append(lambda k=key: self.do_key(k))

                elif command == "DEFAULT_DELAY":
                    try:
                        val = self.get_value(line[1])
                        if type(val) != int:
                            raise DuckyScriptError(f"Invalid integer {val}")
                        out.append(lambda t=val: self.default_delay)
                    except IndexError as e:
                        raise DuckyScriptError(e)

                elif command == "VAR":
                    logger.debug(f"Processing VAR statement, {line}")
                    try:
                        var_name, value_str = line[1], line[3]
                        var_name = var_name.strip()
                        if not var_name.startswith("$"):
                            raise DuckyScriptError(
                                f"Invalid variable name: '{var_name}'"
                            )
                        elif var_name in self.var_table:
                            raise DuckyScriptError(
                                f"Attempted to redefine existing variable '{var_name}'"
                            )

                        value_tokens = value_str.strip().split()
                        self.var_table[var_name] = self.evaluate_expression(
                            value_tokens
                        )
                        logger.debug(
                            f"Defined variable {var_name} = {self.var_table[var_name]}"
                        )
                    except ValueError:
                        raise DuckyScriptError(f"Invalid VAR syntax: {line}")

                elif command.startswith("$"):
                    out.append(lambda l=line: self.reassign(l))

            return out

        def generate_constants(self, lines: list[str]) -> list[str]:
            # Use this on pass 1
            """
            Process DuckyScript to add constants.

            :param list[str] lines: sanitised duckyscript source
            :return: duckyscript with constant definitions removed
            :rtype: list[str]
            """
            out: list[str] = []
            row = 0
            for line in lines:
                row += 1
                line = line.split()
                if line[0] == "DEFINE":
                    logger.debug("DEFINE statement found.")
                    if len(line) < 3:
                        raise DuckyScriptError(
                            f"Error while trying to define a constant in line {row}: {' '.join(line)}"
                        )
                    try:
                        self.const_table[line[1]] = int(" ".join(line[2:]))
                        logger.debug(f"Added {line[1]} to constant table as int.")
                    except:
                        self.const_table[line[1]] = " ".join(line[2:])
                        logger.debug(f"Added {line[1]} to constant table as str.")
                else:
                    out.append(" ".join(line))
            return out

        def replace_constants(self, lines: list[str]) -> list[str]:
            """Replaces all constant names with their value"""
            out: list[str] = []
            row = 0
            for line in lines:
                row += 1
                line = line.split()
                for i in range(len(line)):
                    if self.const_table.get(line[i]):
                        logger.debug(
                            f"Replaced {line[i]} with {self.const_table[line[i]]} at row {row}"
                        )
                        line[i] = str(self.const_table[line[i]])
                out.append(" ".join(line))
            return out

        def replace_random(self, lines: list[str]) -> list[str]:
            out: list[str] = []
            row = 0
            for line in lines:
                row += 1
                line = line.split()
                for i in range(len(line)):
                    if line[i] in RANDOM_KEYSTROKES:
                        random = RANDOM_KEYSTROKES[line[i]]()
                        logger.debug(f"Replaced {line[i]} with {random} at row {row}")
                        line[i] = random
                out.append(" ".join(line))
            return out

        def get_value(self, token: str) -> int | bool | None:
            """Resolves a token into its value, handling function calls."""
            token = token.strip()

            # Check for function call first
            if token.endswith("()") and token in self.function_table:
                return self.evaluate_function_call(token)

            # Then check for variables
            if token.startswith("$") and token in self.var_table:
                return self.var_table[token]
            elif token == "$_RANDOM_INT":
                print(self.var_table["$_RANDOM_MIN"], self.var_table["$_RANDOM_MAX"])
                return rand.randint(
                    self.var_table["$_RANDOM_MIN"], self.var_table["$_RANDOM_MAX"]
                )

            # Then check for literals
            if token.upper() == "TRUE":
                return True
            if token.upper() == "FALSE":
                return False
            if token.upper() == "NONE":
                return None

            try:
                return int(token)
            except ValueError:
                raise DuckyScriptError(
                    f"Invalid value: {token}. Must be variable, function call, or literal (int/bool)."
                )

        def evaluate_expression(self, tokens: list[str]) -> int | bool | None:
            """Evaluates expressions, including function calls."""

            if len(tokens) == 1:
                token = tokens[0]
                # Check if it's a function call
                if token.endswith("()") and token in self.function_table:
                    return self.evaluate_function_call(token)
                else:
                    return self.get_value(token)

            left_val = self.evaluate_expression([tokens[0]])
            op = tokens[1]
            right_val = self.evaluate_expression([tokens[2]])

            if isinstance(left_val, (int, bool)) and isinstance(right_val, (int, bool)):
                if op == "+":
                    return left_val + right_val
                elif op == "-":
                    return left_val - right_val
                elif op == "*":
                    return left_val * right_val
                elif op == "/":
                    return left_val // right_val
                elif op == "==":
                    return left_val == right_val
                elif op == "!=":
                    return left_val != right_val
                elif op == ">":
                    return left_val > right_val
                elif op == "<":
                    return left_val < right_val
                elif op == ">=":
                    return left_val >= right_val
                elif op == "<=":
                    return left_val <= right_val

            raise DuckyScriptError(f"Invalid operation: {left_val} {op} {right_val}")

        def _evaluate_condition(self, tokens: list[str]) -> bool:
            """Evaluates conditional expressions, including function calls."""
            result = self.evaluate_expression(tokens)
            if isinstance(result, bool):
                return result
            raise DuckyScriptError(f"Condition must evaluate to boolean, got: {result}")

        def evaluate_function_call(self, func_name: str) -> int | bool | None:
            """Evaluate a function call as part of an expression."""
            self._execute_function(func_name)
            return self.return_value

        def _execute_while_loop(
            self, condition_tokens: list[str], loop_functions: list
        ):
            """
            At runtime, repeatedly evaluates the condition and executes the loop body.
            """
            logger.debug(
                f"Executing WHILE loop with condition: {' '.join(condition_tokens)}"
            )
            # Safety break to prevent accidental infinite loops during testing/dev
            max_iterations = 1000
            iterations = 0

            while self._evaluate_condition(condition_tokens):
                if iterations >= max_iterations:
                    logger.error(
                        "WHILE loop exceeded max iterations. Breaking to prevent freeze."
                    )
                    break

                for func in loop_functions:
                    func()  # Execute one full cycle of the loop body
                iterations += 1
            logger.debug("WHILE loop finished.")

        def _is_valid_function_name(self, name: str) -> bool:
            """Validate function name."""
            if not name.endswith("()"):
                return False

            base_name = name[:-2]  # Remove "()"

            # Check if starts with number
            if base_name[0].isdigit():
                return False

            # Check for valid characters (letters, numbers, underscore)
            if not all(c.isalpha() or c.isnumeric() or c == "_" for c in base_name):
                return False

            # Check for reserved keywords
            reserved_keywords = (
                MODIFIER_KEYS
                + SPECIAL_KEYS
                + [
                    "ATTACKMODE",
                    "STRING",
                    "DELAY",
                    "DEFAULT_DELAY",
                    "VAR",
                    "DEFINE",
                    "IF",
                    "ELSE",
                    "END_IF",
                    "WHILE",
                    "END_WHILE",
                    "FUNCTION",
                    "END_FUNCTION",
                    "RETURN",
                    "REM",
                    "REM_BLOCK",
                    "END_REM",
                ]
            )

            if base_name.upper() in reserved_keywords:
                return False

            return True

        def _execute_function(self, func_name: str):
            """Execute a function by name."""
            logger.debug(f"Calling function: {func_name}")

            if func_name not in self.function_table:
                raise DuckyScriptError(f"Undefined function: {func_name}")

            # Save current state
            current_if_stack = self.if_condition_stack.copy()

            try:
                # Reset return value for this call
                self.return_value = None

                # Compile and execute function body
                func_body = self.function_table[func_name]
                compiled_func = self._compile_block(func_body)

                # Execute function
                for func in compiled_func:
                    if self.return_value is not None:
                        break  # Early return if RETURN was called
                    func()

            finally:
                # Restore state
                self.if_condition_stack = current_if_stack

            logger.debug(
                f"Function {func_name} finished with return value: {self.return_value}"
            )

        def string(self, s: str) -> None:
            logger.debug(f"Writing {s} with HID device.")
            self.layout.write(s)

        def stringln(self, s: str) -> None:
            logger.debug(f"Writing {s} with HID device.")
            self.layout.write(s + "\n")

        def do_key(self, keys: str | list[str]) -> None:
            logger.debug(f"Sending the {keys} keys.")
            try:
                if type(keys) == str:
                    keys = keys.upper()
                    if keys == "CTRL":
                        keys = "CONTROL"
                    self.keyboard.press(getattr(self.keycode, keys))
                else:
                    for key in keys:
                        key = key.upper()
                        if key == "CTRL":
                            key = "CONTROL"
                        self.keyboard.press(getattr(self.keycode, key))
                        time.sleep(0.1)
                self.keyboard.release_all()
            except AttributeError:
                raise DuckyScriptError("Unknown key found.")

        def delay(self, t: int):
            logger.debug(f"Sleeping for {t}ms")
            time.sleep(t / 1000)

        def set_default_delay(self, t: int):
            self.default_delay = t

        def reassign(self, line: list[str]):
            var_name = line[0]
            if var_name not in self.var_table:
                raise DuckyScriptError(f"Undefined variable '{var_name}'")

            if len(line) > 2 and line[1] == "=":
                value_tokens = line[2:]
                self.var_table[var_name] = self.evaluate_expression(value_tokens)
                logger.debug(
                    f"Reassigned variable {var_name} = {self.var_table[var_name]}"
                )
            else:
                raise DuckyScriptError(f"Invalid syntax for variable usage: {line}")

        def _do_return(self, value: int | bool | None):
            """Handle RETURN statement."""
            self.return_value = value
            logger.debug(f"RETURN statement called with value: {value}")

        def run(self, filename: str):
            with open(filename, "r") as f:
                lines = f.readlines()

            exec = self.compile(lines)
            for func in exec:
                func()

    def main():
        # Initialize keyboard right away if we're in payload mode
        try:
            print("Main.py: Checking USB HID devices...")
            if not usb_hid.devices:
                print("Main.py: No USB HID devices found!")
                flash_error()
            else:
                from layouts_manager import layouts, kbd, keycodes

            print(f"Main.py: Found {len(usb_hid.devices)} HID devices")
            print("Main.py: Keyboard initialized successfully")

            # Test keyboard initialization
            kbd.release_all()
            print("Main.py: Keyboard test successful")

        except Exception as e:
            print(f"Main.py: Failed to initialize keyboard: {str(e)}")
            flash_error()

        compiler = DuckyScriptCompiler(layouts["us"], kbd, keycodes["us"])
        files = os.listdir("/ducks")
        ducky_files = sorted(["/ducks/" + f for f in files if f.endswith(".ducky")])
        if ducky_files:
            compiler.run(ducky_files[0])

    if __name__ == "__main__":
        main()

except Exception as e:
    logger.error(f"{e}")
    flash_error()
