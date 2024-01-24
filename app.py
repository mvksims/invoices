import os
import logging
from helpers import dictionary_to_inline_keyboard_markup, wait_message
from storage import find_client, save_client
from ai import parse_client, parse_lines
from invoice import create_pdf
from telegram import Update
from telegram.ext import filters, ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, CallbackQueryHandler

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

def callback_to_controller(val):
    parts = val.split(':')

    if len(parts) != 2:
        raise ValueError("Invalid input string format. Expected 'key:value'.")

    result = {'action': parts[0].strip(), 'param_0': parts[1].strip()}
    
    return result

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['view'] = 'search'
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Client's name, please?")

async def debug(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="user view: " + context.user_data['view'])

async def request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    view = context.user_data['view']
    # SEARCH
    if view == 'search':
        result = find_client(update.message.text)
        if result:
                await update.message.reply_text(
                    f"Found {len(result)-1} record. Select 'new' for a new client",
                    reply_markup=dictionary_to_inline_keyboard_markup(result)
                )
        else:
            action_buttons = {
                "client:new": "New Client",
            }
            await update.message.reply_text(
                text='Sorry, no clients found. Double-check your input or add a new client',
                reply_markup=dictionary_to_inline_keyboard_markup(action_buttons)
                )
    
    # CLIENT CREATE
    elif view == 'create_client':
        action_buttons = {
            "client:save": "Save",
            "client:new": "New",
        }

        await context.bot.send_message(chat_id=update.effective_chat.id, text=wait_message())
        result = parse_client(update.message.text)
        context.user_data['client'] = result

        message = "Confirm: \n"
        for key, value in result.items():
            message += f"{key}: {value}\n"
        await update.message.reply_text(
            message,
            reply_markup=dictionary_to_inline_keyboard_markup(action_buttons)
        )

    # CLIENT
    elif view == 'client':
        action_buttons = {
            "invoice:save": "Save",
            f"client:{context.user_data['client_id']}": "Cancel",
        }
        await context.bot.send_message(chat_id=update.effective_chat.id, text=wait_message())
        invoice = parse_lines(update.message.text)
        context.user_data['invoice'] = invoice
        message = "Confirm: \n"
        for item in invoice['items']:
            message += f"  - {item['line_item']} Qty: {item['quantity']}, Price/Unit: {item['unit_price']}, Line Total: {item['subtotal']} \n"

        message += f"Grand Total: {invoice['total']}"  
        await update.message.reply_text(
            message,
            reply_markup=dictionary_to_inline_keyboard_markup(action_buttons)
        )
    else:
        print("I am a bit lost here :)")

    print(f"request: {context.user_data}")

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    controller = callback_to_controller(query.data)
    if controller['action'] == 'client':
        if controller['param_0'] == 'new':
            # message: request new client details
            context.user_data['view'] = 'create_client'
            await context.bot.send_message(chat_id=update.effective_chat.id, text="Alright. Please provide all the necessary client data")
        elif controller['param_0'] == 'save':
            # client saved and selected
            # message: request product lines
            client_id = save_client(context.user_data['client'])
            await context.bot.send_message(chat_id=update.effective_chat.id, text="Saved!")
            # FIXME fetch client data and assing local vars
            # temporary solution for demo
            context.user_data['view'] = 'client'
            context.user_data['client_id'] = client_id   
            await context.bot.send_message(chat_id=update.effective_chat.id, text="OK. Send me the list the goods in the invoice. Example: 'Flowers 35' or 'Flowers 35, Delivery in Riga 20'.") 
        else:
            # client selected
            # message: request product lines
            context.user_data['view'] = 'client'
            context.user_data['client_id'] = controller['param_0']
            await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Client {controller['param_0']} selected!")
            await context.bot.send_message(chat_id=update.effective_chat.id, text="OK. Send me the list the goods in the invoice. Example: 'Flowers 35' or 'Flowers 35, Delivery in Riga 20'.")
    
    elif controller['action'] == 'invoice':
        if controller['param_0'] == 'save':

            create_pdf(context.user_data['client'], context.user_data['invoice'])
            await context.bot.send_document(chat_id=update.effective_chat.id, document='output.pdf')
            #await context.bot.send_message(chat_id=update.effective_chat.id, text="Invoice saved")

    await query.answer()
    print(f"context: {context.user_data}")
    print(f"button selected: {controller}")

if __name__ == '__main__':
    application = ApplicationBuilder().token(os.environ["TELEGRAM_API_KEY"]).build()
    
    start_handler = CommandHandler('start', start)
    debug_handler = CommandHandler('debug', debug)
    request_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), request)

    application.add_handler(start_handler)
    application.add_handler(debug_handler)
    application.add_handler(request_handler)
    application.add_handler(CallbackQueryHandler(button))
    
    application.run_polling()