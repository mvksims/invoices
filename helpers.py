from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import random

def dictionary_to_inline_keyboard_markup(dictionary):
    keyboard = [[]]
    for key, value in dictionary.items():
        keyboard[0].append(InlineKeyboardButton(value, callback_data=key))
    result = InlineKeyboardMarkup(keyboard)
    return result

def wait_message():
    wait_messages = ["Wait!", "Moment!", "Sec!", "Pause!", "Hold!", "Quick!", "Chill!", "Easy!"]
    return random.choice(wait_messages)