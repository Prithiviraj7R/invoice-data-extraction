import yaml # type: ignore
import re
import sys

from src.utils.exception import CustomException
from src.utils.logger import logging

def parse_text(text: str):
    """
    Parses the text extracted from a PDF file.
    :param text: Text extracted from the PDF file.
    :return: Parsed information from the text.
    """

    parsed_info = {}
    yaml_output = ""

    try:
        logging.info("Parsing the text extracted from the PDF file.")

        # extract the recipient information
        recipient_search = re.search(r"^(.*?)\nGSTIN (\S+)\s+C/o (.+?)\n(.*?)\nMobile (.+?)\s+Email (.+?)\n", text, re.DOTALL | re.MULTILINE)
        if recipient_search:
            recipient_info = {
                "name": recipient_search.group(1).strip(),
                "gstin": recipient_search.group(2),
                "address": recipient_search.group(3),
                "city": recipient_search.group(4).split(",")[-2].strip(),
                "state": recipient_search.group(4).split(",")[-1].strip(),
                "contact": {
                    "mobile": recipient_search.group(5),
                    "email": recipient_search.group(6)
                }
            }

            parsed_info["recipient"] = recipient_info


        # extract the invoice information

        invoice_details_match = re.search(r"Invoice #: (\S+) Invoice Date: (\d{2} \w+ \d{4}) Due Date: (\d{2} \w+ \d{4})", text)
        if invoice_details_match:
            invoice_info = {
                'invoice_number': invoice_details_match.group(1),
                'invoice_date': invoice_details_match.group(2),
                'due_date': invoice_details_match.group(3)
            }

            parsed_info["invoice"] = invoice_info

            
        # extract the customer information

        customer_details_match = re.search(r"Customer Details:\n(.+?)\n", text)
        place_of_supply_match = re.search(r"Place of Supply:\s*(\d{2})-(.+?)\n", text)

        customer_info = {}
        if customer_details_match:
            customer_info = {
                'name': customer_details_match.group(1).strip(),
            }

        if place_of_supply_match:
            customer_info["place_of_supply"] = {
                'state_code': place_of_supply_match.group(1),
                'state': place_of_supply_match.group(2).strip()
            }

        parsed_info["customer"] = customer_info


        # extract the item information
        
        items = []
        items_start_match = re.search(r"#Item Rate / Item QtyTaxable ValueTax AmountAmount", text)
        items_end_match = re.search(r"Taxable Amount", text)

        if items_start_match and items_end_match:
            items_text = text[items_start_match.end():items_end_match.start()].strip()
            
            lines = items_text.split("\n")
            num_items = len(lines)//2

            items = []
            for i in range(num_items):
                info_part1 = lines[2*i]
                info_part2 = lines[2*i + 1]

                match1 = re.match(r"(\d)(.*?)([\d,]+\.\d+)$", info_part1.strip())
                match2 = re.match(r"([\d,]+\.\d+)\s+\(([-\d]+)%\)(\d+)\s+(\w+)([\d,]+\.\d+)([\d,]+\.\d+)\s+\((\d+)%\)([\d,]+\.\d+)", info_part2.strip())

                item_info = {}

                if match1:
                    item_info.update({
                        "item_number": match1.group(1),
                        "item_name": match1.group(2).strip(),
                        "rate_per_item": float(match1.group(3).replace(',', ''))  # Remove commas before converting
                    })

                if match2:
                    item_info.update({
                        "actual_price": float(match2.group(1).replace(',', '')),
                        "discount": float(match2.group(2)),
                        "quantity": float(match2.group(3)),
                        "unit": match2.group(4),
                        "taxable_value": float(match2.group(5).replace(',', '')),
                        "tax_amount_with_percentage": f"{match2.group(6)} ({match2.group(7)}%)",
                        "amount": float(match2.group(8).replace(',', ''))
                    })
                    
                items.append(item_info)   

            parsed_info["items"] = items

        # extract the total information

        totals_match = re.search(r"Taxable Amount ₹(\d+\.\d+)\nCGST 6.0% ₹(\d+\.\d+)\nSGST 6.0% ₹(\d+\.\d+)\nCGST 9.0% ₹(\d+\.\d+)\nSGST 9.0% ₹(\d+\.\d+)\nRound Off (\d+\.\d+)\nTotal₹(\d+\.\d+)\nTotal Discount ₹(\d+\.\d+)\nTotal Items / Qty : (\d+) / (\d+\.\d+)", text)
        if totals_match:
            total_info = {
                'taxable_amount': float(totals_match.group(1)),
                'cgst_6_percent': float(totals_match.group(2)),
                'sgst_6_percent': float(totals_match.group(3)),
                'cgst_9_percent': float(totals_match.group(4)),
                'sgst_9_percent': float(totals_match.group(5)),
                'round_off': float(totals_match.group(6)),
                'total_amount': float(totals_match.group(7)),
                'total_discount': float(totals_match.group(8)),
                'total_items': {
                    'count': int(totals_match.group(9)),
                    'quantity': float(totals_match.group(10))
                },
                'amount_in_words': re.search(r"Total amount \(in words\):\s+(.*?)\.", text).group(1).strip()
            }

            parsed_info["total"] = total_info

        # extract the payment information

        payment_details_match = re.search(r"Bank:\s*(.+?)\nAccount #:\s*(\S+)\nIFSC Code:\s*(\S+)\nBranch:\s*(.+?)\n", text)
        if payment_details_match:
            paymeny_info = {
                'payment_method': 'UPI',
                'bank_details': {
                    'bank': payment_details_match.group(1).strip(),
                    'account_number': payment_details_match.group(2).strip(),
                    'ifsc_code': payment_details_match.group(3).strip(),
                    'branch': payment_details_match.group(4).strip()
                }
            }

            parsed_info["payment"] = paymeny_info


        # extract the authorisation information
        authorisation_info = {
            'signatory': "Authorized Signatory",
            'note': "This is a computer-generated document and requires no signature."
        }

        logging.info("Text extracted from the PDF file has been parsed successfully.")

        parsed_info["authorisation"] = authorisation_info

        yaml_output = yaml.dump(parsed_info, sort_keys=False)

        logging.info("Parsed information has been converted to YAML format.")

    except Exception as e:
        raise CustomException(e, sys)
    
    return yaml_output


    