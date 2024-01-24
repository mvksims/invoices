from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import random
import locale

def dictionary_to_inline_keyboard_markup(dictionary):
    keyboard = [[]]
    for key, value in dictionary.items():
        keyboard[0].append(InlineKeyboardButton(value, callback_data=key))
    result = InlineKeyboardMarkup(keyboard)
    return result

def wait_message():
    wait_messages = ["Wait!", "Moment!", "Sec!", "Pause!", "Hold!", "Quick!", "Chill!", "Easy!"]
    return random.choice(wait_messages)

def amount_to_words(currency):
    units = [
        "nulle", "viens", "divi", "trīs", "četri", "pieci",
        "seši", "septiņi", "astoņi", "deviņi"
    ]

    teens = [
        "desmit", "vienpadsmit", "divpadsmit", "trīspadsmit",
        "četrpadsmit", "piecpadsmit", "sešpadsmit", "septiņpadsmit",
        "astoņpadsmit", "deviņpadsmit"
    ]

    tens = [
        "", "", "divdesmit", "trīsdesmit", "četrdesmit", "piecdesmit",
        "sešdesmit", "septiņdesmit", "astoņdesmit", "deviņdesmit"
    ]

    thousands = [
        "", "tūkstotis", "miljons", "miljards", "triljons", "kvadriljons"
    ]

    # Helper function to convert a number less than 1000 to words
    def convert_less_than_thousand(num):
        result = ""

        hundreds_digit = num // 100
        remainder = num % 100

        if hundreds_digit > 0:
            result += f"{units[hundreds_digit]} simts "

        if remainder > 0:
            if remainder < 10:
                result += f"{units[remainder]}"
            elif remainder < 20:
                result += f"{teens[remainder - 10]}"
            else:
                tens_digit = remainder // 10
                ones_digit = remainder % 10

                result += f"{tens[tens_digit]} {units[ones_digit]}"

        return result

    # Convert the currency value to words
    words = ""

    # Split the currency value into integer and decimal parts
    integer_part, decimal_part = str(currency).split('.')

    # Convert the integer part to words
    integer_words = convert_less_than_thousand(int(integer_part))

    if not integer_words:
        words += "nulle"
    else:
        words += integer_words

    # Add currency unit
    words += " eiro"

    # Convert the decimal part to words if it exists
    if decimal_part:
        decimal_value = int(decimal_part)
        words += f" un {decimal_value} "
        if decimal_value == 1:
            words += "cents"
        else:
            words += "centi"

    return words

def format_currency(number, locale_str='nl_NL'):
    # Set the locale based on the input string (default is US English)
    locale.setlocale(locale.LC_ALL, locale_str)

    # Format the number as currency
    formatted_currency = locale.currency(number, symbol=False, grouping=True)

    # Reset the locale to the default value
    locale.setlocale(locale.LC_ALL, '')

    return formatted_currency

def extract_vat(amount, vat=1.21):
    if amount < 0 or vat <= 0:
        raise ValueError("Amount and VAT must be positive values.")

    vat_amount = amount / vat
    return vat_amount

def amount_without_vat(amount, vat=1.21):
    return amount - extract_vat(amount, vat)

