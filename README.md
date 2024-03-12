# Tombolenkovač

Tombolenkovač is a simple tool for creating tickets for a tombola, drawing winning tickets, and checking if a ticket won.

## Installation

For installation, use

```bash
python -m pip install tombolenkovac
```

## Usage

### Prizes file

First, you need to create a file with prizes. Each line contains one prize. To create a file with prizes, run:

```bash
tombolenkovac --prizes --prize-file prizes.csv
```

Then enter mode (`c`) to create a new file, and enter the prizes. To finish, enter (`exit`).

You can also edit the file by entering mode (`e`), append new prizes by entering mode (`a`), delete the file by entering mode (`d`), list the prizes by entering mode (`l`), or insert new prize by entering mode (`i`).


### Tickets file
To generate tickets, run

```bash
tombolenkovac --gen
```

and follow the instructions. It will create tombolenky.pdf.

### Drawing and checking tickets
To draw winning tickets, run

```bash
tombolenkovac --draw
```
and scan winning tickets until all prizes runs out.

To check if ticket won, run

```bash
tombolenkovac --check
```
and scan the ticket. It will return the number of prize, or it says it is not a winning ticket.
