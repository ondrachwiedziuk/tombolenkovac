from fpdf import FPDF

def draw_tickets():
    win = []
    i = 1
    while True:
        ticket = input(f"{i}-th ticket: ")
        if ticket == "exit":
            break
        else:
            print(f"Drawing ticket {ticket}")
            win.append(ticket)
    print("Drawing finished")
    file = open("winning_tickets.txt", "w", encoding="utf-8")
    file.write("winning_tickets.txt", win)
    file.close()
    make_pdf(win)

def make_pdf(win):
    # Make pdf of winning tickets using pypdf2
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Winning tickets", ln=True, align="C")
    for i in win:
        pdf.cell(200, 10, txt=i, ln=True, align="C")
    pdf.output("winning_tickets.pdf")
    print("Winning tickets saved to winning_tickets.pdf")


def check_ticket(prizes_file):
    # load csv
    prizes = {}
    with open(prizes_file, "r", encoding="utf-8") as file:
        for line in file:
            ticket, prize = line.strip().split(",")
            prizes[ticket] = prize
    # check if the ticket is winning
    while True:
        ticket = input("Enter the ticket number: ")
        if ticket == "exit":
            break
        else:
            print(f"Checking ticket {ticket}")
            if ticket in prizes:
                print(f"Ticket {ticket} won {prizes[ticket]}")
            else:
                print(f"Ticket {ticket} did not win")
