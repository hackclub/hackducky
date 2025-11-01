# HackScript Quick Reference
HackScript is a derivative of Hak5's [DuckyScript](https://docs.hak5.org/hak5-usb-rubber-ducky). However, not all features are supported.

> [!IMPORTANT]
> This reference is up to date with the HackDucky V1.
> Previous versions may not support all features.

# Comments
## REM
The `REM` command does not perform any keystroke injection functions. `REM` gets its name from the word remark. While `REM` may be used to add vertical spacing within a payload, blank lines are also acceptable and will not be processed by the compiler.
```
REM This is a comment
```
## REM_BLOCK
Defining a comment block is simple! Start the comment with `REM_BLOCK` and end the comment with `END_REM`; everything in between will be considered a comment without the need to prepend every new line with `REM`. Comment blocks can be especially useful when you have multiple lines to be included in a single comment or want to retain formatting.
```
REM_BLOCK DOCUMENTATION
        USAGE:
            Place at beginning of payload (besides ATTACKMODE) to act as dynamic
            boot delay

        TARGETS:
            Any system that reflects CAPSLOCK will detect minimum required delay
            Any system that does not reflect CAPSLOCK will hit the max delay of 3000ms
END_REM
```
# Keystroke Injection
## STRING
The `STRING` command keystroke injects (types) a series of keystrokes. `STRING` will automatically interpret uppercase letters by holding the `SHIFT` modifier key where necessary. The `STRING` command will also automatically press the SPACE cursor key, however trailing spaces will be omitted.
```
STRING The quick brown fox jumps over the lazy dog
```
## STRINGLN
The `STRINGLN` command, like `STRING`, will inject a series of keystrokes then terminate with a carriage return (`ENTER`).
```
STRINGLN      _      _      _      USB      _      _      _
STRINGLN   __(.)< __(.)> __(.)=   Hacky   >(.)__ <(.)__ =(.)__
STRINGLN   \___)  \___)  \___)    Ducky    (___/  (___/  (___/
```
## STRING Blocks
### STRING
`STRING` blocks can be used effectively to convert multiple lines into one without needing to prepend each line with `STRING`
> [!CAUTION]
> `STRING` blocks strip leading white space and ignore new lines!
```
STRING
    a
    b
    c
END_STRING
```
is the equivalent of
```
STRING a
STRING b
STRING c
```
Or in this case: `STRING` abc
### STRINGLN
`STRINGLN` blocks can be used like [here-doc](https://en.wikipedia.org/wiki/Here_document); allowing you to inject multiple lines as they are written in the payload. 
> [!CAUTION]
> `STRINGLN` blocks strip the first tab but will preserve all other formatting.
```
STRINGLN
    a
    b
    c
END_STRINGLN
```
is the equivalent of
```
STRINGLN a
STRINGLN b
STRINGLN c
```
## Cursor Keys

The cursor keys are used to navigate the cursor to a different position on the screen.

> ### `UP` `DOWN` `LEFT` `RIGHT`
>  
> ### `PAGE_UP` `PAGE_DOWN` `HOME` `END`
>  
> ### `INSERT` `DELETE` `BACKSPACE`
>  
> ### `TAB`
>  
> ### `SPACE`

## System Keys

System keys are primarily used by the operating system for special functions and may be used to interact with both text areas and navigating the user interface.

> ### `ENTER`
>
> ### `ESCAPE`
>
> ### `PAUSE`
>
> ### `PRINT_SCREEN`
>
> ### `MENU` `APP`
>
> ### `F1` `F2` `F3` `F4` `F5` `F6` `F7` `F8` `F9` `F0` `F11` `F12`

## Basic Modifier Keys

Modifier keys held in combination with another key to perform a special function. Common keyboard combinations for the PC include the familiar `CTRL c` for copy, `CTRL x` for cut, and `CTRL v` for paste.

> ### `SHIFT`
>
> ### `ALT`
>
> ### `CONTROL` or `CTRL`
>
> ### `COMMAND`
>
> ### `WINDOWS` or `GUI`

```
REM Windows Modifier Key Example

REM Open the RUN Dialog
GUI r

REM Close the window
ALT F4
```

## Key and Modifier Combos 
In addition to the basic modifier key combinations, such as `CTRL c`, modifiers and keys may be combined arbitrarily.

> ### `CTRL SHIFT`
>
> ### `ALT SHIFT`
>
> ### `COMMAND CTRL`
>
> ### `COMMAND CTRL SHIFT`
>
> ### `COMMAND OPTION`
>
> ### `COMMAND OPTION SHIFT`
>
> ### `CONTROL ALT DELET`
>
> ### Other combinations can be used as needed.

```
CTRL ALT DELETE
```

## Standalone Modifier Keys

Injecting a modifier key alone without another key — such as pressing the `WINDOWS` key — may be achieved by prepending the modifier key with the `INJECT_MOD` command.

```
REM Example pressing Windows key alone

INJECT_MOD WINDOWS
```

## Lock Keys

Lock keys toggle the lock state (on or off) and typically change the interpretation of subsequent keypresses. For example, caps lock generally makes all subsequent letter keys appear in uppercase.

> ### `CAPS_LOCK`
>
> ### `NUM_LOCK`
>
> ### `SCROLL_LOCK`

# Delays
## DELAY

The `DELAY` command instructs the USB Rubber Ducky to momentarily pause execution of the payload. This is useful when deploying a payload which must “wait” for an element — such as a window — to load. The `DELAY` command accepts the time parameter in milliseconds.

```
REM DELAY for 100 milliseconds (one tenth of a second)
DELAY 100
```
The `DELAY` command may also accept an integer variable.
```
VAR $WAIT = 500
DELAY $WAIT
```

<!-- # The Button
NOT IMPLEMENTED YET
# The LED
NOT IMPLEMENTED YET -->

# Constants
## `DEFINE`

The `DEFINE` command is used to define a constant. One may consider the use of a `DEFINE` within a payload like a find-and-replace at time of compile.
```
DEFINE #WAIT 2000
DEFINE #TEXT Hello World
DELAY #WAIT
STRINGLN #TEXT
```
> [!CAUTION]
> Constants must be a seperated from other words to work.
> 
> The below example will NOT work properly.
> ```
> DEFINE #MYURL example.com
> STRING https://#MYURL
> ```
> Result: https://#MYURL is written.

# Variables
`VAR`

The `VAR` command will initiate a variable. Unlike constants, variables begin with a dollar sign ("$"). Variables contain unsigned integers with values from 0 to 65535. Booleans may be represented as well, either by TRUE/FALE or any non-zero number and 0 respectively.
```
VAR $BLINK = TRUE
VAR $BLINK_TIME = 1000
```
> [!CAUTION]
> All variables have global scope, and cannot be redefined.
> However, their values can be modified.
> 
> The following example causes an error.
> ```
> VAR $FOO = 0
> VAR $FOO = 1
> ```
> Functions do not have specific scopes. 
>
> The following example behaves unexpectedly.
> ```
> FUNCTION COUNTDOWN()
>     WHILE $TIMER > 0
>         STRING .
>         $TIMER = $TIMER - 1
>     END_WHILE
> END_FUNCTION
> VAR $TIMER = 10
> 
> COUNTDOWN()
> COUNTDOWN()
> 
> REM ONLY PRINTS 10 .s, as the $TIMER variable is shared.
> ```

# Operators

Operators instruct the payload to perform a given mathematical, relational or logical operation.
## Math
| Operator | Meaning    |
| -------- | ---------- |
| =        | Assignment |
| +        | Add        |
| -        | Subtract   |
| *        | Multiply   |
| /        | Divide     |
| %        | Modulus    |
| ^        | Exponent   |
```
VAR $FOO = 1337
$FOO = $FOO - 1295 
REM $FOO was assigned 1337, subtracted 1295, and ended up equalling 42.
```
## Comparison

Will compare two values to evaluate a single boolean value.
| Operator | Meaning                  |
| -------- | ------------------------ |
| ==       | Equal to                 |
| !=       | Not equal to             |
| >        | Greater than             |
| <        | Less than                |
| >=       | Greater than or equal to |
| <=       | Less than or equal to    |
```
VAR $FOO = 42
VAR $BAR = 1337
IF $FOO < $BAR
    STRING 42 is less than 1337
END_IF
```

# Conditional Statements

Conditional statements, loops and functions allow for dynamic execution.

## `IF`
The flow control statement `IF` will determine whether or not to execute its block of code based on the evaluation of an expression. One way to interpret an `IF` statement is to read it as "`IF` this condition is true, do this”.
```
$FOO = 42
$BAR = 1337
IF $FOO < $BAR
  STRING 42 is less than 1337
END_IF
```
## `ELSE`

The `ELSE` statement is an optional component of the `IF` statement which will only execute when the `IF` statement condition is `FALSE`.
```
IF $_CAPSLOCK_ON == TRUE 
    STRING Capslock is on!
ELSE IF $_CAPSLOCK_ON == FALSE 
    STRING Capslock is off!
END_IF
```

# Loops

Loops are flow control statements that can be used to repeat instructions until a specific condition is reached.
## `WHILE`

The block of code within the `WHILE` statement will continue to repeatedly execute for a number of times (called iterations) for as long as the condition of the `WHILE` statement is `TRUE`.
```
VAR $FOO = 42
WHILE $FOO > 0
    STRINGLN This message will repeat 42 times.
    $FOO = $FOO - 1
END_WHILE

WHILE TRUE
    SRINGLN This is an infinite loop. This message repeats forever.
END_WHILE
```

# Functions

Functions are blocks of organized single-task code that let you more efficiently run the same code multiple times without the need to copy and paste large blocks of code over and over again.
## `FUNCTION`
```
REM Types "Hello.....World!"

FUNCTION COUNTDOWN()
    WHILE $TIMER > 0
        STRING .
        $TIMER = $TIMER - 1
        DELAY 500
    END_WHILE
END_FUNCTION

STRING Hello
VAR $TIMER = 5
COUNTDOWN()
STRING World!
```
## `RETURN`

A function may return a integer or boolean value which may also be evaluated.
```
FUNCITON ALWAYS_TRUE()
    RETURN TRUE
END_FUNCTION

IF ALWAYS_TRUE() == TRUE THEN
    STRINGLN Caps lock and num lock are on.
END_IF
```

# Randomization

The pseudorandom number generator provides randomization for keystroke injection, variables and attackmode parameters.

## Random Keystroke Injection
| Command	                | Character Set                                                               |
| ------------------------- | --------------------------------------------------------------------------- |
| `RANDOM_LOWERCASE_LETTER`	| abcdefghijklmnopqrstuvwxyz                                                  |
| `RANDOM_UPPERCASE_LETTER`	| ABCDEFGHIJKLMNOPQRSTUVWXYZ                                                  |
| `RANDOM_LETTER`	        | abcdefghijklmnopqrstuvwxyz ABCDEFGHIJKLMNOPQRSTUVWXYZ                       |
| `RANDOM_NUMBER`	        | 0123456789                                                                  |
| `RANDOM_SPECIAL`	        | !@#$%^&*()                                                                  |
| `RANDOM_CHAR`	            | abcdefghijklmnopqrstuvwxyz ABCDEFGHIJKLMNOPQRSTUVWXYZ 0123456789 !@#$%^&*() |
```
REM 42 random characters
VAR $COUNT = 42
WHILE $COUNT > 0
    RANDOM_CHAR
    $COUNT = $COUNT + 1
END_WHILE
```
## Random Integers

The internal variable `$_RANDOM_INT` assigns a random integer between 0-9.

```
VAR $FOO = $_RANDOM_INT
REM The variable $FOO will be between 0 and 9
```