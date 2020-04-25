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
Creating new character from scratch.

You will be guided through the steps of character creations. At each step, you will be presented with a series of options.
To exit character creator, enter 'exit'
Choose a Species:
[0] Human
[1] Elek
[2] Parathan
[3] Primas-Ika
[4] Yasre
# 4
Successfully selected Yasre for your Species.
Selection opens up new options.
Choose a Species Trait:
[0] By His Righteous Code
[1] The Old Hunger
# 1
Successfully selected The Old Hunger for your Species Trait.
Done with this choice tree! Moving on.
Choose a Talent:
[0] Brawn
[1] Grace
[2] Wits
[3] Spirit
# 1
Successfully selected Grace for your Talent.
Done with this choice tree! Moving on.
Choose a Die to Boost:
[0] Shooting Die
[1] Fighting Die
# 1

## EXAMPLE TRUNCATED ##

Input your character's Name:
# Laredo
Done with this choice tree! Moving on.
Successfully created 'Laredo'!

MAIN MENU
---------
Current character: Laredo
Choose an option:
[0] New Character
[1] Load Character from File
[2] Save Character
[3] Edit Character
[4] Output Character Sheet to PDF
[5] Exit (or type 'exit')
# 
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