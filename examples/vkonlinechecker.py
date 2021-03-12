from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

import sqlite3
from sqlite3 import Error

def create_connection(path):
    connection = None
    try:
        connection = sqlite3.connect(path)
        print("Connection to SQLite DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection

############################### Bot ############################################
def start(update, context):
  update.message.reply_text(main_menu_message(),
                            reply_markup=main_menu_keyboard())

def main_menu(update,context):
  query = update.callback_query
  query.answer()
  query.edit_message_text(
                        text=main_menu_message(),
                        reply_markup=main_menu_keyboard())

def profile_menu(update,context):
  query = update.callback_query
  query.answer()
  query.edit_message_text(
                        text=profile_menu_message(),
                        reply_markup=profile_menu_keyboard())

def buySubscription_menu(update,context):
  query = update.callback_query
  query.answer()
  query.edit_message_text(
                        text=buySubscription_menu_message(),
                        reply_markup=buySubscription_menu_keyboard())

def tracking_menu(update,context):
  query = update.callback_query
  query.answer()
  query.edit_message_text(
                        text=tracking_menu_message(),
                        reply_markup=tracking_menu_keyboard())

def tracking_vk_menu(update,context):
  query = update.callback_query
  query.answer()
  query.edit_message_text(
                        text=tracking_vk_menu_message(),
                        reply_markup=tracking_vk_menu_keyboard())

def tracking_vk_add_menu(update,context):
  query = update.callback_query
  query.answer()
  query.edit_message_text(
                        text=tracking_vk_add_menu_message(),
                        reply_markup=tracking_vk_add_menu_keyboard())

def tracking_vk_del_menu(update,context):
  query = update.callback_query
  query.answer()
  query.edit_message_text(
                        text=tracking_vk_del_menu_message(),
                        reply_markup=tracking_vk_del_menu_keyboard())

def tracking_vk_clear_menu(update,context):
  query = update.callback_query
  query.answer()
  query.edit_message_text(
                        text=tracking_vk_clear_menu_message(),
                        reply_markup=tracking_vk_clear_menu_keyboard())

def tracking_vk_stop_menu(update,context):
  query = update.callback_query
  query.answer()
  query.edit_message_text(
                        text=tracking_vk_stop_menu_message(),
                        reply_markup=tracking_vk_stop_menu_keyboard())

def tracking_vk_start_menu(update,context):
  query = update.callback_query
  query.answer()
  query.edit_message_text(
                        text=tracking_vk_start_menu_message(),
                        reply_markup=tracking_vk_start_menu_keyboard())

def tracking_inst_menu(update,context):
  query = update.callback_query
  query.answer()
  query.edit_message_text(
                        text=tracking_inst_menu_message(),
                        reply_markup=tracking_inst_menu_keyboard())

def analysis_menu(update,context):
  query = update.callback_query
  query.answer()
  query.edit_message_text(
                        text=analysis_menu_message(),
                        reply_markup=analysis_menu_keyboard())

def analysis_vk_menu(update,context):
  query = update.callback_query
  query.answer()
  query.edit_message_text(
                        text=analysis_vk_menu_message(),
                        reply_markup=analysis_vk_menu_keyboard())

def analysis_inst_menu(update,context):
  query = update.callback_query
  query.answer()
  query.edit_message_text(
                        text=analysis_inst_menu_message(),
                        reply_markup=analysis_inst_menu_keyboard())

# and so on for every callback_data option

############################ Keyboards #########################################
def main_menu_keyboard():
  keyboard = [[InlineKeyboardButton('Профиль', callback_data='profile')],
              [InlineKeyboardButton('Отслеживание', callback_data='tracking')],
              [InlineKeyboardButton('Анализ', callback_data='analysis')],
              [InlineKeyboardButton('Купить подписку', callback_data='buySubscription')]]
  return InlineKeyboardMarkup(keyboard)

def profile_menu_keyboard():
  keyboard = [[InlineKeyboardButton('Купить подписку', callback_data='buySubscription')],
              [InlineKeyboardButton('<- Назад', callback_data='main')]]
  return InlineKeyboardMarkup(keyboard)

def tracking_menu_keyboard():
  keyboard = [[InlineKeyboardButton('VK', callback_data='vkTracking')],
            [InlineKeyboardButton('Instagram', callback_data='instTracking')],
            [InlineKeyboardButton('<- Назад', callback_data='main')]]
  return InlineKeyboardMarkup(keyboard)

def tracking_vk_menu_keyboard():
  keyboard = [[InlineKeyboardButton('Добавить аккаунт', callback_data='vkAddTracking')],
            [InlineKeyboardButton('Удалить аккаунт', callback_data='vkDelTracking')],
            [InlineKeyboardButton('Очистить все', callback_data='vkClearTracking')],
            [InlineKeyboardButton('Остановить отслеживание', callback_data='vkStopTracking')],
            [InlineKeyboardButton('Начать отслеживание', callback_data='vkStartTracking')],
            [InlineKeyboardButton('<- Назад', callback_data='tracking')]]
  return InlineKeyboardMarkup(keyboard)

def tracking_vk_add_menu_keyboard():
  keyboard = [[InlineKeyboardButton('<- Назад', callback_data='vkTracking')]]
  return InlineKeyboardMarkup(keyboard)

def tracking_vk_del_menu_keyboard():
  keyboard = [[InlineKeyboardButton('<- Назад', callback_data='vkTracking')]]
  return InlineKeyboardMarkup(keyboard)

def tracking_vk_clear_menu_keyboard():
  keyboard = [[InlineKeyboardButton('Очистить все', callback_data='clear_vk')],
              [InlineKeyboardButton('<- Назад', callback_data='vkTracking')]]
  return InlineKeyboardMarkup(keyboard)

def tracking_vk_stop_menu_keyboard():
  keyboard = [[InlineKeyboardButton('Остановить', callback_data='stop_vk')],
              [InlineKeyboardButton('<- Назад', callback_data='vkTracking')]]
  return InlineKeyboardMarkup(keyboard)

def tracking_vk_start_menu_keyboard():
  keyboard = [[InlineKeyboardButton('Старт', callback_data='start_vk')],
              [InlineKeyboardButton('<- Назад', callback_data='vkTracking')]]
  return InlineKeyboardMarkup(keyboard)

def tracking_inst_menu_keyboard():
  keyboard = [[InlineKeyboardButton('Добавить', callback_data='instAddTracking')],
            [InlineKeyboardButton('Удалить аккаунт', callback_data='instDelTracking')],
            [InlineKeyboardButton('Очистить все', callback_data='instClearTracking')],
            [InlineKeyboardButton('Остановить отслеживание', callback_data='instStopTracking')],
            [InlineKeyboardButton('Начать отслеживание', callback_data='instStartTracking')],
            [InlineKeyboardButton('<- Назад', callback_data='tracking')]]
  return InlineKeyboardMarkup(keyboard)

def analysis_menu_keyboard():
  keyboard = [[InlineKeyboardButton('VK', callback_data='vkAnalysis')],
            [InlineKeyboardButton('Instagram', callback_data='instAnalysis')],
            [InlineKeyboardButton('<- Назад', callback_data='main')]]
  return InlineKeyboardMarkup(keyboard)

def analysis_vk_menu_keyboard():
  keyboard = [[InlineKeyboardButton('<- Назад', callback_data='analysis')]]
  return InlineKeyboardMarkup(keyboard)

def analysis_inst_menu_keyboard():
  keyboard = [[InlineKeyboardButton('<- Назад', callback_data='analysis')]]
  return InlineKeyboardMarkup(keyboard)

def buySubscription_menu_keyboard():
  keyboard = [[InlineKeyboardButton('<- Назад', callback_data='main')]]
  return InlineKeyboardMarkup(keyboard)

############################# Messages #########################################
def main_menu_message():
    result = '*Название бота* - бот-детектив\n\n'
    result +='Найти поклонников, отследить активность пользователя, а также анализировать последнии действия друзей/подписчиков.\n'
    result +='Все в ваших руках.\n'
    result +='Бот отсведомляет и хранит информацию об изменениях в профилях отслеживаемых пользователей.\n\n'
    result +='Плюсом будет являться ваша анонимность)\n\n'
    result +='Пошарьте меню, может вам интересно, кто лайкает вашу половинку или друга...'
    return result

def profile_menu_message():
  return 'Инфа о профиле...'

def buySubscription_menu_message():
  return 'Функция покупки подписки пока недоступна..'

def tracking_menu_message():
  return 'Инфа по отслеживаемым аккаунтам...'

def tracking_vk_menu_message():
  return 'Инфа по анализу аккаунтов вк...'

def tracking_inst_menu_message():
  return 'Инфа по анализу аккаунтов инсты...'

def tracking_vk_add_menu_message():
  return 'Чтобы добавить отслеживаемый аккаунт, введите команду: \n"/add_vk *ссылка на пользователя*"'

def tracking_vk_del_menu_message():
  return 'Чтобы удалить отслеживаемый аккаунт, введите команду "/del_vk *ссылка на пользователя*"'

def tracking_vk_clear_menu_message():
  return 'Чтобы очистить список отслеживаемых аккаунтов, нажмите на кнопку "Очистить все" или введите команду /clear_vk' \
         '\n\n' \
         '(Отслеживание будет остановлено)'

def tracking_vk_stop_menu_message():
  return 'Чтобы остановить отслеживание аккаунтов, нажмите на кнопку "Остановить" или введите команду /stop_vk'

def tracking_vk_start_menu_message():
  return 'Чтобы начать отслеживание аккаунтов, нажмите на кнопку "Старт" или введите команду /start_vk'

def analysis_menu_message():
  return 'Инфа по анализу аккаунтов...'

def analysis_vk_menu_message():
  return 'Инфа по анализу аккаунтов вк...'

def analysis_inst_menu_message():
  return 'Инфа по анализу аккаунтов инсты...'


def main():
    ############################# Handlers #########################################
    updater = Updater("1517729956:AAEo8WdIFETkzKx-EGCmAVh3QT1GWvzbNis", use_context=True)

    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CallbackQueryHandler(main_menu, pattern='main'))
    updater.dispatcher.add_handler(CallbackQueryHandler(profile_menu, pattern='profile'))
    updater.dispatcher.add_handler(CallbackQueryHandler(buySubscription_menu, pattern='buySubscription'))
    updater.dispatcher.add_handler(CallbackQueryHandler(tracking_menu, pattern='tracking'))
    updater.dispatcher.add_handler(CallbackQueryHandler(tracking_vk_menu, pattern='vkTracking'))
    updater.dispatcher.add_handler(CallbackQueryHandler(tracking_inst_menu, pattern='instTracking'))
    updater.dispatcher.add_handler(CallbackQueryHandler(analysis_menu, pattern='analysis'))
    updater.dispatcher.add_handler(CallbackQueryHandler(analysis_vk_menu, pattern='vkAnalysis'))
    updater.dispatcher.add_handler(CallbackQueryHandler(analysis_inst_menu, pattern='instAnalysis'))
    updater.dispatcher.add_handler(CallbackQueryHandler(tracking_vk_add_menu, pattern='vkAddTracking'))
    updater.dispatcher.add_handler(CallbackQueryHandler(tracking_vk_del_menu, pattern='vkDelTracking'))
    updater.dispatcher.add_handler(CallbackQueryHandler(tracking_vk_clear_menu, pattern='vkClearTracking'))
    updater.dispatcher.add_handler(CallbackQueryHandler(tracking_vk_stop_menu, pattern='vkStopTracking'))
    updater.dispatcher.add_handler(CallbackQueryHandler(tracking_vk_start_menu, pattern='vkStartTracking'))
    #updater.dispatcher.add_handler(CallbackQueryHandler(tracking_inst_add_menu, pattern='instAddTracking'))
    #updater.dispatcher.add_handler(CallbackQueryHandler(tracking_inst_del_menu, pattern='instDelTracking'))
    #updater.dispatcher.add_handler(CallbackQueryHandler(tracking_inst_clear_menu, pattern='instClearTracking'))
    #updater.dispatcher.add_handler(CallbackQueryHandler(tracking_inst_stop_menu, pattern='vkStopTracking'))
    #updater.dispatcher.add_handler(CallbackQueryHandler(tracking_inst_start_menu, pattern='instStartTracking'))

    updater.start_polling()

if __name__ == '__main__':
    main()