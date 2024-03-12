"""Module for generating tickets

This module contains functions for generating tickets.

Raises:
    ValueError: Year must be in format YYYY
"""
# TODO: Add config file for logo, font, grid size, etc.
# TODO: Make the code more reusable in tags.py to avoid code duplication
import os
import barcode
from barcode.writer import ImageWriter
from PIL import Image, ImageDraw, ImageFont
from PyPDF2 import PdfMerger
import pkg_resources



# Dimensions of A4 paper in mm
A4_WIDTH = 210
A4_HEIGHT = 297

# Margin in mm
MARGIN = 10

# Grid dimensions
GRID_WIDTH = 5
GRID_HEIGHT = 5

DPI = 500

MM_TO_INCH = 0.0393701

YEAR = 2024

LINE_COLOR = (100, 100, 100)  # Gray color
LINE_WIDTH = 8
LINE_LENGTH = 15
LINE_SPACING = 30


# Calculate the available width and height for the grid
AVAILABLE_WIDTH = A4_WIDTH - 2 * MARGIN
AVAILABLE_HEIGHT = A4_HEIGHT - 2 * MARGIN

# Calculate cell dimensions
CELL_WIDTH = AVAILABLE_WIDTH / GRID_WIDTH
CELL_HEIGHT = AVAILABLE_HEIGHT / GRID_HEIGHT

def ean_gen(year: int, start: int, stop: int) -> list[str]:
    """Generate EAN8 codes in format YYNNNN0X

    Args:
        year (int): Year of the event
        start (int): Number of the first ticket
        stop (int): Number of the last ticket

    Returns:
        list[str]: List of EAN8 codes
    """
    ean = []
    for i in range(start, stop + 1):
        ean.append(str(year)[2:] + str(i).zfill(4) + "0")

    return ean


def generate_ean(ean: list[str]) -> None:
    """Generate EAN8 barcodes

    Args:
        ean (list[str]): List of EAN8 codes
    """
    for i in ean:
        # EAN8 without checksum
        code = barcode.EAN8(i, writer=ImageWriter())
        code.save(f'barcode_{i}')


def create_ticket(ean: str, style: str, year:int=YEAR) -> Image:
    """Create a ticket with a barcode, style and year

    Args:
        ean (str): EAN8 code
        style (str): Style of the ticket
        year (int, optional): Year of the event. Defaults to YEAR.

    Returns:
        Image: Image of the ticket
    """
    image = Image.new('RGB', (int(CELL_WIDTH * DPI * MM_TO_INCH), int(CELL_HEIGHT * DPI * MM_TO_INCH)), color = (255, 255, 255))
    # Code
    code = Image.open(f'barcode_{ean}.png')
    code = code.resize((int(CELL_WIDTH * DPI * MM_TO_INCH), int(code.height * (CELL_WIDTH * DPI * MM_TO_INCH) / code.width)))
    image.paste(code, (0, int(CELL_HEIGHT * DPI * MM_TO_INCH) - code.height))

    # Style
    if os.path.exists(f"{style}.png"):
        top = Image.open(f"{style}.png")
        top = top.resize((int(CELL_WIDTH * DPI * MM_TO_INCH), int(top.height * (CELL_WIDTH * DPI * MM_TO_INCH) / top.width)))
        image.paste(top, (0, 0))

    # Text
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype("OpenSans-Bold.ttf", 100)

    # Los number
    los = f'Los {int(ean[2:6])}'
    los_width = draw.textlength(los, font=font)
    draw.text((int((CELL_WIDTH * DPI * MM_TO_INCH - los_width) // 2), 125), los, fill='black', font=font)

    # Logo
    try:
        logo_path = pkg_resources.resource_filename('Tombolenkovac', 'data/logo.png')
    except ModuleNotFoundError:
        location = os.path.realpath(
            os.path.join(os.getcwd(), os.path.dirname(__file__)))
        logo_path = os.path.join(location, 'data/logo.png')
    logo = Image.open(logo_path)
    logo = logo.resize((200, 200))
    image.paste(logo, ((int(CELL_WIDTH * DPI * MM_TO_INCH) // 2 - 310), 350))

    # {year - 1995}. ples MFF UK
    font = ImageFont.truetype("OpenSans-Bold.ttf", 100)
    ples = f'{year - 1995}. ples'
    draw.text((int(CELL_WIDTH * DPI * MM_TO_INCH) // 2 - 75, 310), ples, fill='black', font=font)
    ples = 'MFF UK'
    draw.text((int(CELL_WIDTH * DPI * MM_TO_INCH) // 2 - 75, 440), ples, fill='black', font=font)

    return image


def make_A4(year: int, start: int, stop: int, style: str) -> None:
    """Make A4 grid of tickets

    Args:
        year (int): Year of the event
        start (int): Number of the first ticket
        stop (int): Number of the last ticket
        style (str): Style of the ticket

    Raises:
        ValueError: Year must be in format YYYY
    """
    if len(str(year)) != 4:
        raise ValueError("Year must be in format YYYY")

    ean = ean_gen(year, start, stop)
    generate_ean(ean)
    
    tickets = [create_ticket(i, style, year) for i in ean]

    # Create A4 grid
    tickets_grid = Image.new('RGB', (int(A4_WIDTH * DPI * MM_TO_INCH), int(A4_HEIGHT * DPI * MM_TO_INCH)), color = (255, 255, 255))
    for i in range(GRID_HEIGHT):
        for j in range(GRID_WIDTH):
            index = i * GRID_WIDTH + j
            if index >= len(tickets):
                break
            tickets_grid.paste(tickets[index], (int(MARGIN * DPI * MM_TO_INCH + j * CELL_WIDTH * DPI * MM_TO_INCH), int(MARGIN * DPI * MM_TO_INCH + i * CELL_HEIGHT * DPI * MM_TO_INCH)))

    # Add dotted lines to the grid
    draw = ImageDraw.Draw(tickets_grid)
    lines(draw)

    # Save it as pdf
    tickets_grid.save(f'tickets_{year}_{start}_{stop}.pdf')


def lines(draw: ImageDraw) -> None:
    """Add dotted lines to the grid

    Args:
        draw (ImageDraw): ImageDraw object
    """
    for i in range(0, GRID_WIDTH + 1):
        for j in range(int(MARGIN * DPI * MM_TO_INCH), int((MARGIN + GRID_HEIGHT * CELL_HEIGHT) * DPI * MM_TO_INCH), LINE_SPACING + LINE_WIDTH):
            draw.line([(int((MARGIN + i * CELL_WIDTH) * DPI * MM_TO_INCH), j), (int((MARGIN + i * CELL_WIDTH) * DPI * MM_TO_INCH), j + LINE_LENGTH)], fill=LINE_COLOR)

    for i in range(0, GRID_HEIGHT + 1):
        for j in range(int(MARGIN * DPI * MM_TO_INCH), int((MARGIN + GRID_WIDTH * CELL_WIDTH) * DPI * MM_TO_INCH), LINE_SPACING + LINE_WIDTH):
            draw.line([(j, int((MARGIN + i * CELL_HEIGHT) * DPI * MM_TO_INCH)), (j + LINE_LENGTH, int((MARGIN + i * CELL_HEIGHT) * DPI * MM_TO_INCH))], fill=LINE_COLOR)


def make_tickets(year: int, start: int, stop: int, style: str) -> None:
    """Make tickets

    Args:
        year (int): Year of the event
        start (int): Number of the first ticket
        stop (int): Number of the last ticket
        style (str): Style of the ticket
    """
    # On one page there are 25 tickets
    for i in range(start, stop, 25):
        make_A4(year, i, min(i + 24, stop), style)
        print(f"Page {i // 25 + 1} out of {(stop + ((25 - stop) % 25)) // 25} done")

    concatenate()

    clean()


def concatenate() -> None:
    """Concatenate all pdfs to one
    """
    files = os.listdir()
    pdfs = []
    for file in files:
        if file.startswith('tickets_'):
            pdfs.append(file)
    pdfs.sort(key=lambda x: int(x.split('_')[2]))

    merger = PdfMerger()
    for pdf in pdfs:
        merger.append(pdf)
    merger.write('tombolenky.pdf')
    merger.close()


def clean() -> None:
    """Clean the directory
    """
    files = os.listdir()
    for file in files:
        if file.startswith('barcode_'):
            os.remove(file)
        if file.startswith('ticket_'):
            os.remove(file)
        if file.startswith('tickets_'):
            os.remove(file)
        if file.startswith('tags_'):
            os.remove(file)
