"""Main module for Tombolenkovac

This module provides a CLI app for Tombolenkovac.
"""


import argparse
import sys
import tombolenkovac.generate as generate
import tombolenkovac.draw as draw
# import tombolenkovac.tags as tags

def main() -> None:
    """CLI app for Tombolenkovac
    """
    parser = argparse.ArgumentParser(description='Tombolenkovac')
    parser.add_argument('--gen', action='store_true', help='Generate tickets')
    parser.add_argument('--draw', action='store_true', help='Draw winning tickets')
    parser.add_argument('--check', action='store_true', help='Check if the ticket is winning')
    parser.add_argument('--clean', action='store_true', help='Clean the directory')
    parser.add_argument('--version', action='version', version='%(prog)s 0.2.4')
    parser.add_argument('--prizes', action='store_true', help='Create prizes file')
    parser.add_argument('--winners', action='store_true', help='Create winners file')
    parser.add_argument('--prize-path', type=str, help='Path to the prizes file', default='prizes.csv')
    parser.add_argument('--pdf-path', type=str, help='Path to the pdf file', default='winning_tickets.pdf')
    parser.add_argument('--tags', action='store_true', help='Make tags')

    args = parser.parse_args()

    if args.gen:
        year = int(input('Enter the year: '))
        start = int(input('Enter the start number: '))
        stop = int(input('Enter the stop number: '))
        style = input('Enter the style: ')
        generate.make_tickets(year, start, stop, style)

    elif args.clean:
        generate.clean()

    elif args.draw:
        start = int(input('Enter the number of first drawn prize (blank from 1): ').strip() or 1)
        draw.draw_tickets(args.prize_path, args.pdf_path, start)

    elif args.check:
        draw.check_ticket(args.prize_path)

    elif args.prizes:
        mode = input('Enter the mode (default append): ') or 'a'
        draw.generate_prizes(mode, args.prize_path)

    elif args.winners:
        start = int(input('Enter the start number: '))
        draw.make_pdf(args.prize_path, args.pdf_path, start)
    
    elif args.tags:
        print("This function is not yet implemented.")

        # start = int(input('Enter the start number: '))
        # stop = int(input('Enter the stop number: '))
        # tags.make_tags(start, stop)
        # generate.clean()

    else:
        print('No command given, try --help for help.')
        sys.exit(1)
    sys.exit(0)

if __name__ == '__main__':
    main()
