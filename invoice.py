import json
from helpers import number_to_words_latvian, format_currency
from decimal import Decimal
from pathlib import Path  
from borb.pdf import Document
from borb.pdf import PDF
from borb.pdf import Page
from borb.pdf import PageLayout
from borb.pdf import Paragraph
from borb.pdf import SingleColumnLayout
from borb.pdf import Alignment
from borb.pdf import HexColor
from borb.pdf import TableCell
from borb.pdf import FixedColumnWidthTable
from borb.pdf.canvas.font.simple_font.true_type_font import TrueTypeFont  
from borb.pdf.canvas.font.font import Font

def create_paragraph(text, font, alignment, color, size):
    return Paragraph(text, font=font, horizontal_alignment=alignment, font_color=HexColor(color), font_size=Decimal(size))

def generate_pdf(payer, line_items):
    # configure pdf
    textColor1 = "#666666"
    titleColor1 = "#000000"
    backgroundColor1 = "#EEEEEE"
    fontSize = 10
    font_path: Path = Path("assets/Roboto-Regular.ttf")
    font: Font = TrueTypeFont.true_type_font_from_file(font_path)

    sender = json.loads('{"name": "SIA INFLORIUM", "number": "Reģistrācijas nr. 40103750858", "vat_number": "PVN nr. LV40103750858", "account_line_1": "LV95HABA0551037785821", "account_line_2": "bHABALV22", "account_line_3": "Swedbank", "address": "Juridiskā adrese Rīga, Dunalkas iela 10, LV-1029"}')

    sender_lines = ""
    for key, value in sender.items():
        sender_lines += f"{value}\n"

    payer_lines = ""
    for key, value in payer.items():
        if value != "" and key != "type":
            payer_lines += f"{value}\n"

    # setup Document
    doc: Document = Document()
    page: Page = Page()
    doc.add_page(page)
    layout: PageLayout = SingleColumnLayout(page)

    layout.add(Paragraph("Rēķins Nr. 2022", font=font))
    layout.add(Paragraph("Datums 2012/1/11", font=font))

    # Seller: title
    layout.add(
        Paragraph(
            "Nosūtītājs", 
            font=font, 
            horizontal_alignment=Alignment.RIGHT,
            font_color=HexColor(titleColor1),
            font_size=Decimal(fontSize)
        )
    )

    # Seller: details
    layout.add(
        Paragraph(
            sender_lines, 
            respect_newlines_in_text=True,
            font=font, 
            horizontal_alignment=Alignment.RIGHT,
            text_alignment=Alignment.RIGHT,
            font_color=HexColor(textColor1),
            font_size=Decimal(fontSize)
        )
    )

    # Payer: title
    layout.add(
        Paragraph(
            "Maksātājs",
            font=font,
            font_color=HexColor(titleColor1),
            font_size=Decimal(fontSize)
        )
    )

    # Payer: details
    layout.add(
        Paragraph(
            payer_lines,
            respect_newlines_in_text=True,
            font=font,
            font_color=HexColor(textColor1),
            font_size=Decimal(fontSize)
        )
    )

    # config table
    header_cells = ["Apraksts", "Skaits", "Vienības", "Cena", "Summa, EUR"]

    # init table
    t: FixedColumnWidthTable = FixedColumnWidthTable(
        number_of_columns=5,
        number_of_rows=4,
        column_widths=[Decimal(4), Decimal(.8), Decimal(.9), Decimal(1.2), Decimal(1.2)]
        )

    # add header
    for header_cell in header_cells:
        textAligment = Alignment.LEFT
        if header_cell in ("Skaits", "Vienības"):
            textAligment = Alignment.CENTERED
        if header_cell in ("Cena", "Summa, EUR"):
            textAligment = Alignment.RIGHT

        t.add(
            TableCell(
                create_paragraph(
                    header_cell,
                    font,
                    textAligment,
                    titleColor1,
                    fontSize
                ),
                background_color=HexColor(backgroundColor1)
            )
        )

    print(line_items.get('items'))
    # add line items
    for item in line_items.get('items'):
        for key, value in item.items():
            textAligment = Alignment.LEFT
            if key in ("quantity"):
                textAligment = Alignment.CENTERED

            if key in ("unit_price", "subtotal"):
                value = format_currency(value)
                textAligment = Alignment.RIGHT
            t.add(
                TableCell(
                    create_paragraph(
                        f"{value}",
                        font,
                        textAligment,
                        titleColor1,
                        fontSize
                    ),
                )
            )
            if key == "quantity":
                t.add(
                    TableCell(
                        create_paragraph(
                            "gab.",
                            font,
                            Alignment.CENTERED,
                            titleColor1,
                            fontSize
                        ),
                    )
                )           

    t.set_padding_on_all_cells(Decimal(5), Decimal(5), Decimal(2), Decimal(5))

    layout.add(t)
    # Todo: add total/vat/ vat total number
    
    # layout.add(Paragraph('test', font=font))
    # layout.add(Paragraph(number_to_words_latvian('1.01'), font=font))
    # layout.add(Paragraph(number_to_words_latvian('11.3'), font=font))
    # layout.add(Paragraph(number_to_words_latvian('123.11'), font=font))
    # layout.add(Paragraph(number_to_words_latvian('123.13'), font=font))

    # store
    with open("output.pdf", "wb") as pdf_file_handle:
        PDF.dumps(pdf_file_handle, doc)

def main():
    payer = json.loads('{"type": 1, "name": "SIA “Kreiss”", "registration_number": "40103116320", "vat_number": "LV40103116320", "address": "Bērzlapas 5, Mārupe, Mārupes novads, LV-2167, Latvija", "email": "", "phone_number": "+371 67409300", "bank_account": "LV38PARX0000021540002"}')
    line_items = json.loads('{"items": [{"line_item": "Flowers", "quantity": 1, "unit_price": 35, "subtotal": 35}, {"line_item": "vase", "quantity": 3, "unit_price": 43, "subtotal": 129}, {"line_item": "Delivery in Riga", "quantity": 1, "unit_price": 20, "subtotal": 20}], "total": 184}')
    generate_pdf(payer, line_items)

if __name__ == "__main__":
    main()