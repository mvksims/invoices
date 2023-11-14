import json
import random
from faker import Faker
from reportlab.pdfgen import canvas

fake = Faker()

def generate_invoice_data():
    client_details = {
        "company_name": fake.company(),
        "registration_number": fake.random_int(min=1000, max=9999),
        "vat_number": fake.random_int(min=100000, max=999999),
        "address": fake.address(),
        "phone_number": fake.phone_number(),
        "email": fake.email(),
        "bank_account": fake.iban(),
    }

    seller_details = {
        "company_name": "Your Company Name",
        "registration_number": "12345",
        "vat_number": "GB123456789",
        "address": "Your Company Address",
        "phone_number": "123-456-7890",
        "email": "info@yourcompany.com",
        "bank_account": "Your Bank Account Number",
    }

    products = [
        {"line_item": fake.word(), "quantity": fake.random_int(min=1, max=10), "unit_price": f"{fake.random_int(min=5, max=50):.2f}"}
        for _ in range(3)
    ]

    total_pre_tax = sum(float(product["unit_price"]) * product["quantity"] for product in products)
    tax = total_pre_tax * 0.21
    total = total_pre_tax + tax

    return {
        "client_details": client_details,
        "seller_details": seller_details,
        "products": products,
        "total_pre_tax": f"{total_pre_tax:.2f}",
        "tax": f"{tax:.2f}",
        "total": f"{total:.2f}",
    }

def create_invoice_pdf(file_path, invoice_data):
    pdf_canvas = canvas.Canvas(file_path)

    # Add client details
    pdf_canvas.drawString(100, 800, "Client Details:")
    y_position = 780
    for key, value in invoice_data["client_details"].items():
        pdf_canvas.drawString(100, y_position, f"{key}: {value}")
        y_position -= 20

    # Add seller details
    pdf_canvas.drawString(100, y_position, "\nSeller Details:")
    y_position -= 20
    for key, value in invoice_data["seller_details"].items():
        pdf_canvas.drawString(100, y_position, f"{key}: {value}")
        y_position -= 20

    # Add products
    pdf_canvas.drawString(100, y_position, "\nProducts:")
    y_position -= 20
    for product in invoice_data["products"]:
        line_item = f"{product['line_item']} (Qty: {product['quantity']}, Unit Price: {product['unit_price']})"
        pdf_canvas.drawString(100, y_position, line_item)
        y_position -= 20

    # Add totals
    pdf_canvas.drawString(100, y_position, "\nTotals:")
    y_position -= 20
    pdf_canvas.drawString(100, y_position, f"Total (Pre Tax): {invoice_data['total_pre_tax']}")
    y_position -= 20
    pdf_canvas.drawString(100, y_position, f"Tax: {invoice_data['tax']}")
    y_position -= 20
    pdf_canvas.drawString(100, y_position, f"Grand Total: {invoice_data['total']}")

    # Save the PDF
    pdf_canvas.save()

# Generate invoice data
invoice_data = generate_invoice_data()

# Generate PDF
create_invoice_pdf("invoice_with_details.pdf", invoice_data)
