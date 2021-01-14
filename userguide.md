# User Guide

Sidekick takes voice commands and converts them to actions on the computer. It operates differently when in different states or modes. There are currently three modes, described below, but more can be added.

- command - this mode allows the user to issue a variety of commands
- mouse - this mode allows the user to control the mouse
- text - this mode transcribes spoken speech to text

In each mode certain keywords are linked to certain actions. To switch between modes, simply say 'command', 'mouse', or 'text'. These keywords are reserved to switch between modes. More details provided below, with examples of the more complex commands. 

## Command

Some commands are stateless, in that they function no matter what state/mode you are in. Others only function when in the command state.

#### Stateless

- `click` or `go` - double click left mouse button
- `double` - double click left mouse button
- `enter` 
- `space`
- `back [1-7]` - hit backspace 

#### Stateful

- `up`, `left`, `down`, `right` - arrow keys
- `copy`
- `paste`
- `save`
- `north [1-7]`, `south [1-7]`, `east [1-7]`, `west [1-7]` - move mouse in cardinal directions 
- `scroll [up,down,left,right] [1-7]` 

#### Examples

- `scroll up 1 2 1` - will scroll up 1, then 2, then 1 again - number can be repeated without repeating entire command
- `north 3 1` - moves mouse north 3, then 1
- `back 1 2` - backspace by 1, then 2

## Mouse

Once you say `mouse` and provide a direction, such as `north`, the mouse will begin to move that direction at the `slow` speed. You then use the commands to change direction, change speed, or stop the mouse. 

- `north`, `south`, `east`, `west`, `northeast` or `one`, `northwest` or `two`, `southeast` or `three`, `southwest` or `four`
- `stop` - stop the mouse
- `snail`, `slow`, `medium`, `fast` - speed at which mouse moves - slow is default
- `counter` or `up` - rotate direction 15 degrees counterclockwise
- `clock` or `down` - rotate direction 15 degrees clockwise

#### Examples

- `mouse north medium clock stop` - mouse moves north, speed changed to medium, rotated clockwise 15 degreeds, then stopped

## Text

In text mode, speech will be transcribed to text. There are, however, somekeywords used for punctuation. 

A space is automatically added after each word when speaking. Therefore, punctuation is added by first going back one space, adding the punctuation, and then adding a space afterwards. The exceptions are `hash` and `dash`, which are written directly to text without any backspaces or spaces, and `dot`, which uses backspace but inserts no space after (for web addresses).

- `period`
- `comma` or `coma`
- `colon` or `colin`
- `q` for question mark
- `semi` for semicolon
- `exclamation` for exclamation point
- `hash`
- `dash`
- `dot`
- `caps` or `capitalize` - word spoken after this keyword will be capitalized

#### Examples

- `caps hello coma how are you q` - will produce the text 'Hello, how are you?'