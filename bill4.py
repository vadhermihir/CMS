import json

def generate_invoice():
    invoice_data = {
        "invoice_details": {
            "title": "INVOICE",
            "invoice_number": "000000",
            "date_of_issue": "10/07/14",
            "invoice_total": 4520.00
        },
        "billed_to": {
            "client_name": "Client Name",
            "address": "1 Client Address",
            "city_state_country": "City, State, Country",
            "zip_code": "ZIP CODE"
        },
        "billed_from": {
            "company_name": "Not specified",
            "address": "1 Your Address",
            "city_state_country": "City, State, Country",
            "zip_code": "ZIP CODE",
            "phone_number": "647-444-1234",
            "email": "your@email.com",
            "website": "yourwebsite.com"
        },
        "items": [
            {"description": "Your item Name", "unit_cost": 1000, "qty": 1, "amount": 1000},
            {"description": "Your item Name", "unit_cost": 1000, "qty": 1, "amount": 1000},
            {"description": "Your item Name", "unit_cost": 1000, "qty": 1, "amount": 1000},
            {"description": "Your item Name", "unit_cost": 1000, "qty": 1, "amount": 1000}
        ],
        "totals": {
            "subtotal": 4000.00,
            "tax": 520.00,
            "grand_total": 4520.00
        }
    }
    return invoice_data

if __name__ == "__main__":
    invoice = generate_invoice()
    print(json.dumps(invoice, indent=4))
