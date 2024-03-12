import os
from PIL import Image, ImageDraw, ImageFont
from PyPDF2 import PdfMerger
from fpdf import FPDF


# Dimensions of A4 paper in mm
A4_WIDTH = 210
A4_HEIGHT = 297

# Margin in mm
MARGIN = 10

# Grid dimensions
GRID_WIDTH = 6
GRID_HEIGHT = 10

DPI = 500
MM_TO_INCH = 0.0393701  

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

def create_square():
    SIZE = min(CELL_WIDTH, CELL_HEIGHT) - 2 * LINE_WIDTH
    image = Image.new('RGB', (int(SIZE * DPI * MM_TO_INCH), int(SIZE * DPI * MM_TO_INCH)), color='white')
    draw = ImageDraw.Draw(image)
    # Square rotated by 45 degrees with the center in the middle of the image and fitted into the image
    center = (SIZE * DPI * MM_TO_INCH / 2, SIZE * DPI * MM_TO_INCH / 2)
    vertices = [(center[0] + SIZE * DPI * MM_TO_INCH / 2, center[1]), (center[0], center[1] + SIZE * DPI * MM_TO_INCH / 2), (center[0] - SIZE * DPI * MM_TO_INCH / 2, center[1]), (center[0], center[1] - SIZE * DPI * MM_TO_INCH / 2)]
    
    draw.polygon(vertices, fill='black')
    image.save('square.png')
    

def create_tag(number: int) -> Image:
    image = Image.new('RGB', (int(CELL_WIDTH * DPI * MM_TO_INCH), int(CELL_HEIGHT * DPI * MM_TO_INCH)), color='white')
    square = Image.open('square.png')
    image.paste(square, (LINE_WIDTH, LINE_WIDTH))

    # font = ImageFont.truetype('OpenSans-Regular.ttf', 100)
    # draw = ImageDraw.Draw(image)
    # text = str(number)
    # width = draw.textlength(text, font=font)
    # draw.text(((CELL_WIDTH * DPI * MM_TO_INCH - width) / 2, (CELL_HEIGHT * DPI * MM_TO_INCH - 100) / 2), text, font=font, fill='white')
    return image


def make_A4(start, stop):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=0)
    pdf.add_page()
    for i in range(start, stop + 1):
        if i % (GRID_HEIGHT * GRID_WIDTH) == 0:
            pdf.add_page()
        x = (i - start) % GRID_WIDTH
        y = (i - start) // GRID_WIDTH % GRID_HEIGHT
        create_tag(i).save('tags_' + str(i) + '.png')
        pdf.image('tags_' + str(i) + '.png', MARGIN + x * CELL_WIDTH * DPI * MM_TO_INCH, MARGIN + y * CELL_HEIGHT * DPI * MM_TO_INCH, CELL_WIDTH * DPI * MM_TO_INCH, CELL_HEIGHT * DPI * MM_TO_INCH)
    pdf.output('tags_' + str(start) + '_' + str(stop) + '.pdf')


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


def make_tags(start: int, stop: int) -> None:
    """Make tags

    Args:
        start (int): Number of the first tag
        stop (int): Number of the last tag
    """
    for i in range(start, stop, GRID_HEIGHT * GRID_WIDTH):
        make_A4(i, i + GRID_HEIGHT * GRID_WIDTH - 1)
        print(f"Page {i // (GRID_HEIGHT * GRID_WIDTH) + 1} out of {(stop + (((GRID_HEIGHT * GRID_WIDTH) - stop) % (GRID_HEIGHT * GRID_WIDTH))) // (GRID_HEIGHT * GRID_WIDTH)} done")

    concatenate()


def concatenate() -> None:
    """Concatenate all pdfs to one
    """
    files = os.listdir()
    pdfs = []
    for file in files:
        if file.startswith('tags_'):
            pdfs.append(file)
    pdfs.sort(key=lambda x: int(x.split('_')[1]))

    merger = PdfMerger()
    for pdf in pdfs:
        merger.append(pdf)
    merger.write('tags.pdf')
    merger.close()
