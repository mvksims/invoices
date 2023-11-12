import logging
from client import client_search_by_keyword
from ai import parse_client_details
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import filters, ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, CallbackQueryHandler

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

def dictionary_to_inline_keyboard_markup(dictionary):
    keyboard = [[]]
    for key, value in dictionary.items():
        keyboard[0].append(InlineKeyboardButton(value, callback_data=key))
    result = InlineKeyboardMarkup(keyboard)
    return result

def callback_to_controller(val):
    parts = val.split(':')

    if len(parts) != 2:
        raise ValueError("Invalid input string format. Expected 'key:value'.")

    result = {'action': parts[0].strip(), 'param_0': parts[1].strip()}
    
    return result

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['view'] = 'search'
    await context.bot.send_message(chat_id=update.effective_chat.id, text="What's client name?")

async def debug(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="user view: " + context.user_data['view'])

async def request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    view = context.user_data['view']
    if view == 'search':
        result = client_search_by_keyword(update.message.text)
        if result:
                await update.message.reply_text(
                    f"I found {len(result)-1} record. Select 'new' to save details for a new client",
                    reply_markup=dictionary_to_inline_keyboard_markup(result),
                )
        else:
            await context.bot.send_message(chat_id=update.effective_chat.id, text='No clients found')
    elif view == 'create_client':
        json = parse_client_details(update.message.text)
        print(json)
        await context.bot.send_message(chat_id=update.effective_chat.id, text=json)
    elif view == 'client':
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Generating invoice")
    else:
        print("I am a bit lost here :)")


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    controller = callback_to_controller(query.data)
    if controller['action'] == 'client':
        if controller['param_0'] == 'new':
            # create new
            context.user_data['view'] = 'create_client'
            await context.bot.send_message(chat_id=update.effective_chat.id, text="Please enter all nesesary data to create client profile")
        else:
            # set client
            context.user_data['view'] = 'client'
            context.user_data['client_id'] = controller['param_0']
            await context.bot.send_message(chat_id=update.effective_chat.id, text="Let's write new invoice. Write: product quantity price")

    await query.answer()
    print(f"button selected: {controller}")




if __name__ == '__main__':
    application = ApplicationBuilder().token('6336304373:AAG4zaeQ4EyejWNC59zzCid-i-odrKAtVP0').build()
    
    start_handler = CommandHandler('start', start)
    debug_handler = CommandHandler('debug', debug)
    request_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), request)

    application.add_handler(start_handler)
    application.add_handler(debug_handler)
    application.add_handler(request_handler)
    application.add_handler(CallbackQueryHandler(button))
    
    application.run_polling()