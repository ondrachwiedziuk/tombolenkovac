"""Draw winning tickets for a lottery.

This module provides a set of functions for drawing winning tickets for a lottery.
"""

import csv
from fpdf import FPDF

def number_from_ticket(ticket: str) -> int:
    """Extract number from ticket

    Args:
        ticket (str): ticket number in format YYNNNN0X

    Returns:
        int: number from ticket in format NNNN
    """
    return int(ticket[2:6])


def draw_tickets(prizes_file: str = 'prizes.csv', pdf_path: str = 'winning_tickets.pdf', start: int = 1) -> None:
    """Draw winning tickets

    Args:
        prizes_file (str, optional): Path to the prizes file. Defaults to 'prizes.csv'.
        pdf_path (str): Path to the pdf file.
        start (int, optional): Number of first drawn prize. Defaults to 1.
    """
    with open(prizes_file, "r", encoding="utf-8") as file:
        reader = csv.reader(file)
        data = list(reader)
    end = len(data)
    for i in range(start, len(data)):
        ticket = input(f"{i}-th winning ticket: ")
        if ticket == "exit":
            end = i
            break
        else:
            data[i][2] = ticket

    with open(prizes_file, "w", newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(data)

    make_pdf(prizes_file, pdf_path, start, end)


def make_pdf(prizes_file: str = 'prizes.csv', pdf_path: str = 'winning_tickets.pdf', start: int = 1, end = None) -> None:
    """Make pdf with winning tickets

    Args:
        prizes_file (str, optional): Path to the prizes file. Defaults to 'prizes.csv'.
        pdf_path (str, optional): Path to the pdf file. Defaults to 'winning_tickets.pdf'.
        start (int, optional): Number of first drawn prize. Defaults to 1.
        end (int, optional): Number of last drawn prize. Defaults to None.
    """
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Výherní lístky", ln=True, align="C")
    with open(prizes_file, "r", encoding="utf-8") as file:
        reader = csv.reader(file)
        data = list(reader)
    if end is None:
        end = len(data)
    for i in range(start, end):
        print(f"Drawing {i} out of {end - 1}")
        pdf.cell(200, 10, txt=str(number_from_ticket(data[i][2])), ln=True, align="C")
    pdf.output(pdf_path)
    print(f"Winning tickets saved to {pdf_path}")


def check_ticket(prizes_file: str = 'prizes.csv') -> None:
    """Check if the ticket is winning

    Args:
        prizes_file (str, optional): Path to the prizes file. Defaults to 'prizes.csv'.
    """
    with open(prizes_file, "r", encoding="utf-8") as file:
        reader = csv.reader(file)
        data = list(reader)
    while True:
        ticket = input("Enter the ticket number: ")
        if ticket == "exit":
            break
        for row in data:
            if row[2] == ticket:
                print(f"Ticket {number_from_ticket(ticket)} won {row[0]}: {row[1]}")
                break
        else:
            print(f"Ticket {number_from_ticket(ticket)} did not win")


def generate_prizes(mode: str, prizes_file='prizes.csv'):
    """Generate prizes file

    Args:
        mode (str): Mode of generating prizes file. 'c' for create, 'a' for append, 'e' for edit, 'd' for delete, 'i' for insert, 'l' for list.
        prizes_file (str, optional): Path to the prizes file. Defaults to 'prizes.csv'.
    """
    match mode:
        case 'c':
            create(prizes_file)
        case 'a':
            append(prizes_file)
        case 'e':
            edit(prizes_file)
        case 'd':
            delete(prizes_file)
        case 'i':
            insert(prizes_file)
        case 'l':
            with open(prizes_file, 'r', newline='', encoding='utf-8') as file:
                reader = csv.reader(file)
                data = list(reader)
            for row in data:
                print(f"{row[0]}: {row[1]}")
        case _:
            print('Invalid mode')
            return


def create(prizes_file: str = 'prizes.csv') -> None:
    """Create prizes file

    Args:
        prizes_file (str, optional): Path to the prizes file. Defaults to 'prizes.csv'.
    """
    with open(prizes_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['index', 'prize', 'ticket'])
        i = 1
        while True:
            prize = input('Enter the prize: ')
            if prize == 'exit':
                break
            writer.writerow([i, prize, None])
            i += 1


def append(prizes_file: str = 'prizes.csv') -> None:
    """Append prize to the prizes file

    Args:
        prizes_file (str, optional): Path to the prizes file. Defaults to 'prizes.csv'.
    """
    with open(prizes_file, 'r', encoding='utf-8') as file:
        i = sum(1 for _ in file)
    with open(prizes_file, 'a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        while True:
            prize = input('Enter the prize: ')
            if prize == 'exit':
                break
            writer.writerow([i, prize, None])
            i += 1


def edit(prizes_file: str = 'prizes.csv') -> None:
    """Edit prize in the prizes file

    Args:
        prizes_file (str, optional): Path to the prizes file. Defaults to 'prizes.csv'.
    """
    with open(prizes_file, 'r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        data = list(reader)
        while True:
            i = input('Enter the index: ')
            if i == 'exit':
                break
            prize = input('Enter the prize: ')
            for row in data:
                if row[0] == i:
                    row[1] = prize

    with open(prizes_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(data)


def delete(prizes_file: str = 'prizes.csv') -> None:
    """Delete prize from the prizes file

    Args:
        prizes_file (str, optional): Path to the prizes file. Defaults to 'prizes.csv'.
    """
    with open(prizes_file, 'r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        data = list(reader)
    while True:
        i = input('Enter the index: ')
        if i == 'exit':
            break
        for row in data:
            if row[0] == i:
                data.remove(row)
    with open(prizes_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(data)


def insert(prizes_file: str = 'prizes.csv') -> None:
    """Insert prize to the prizes file

    Args:
        prizes_file (str, optional): Path to the prizes file. Defaults to 'prizes.csv'.
    """
    with open(prizes_file, 'r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        data = list(reader)
    while True:
        i = input('Enter the index: ')
        if i == 'exit':
            break
        prize = input('Enter the prize: ')
        for row in data:
            if row[0] == i:
                data.insert(int(i), [i, prize, None])
    with open(prizes_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(data)
