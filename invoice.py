import json
from helpers import amount_to_words, format_currency, extract_vat, amount_without_vat
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

# theme PDF
textColor1 = "#000000"
textColor2 = "#666666"

backgroundColor1 = "#EEEEEE"
fontSize = 10
font_path: Path = Path("assets/Roboto-Regular.ttf")
font: Font = TrueTypeFont.true_type_font_from_file(font_path)

def create_paragraph(text, newlines=False, font=font, alignment=Alignment.LEFT, text_alignment=Alignment.LEFT, color=textColor1, size=fontSize):
    return Paragraph(
        text,
        respect_newlines_in_text=newlines,
        font=font,
        horizontal_alignment=alignment,
        text_alignment=text_alignment,
        font_color=HexColor(color),
        font_size=Decimal(size)
    )

def create_pdf(payer, line_items):
    sender = json.loads('{"name": "SIA INFLORIUM",  "number": "Reģistrācijas nr. 40103750858", "vat_number": "PVN nr. LV40103750858", "account_line_1": "LV95HABA0551037785821", "account_line_2": "HABALV22", "account_line_3": "Swedbank", "address": "Juridiskā adrese Rīga, Dunalkas iela 10, LV-1029"}') 
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

    layout.add(create_paragraph("Rēķins Nr. 01/12/2023"))
    layout.add(create_paragraph("Datums 01/12/2023"))

    # Seller: title
    layout.add(
        create_paragraph(
            "Nosūtītājs", 
            alignment=Alignment.RIGHT
        )
    )

    # Seller: details
    layout.add(
        create_paragraph(
            sender_lines, 
            color=textColor2,
            newlines=True,
            alignment=Alignment.RIGHT,
            text_alignment=Alignment.RIGHT,
        )
    )

    # Payer: title
    layout.add(
        create_paragraph(
            "Maksātājs"
        )
    )

    # Payer: details
    layout.add(
        create_paragraph(
            payer_lines,
            color=textColor2,
            newlines=True,
        )
    )

    # config table header
    header_cells = ["Apraksts", "Skaits", "Vienības", "Cena", "Summa, EUR"]
    total = 0

    # define table
    t: FixedColumnWidthTable = FixedColumnWidthTable(
        number_of_columns=5,
        number_of_rows= (6 + len(line_items.get('items'))),
        column_widths=[Decimal(4), Decimal(.8), Decimal(.9), Decimal(1.2), Decimal(1.2)]
        )

    # table: add header
    for cell in header_cells:
        textAligment = Alignment.LEFT
        if cell in ("Skaits", "Vienības"):
            textAligment = Alignment.CENTERED
        if cell in ("Cena", "Summa, EUR"):
            textAligment = Alignment.RIGHT

        t.add(
            TableCell(
                create_paragraph(
                    cell,
                    alignment=textAligment,
                ),
                background_color=HexColor(backgroundColor1)
            )
        )

    # table: add line items
    for item in line_items.get('items'):
        for key, value in item.items():
            textAligment = Alignment.LEFT
            if key in ("quantity"):
                textAligment = Alignment.CENTERED
            if key in ("subtotal"):
                total = total + float(value)
            if key in ("unit_price", "subtotal"):
                value = format_currency(value)
                textAligment = Alignment.RIGHT
            t.add(
                TableCell(
                    create_paragraph(
                        f"{value}",
                        alignment=textAligment,
                    ),
                )
            )
            if key == "quantity":
                t.add(
                    TableCell(
                        create_paragraph(
                            "gab.",
                            alignment=Alignment.CENTERED,
                        ),
                    )
                )       

    # Total without VAT
    t.add(
        TableCell(
            create_paragraph(
                "Ar PVN 21% apliekamā summa:",
                alignment=Alignment.RIGHT,
            ),
            column_span=4,
            border_top=False,
            border_left=False,
            border_right=False,
            border_bottom=False
        )
    )    
    t.add(
        TableCell(
            create_paragraph(
                format_currency(amount_without_vat(total)),
                alignment=Alignment.RIGHT,
            ),
            border_top=False,
            border_left=False,
            border_right=False,
            border_bottom=False
        )
    )  

     # VAT line
    t.add(
        TableCell(
            create_paragraph(
                "PVN 21%:",
                alignment=Alignment.RIGHT,
            ),
            column_span=4,
            border_top=False,
            border_left=False,
            border_right=False,
            border_bottom=False
        )
    )    
    t.add(
        TableCell(
            create_paragraph(
                format_currency(extract_vat(total)),
                alignment=Alignment.RIGHT,
            ),
            border_top=False,
            border_left=False,
            border_right=False,
            border_bottom=False
        )
    )     

    # Total with VAT
    t.add(
        TableCell(
            create_paragraph(
                "Kopā ar PVN:",
                alignment=Alignment.RIGHT,
            ),
            column_span=4,
            border_top=False,
            border_left=False,
            border_right=False,
            border_bottom=False
        )
    )    
    t.add(
        TableCell(
            create_paragraph(
                format_currency(total),
                alignment=Alignment.RIGHT,
            ),
            border_top=False,
            border_left=False,
            border_right=False,
            border_bottom=False
        )
    )     

    # Amount in words
    t.add(
        TableCell(
            create_paragraph(
                "Summa vārdiem:",
            ),
            border_top=False,
            border_left=False,
            border_right=False,
            border_bottom=False
        )
    )    
    t.add(
        TableCell(
            create_paragraph(
                amount_to_words(total),
            ),
            column_span=4,
            border_top=False,
            border_left=False,
            border_right=False,
            border_bottom=False
        )
    ) 

    # Due date
    t.add(
        TableCell(
            create_paragraph(
                "Apmaksas datums un kārtība:",
            ),
            border_top=False,
            border_left=False,
            border_right=False,
            border_bottom=False
        )
    )    
    t.add(
        TableCell(
            create_paragraph(
                "01.12.2023 / Pārskaitījums",
            ),
            column_span=4,
            border_top=False,
            border_left=False,
            border_right=False,
            border_bottom=False
        )
    ) 

    t.set_padding_on_all_cells(Decimal(5), Decimal(5), Decimal(2), Decimal(5))
    layout.add(t)

    layout.add(
        create_paragraph(
            "Rēķins sagatavots elektroniski un ir derīgs bez paraksta",
            alignment=Alignment.CENTERED
        )
    )
    layout.add(
        create_paragraph(
            "INFLORIUM / <a href=http://www.inflorium.lv>www.inflorium.lv</a> / studio@inflorium.lv / +371 2284 4122",
            alignment=Alignment.CENTERED
        )
    )

    # store
    with open("output.pdf", "wb") as pdf_file_handle:
        PDF.dumps(pdf_file_handle, doc)

def main():
    payer = json.loads('{"type": 1, "name": "SIA “Kreiss”", "registration_number": "40103116320", "vat_number": "LV40103116320", "address": "Bērzlapas 5, Mārupe, Mārupes novads, LV-2167, Latvija", "email": "", "phone_number": "+371 67409300", "bank_account": "LV38PARX0000021540002"}')
    line_items = json.loads('{"items": [{"line_item": "Flowers", "quantity": 1, "unit_price": 35, "subtotal": 35}, {"line_item": "Delivery in Riga", "quantity": 1, "unit_price": 20, "subtotal": 20}], "total": 55}')
    create_pdf(payer, line_items)

if __name__ == "__main__":
    main()