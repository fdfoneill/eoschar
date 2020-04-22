# eoschar

Python package for creating beautiful character sheets for the Era of Silence role-playing game

# Motivation

Era of Silence (EoS) is a futuristic fantasy tabletop role-playing game, one that is built on a unique foundation and aspires to be a dynamic, fast-paced, and exciting system. The goal of EoS as a system is to inspire realism through a ruleset that rewards realistic actions.

Creating characters is always one of the most labor-intensive parts of playing an RPG. For some players, it's also their favorite part--building a unique character from scratch has a joy all its own. For others, however, the process can be laborious. This package is intended to streamline the process, allowing anyone to quickly and easily produce a rules-legal EoS character, written up on a beautiful single-page character sheet.

# Features

The current version of `eoschar` works through a command-line interface. (Future versions will feature a graphic user interface.) The `eoschar` command takes several subcommands, including:

* `new`: Start a new character
* `load`: Load an existing character

# Code Example

```
> eoschar new
Creating a new character from scratch.
Choose a Species:
[1] Elek
[2] Human
[3] Parathan
[4] Primas-Ika
[5] Yasre
>>>5
Selected Yasre.
Species choice unlocks new choices!
Choose a Species Trait:
[1] Vian Moves Slowly
[2] Unrivaled Reaction
>>>1
Selected Vian Moves Slowly.
End of category.
Choose a Talent:
[1] Brawn
[2] Grace
[3] Wits
[4] Spirit
>>> Grace
Chose Grace.
End of category.

##### Example Truncated #####

Character fully generated.
[1] Save character data
[2] Create character sheet
[3] Edit character
[4] Exit
>>>
```

# How to Use

Once the package is fully installed, call `eoschar new` from the command line. The interface will then guide you through the process of creating an Era of Silence character from scratch! You can exit the program at any time by typing 'exit.' To save an in-progress character, type 'save.'

Once you have created your character, you can save the data to a file as pickled text. Previously created characters can be loaded with the `eoschar load` command. Completed characters can also be saved as beautiful PDF character sheets, although this format does not allow for re-loading into `eoschar`.

# License

MIT License

Copyright (c) 2020 Shrike Tabletop

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.