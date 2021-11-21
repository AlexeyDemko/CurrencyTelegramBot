import logging
import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, ConversationHandler, CallbackContext
from Parse_MyFin import get_currency_value, parse_myfin
import pandas as pd
from datetime import datetime

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

# Levels
FIRST, SECOND = range(2)
# Callback data
BUY, SELL, USD_BUY, EUR_BUY, RUB_BUY, USD_SELL, EUR_SELL, RUB_SELL, END = range(9)
# Back
BACK_BUY, BACK_SELL, START_OVER, STOPPING = range(4)
# Getting data from www.MyFin.by
initial_tables = parse_myfin()
df = pd.DataFrame(initial_tables[0])


# Primary choice menu
def start(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    logger.info("User %s started the conversation.", user.first_name)
    keyboard = [
        [
            InlineKeyboardButton("Покупка валюты", callback_data=str(BUY)),
            InlineKeyboardButton("Продажа валюты", callback_data=str(SELL)),

        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Привет, я Валютный Бот, выберите действие:", reply_markup=reply_markup)
    return FIRST


# Primary choice menu without "greeting phrase"
def start_over(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    query.answer()
    keyboard = [
        [
            InlineKeyboardButton("Покупка валюты", callback_data=str(BUY)),
            InlineKeyboardButton("Продажа валюты", callback_data=str(SELL)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(text="Выберите действие:", reply_markup=reply_markup)
    context.user_data[START_OVER] = False
    return FIRST


# First level
def process_first_level(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    query.answer()
    query_data = query.data
    if query_data == "0":
        keyboard = [
            [
                InlineKeyboardButton("USD", callback_data=str(USD_BUY)),
                InlineKeyboardButton("EUR", callback_data=str(EUR_BUY)),
                InlineKeyboardButton("RUB", callback_data=str(RUB_BUY)),
                InlineKeyboardButton(text='Назад', callback_data=str(END))
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.edit_message_text(
            text="Выберите валюту (покупка):", reply_markup=reply_markup
        )
    elif query_data == "1":
        keyboard = [
            [
                InlineKeyboardButton("USD", callback_data=str(USD_SELL)),
                InlineKeyboardButton("EUR", callback_data=str(EUR_SELL)),
                InlineKeyboardButton("RUB", callback_data=str(RUB_SELL)),
                InlineKeyboardButton(text='Back', callback_data=str(END))
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.edit_message_text(
            text="Выберите валюту (продажа):", reply_markup=reply_markup
        )
    return SECOND


# Second level
def process_second_level(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    query.answer()
    query_data = query.data
    keyboard = [
        [InlineKeyboardButton(text='Перейти к покупке валюты', callback_data=str(BACK_BUY))],
        [InlineKeyboardButton(text='Перейти к продаже валюты', callback_data=str(BACK_SELL))],
        [InlineKeyboardButton(text='Вернуться', callback_data=str(END))],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    print(update.callback_query.data)
    if query_data == "2":
        USD_BUY_VAR = get_currency_value(df=df, currency="Доллар США", operation="Покупка")
        query.edit_message_text(
            text="Курс покупки доллара США по состоянию на <b>{}</b> составляет: "
                 "<b>{}</b>".format(datetime.now().strftime("%d-%m-%Y %H:%M:%S"), USD_BUY_VAR),
            reply_markup=reply_markup, parse_mode=telegram.ParseMode.HTML
        )
    elif query_data == "3":
        EUR_BUY_VAR = get_currency_value(df=df, currency="Евро", operation="Покупка")
        query.edit_message_text(
            text="Курс покупки евро по состоянию на <b>{}</b> составляет: "
                 "<b>{}</b>".format(datetime.now().strftime("%d-%m-%Y %H:%M:%S"), EUR_BUY_VAR),
            reply_markup=reply_markup, parse_mode=telegram.ParseMode.HTML
        )
    elif query_data == "4":
        RUB_BUY_VAR = get_currency_value(df=df, currency="Российский рубль", operation="Покупка")
        query.edit_message_text(
            text="Курс покупки российского рубля (100) по состоянию на <b>{}</b> составляет: "
                 "<b>{}</b>".format(datetime.now().strftime("%d-%m-%Y %H:%M:%S"), RUB_BUY_VAR),
            reply_markup=reply_markup, parse_mode=telegram.ParseMode.HTML
        )
    elif query_data == "5":
        USD_SELL_VAR = get_currency_value(df=df, currency="Доллар США", operation="Продажа")
        query.edit_message_text(
            text="Курс продажи доллара США по состоянию на <b>{}</b> составляет: "
                 "<b>{}</b>".format(datetime.now().strftime("%d-%m-%Y %H:%M:%S"), USD_SELL_VAR),
            reply_markup=reply_markup, parse_mode=telegram.ParseMode.HTML
        )
    elif query_data == "6":
        EUR_SELL_VAR = get_currency_value(df=df, currency="Евро", operation="Продажа")
        query.edit_message_text(
            text="Курс продажи евро по состоянию на <b>{}</b> составляет: "
                 "<b>{}</b>".format(datetime.now().strftime("%d-%m-%Y %H:%M:%S"), EUR_SELL_VAR),
            reply_markup=reply_markup, parse_mode=telegram.ParseMode.HTML
        )
    elif query_data == "7":
        RUB_SELL_VAR = get_currency_value(df=df, currency="Российский рубль", operation="Продажа")
        query.edit_message_text(
            text="Курс продажи российского рубля (100) по состоянию на <b>{}</b> составляет: "
                 "<b>{}</b>".format(datetime.now().strftime("%d-%m-%Y %H:%M:%S"), RUB_SELL_VAR),
            reply_markup=reply_markup, parse_mode=telegram.ParseMode.HTML
        )
    return SECOND


# Back-button to the second level
def back_to_second_level(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    query.answer()
    process_first_level(update, context)
    print(update.callback_query.data)
    return SECOND


# End conversation
def stop(update, context):
    update.message.reply_text('Окей, до встречи!')
    return STOPPING


def main():
    updater = Updater("Token")
    dispatcher = updater.dispatcher
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            # First level ConversationHandler
            FIRST: [
                CallbackQueryHandler(process_first_level, pattern='^' + str(BUY) + '$'),
                CallbackQueryHandler(process_first_level, pattern='^' + str(SELL) + '$'),
            ],
            # Second level ConversationHandler
            SECOND: [
                CallbackQueryHandler(process_second_level, pattern='^' + str(USD_BUY) + '$'),
                CallbackQueryHandler(process_second_level, pattern='^' + str(EUR_BUY) + '$'),
                CallbackQueryHandler(process_second_level, pattern='^' + str(RUB_BUY) + '$'),
                CallbackQueryHandler(process_second_level, pattern='^' + str(USD_SELL) + '$'),
                CallbackQueryHandler(process_second_level, pattern='^' + str(EUR_SELL) + '$'),
                CallbackQueryHandler(process_second_level, pattern='^' + str(RUB_SELL) + '$'),
                CallbackQueryHandler(start_over, pattern='^' + str(END) + '$'),
                CallbackQueryHandler(back_to_second_level, pattern='^' + str(BACK_BUY) + '$'),
                CallbackQueryHandler(back_to_second_level, pattern='^' + str(BACK_SELL) + '$'),
            ],
        },
        fallbacks=[
            CommandHandler('start', start),
            CommandHandler('stop', stop),
        ],
        map_to_parent={
            STOPPING: STOPPING,
        }
    )
    dispatcher.add_handler(conv_handler)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
