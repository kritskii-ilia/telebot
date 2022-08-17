import config
import random
import telebot as tb
from telebot import types

bot = tb.TeleBot(config.token)

#keyboards
keyboard_want = types.InlineKeyboardMarkup()
key_want1 = types.InlineKeyboardButton(text='Хочу!', callback_data='want')
keyboard_want.add(key_want1)

keyboard_sub = types.InlineKeyboardMarkup()
key_sub1 = types.InlineKeyboardButton(text='Подписался', callback_data='done')
keyboard_sub.add(key_sub1)

keyboard_adm = types.InlineKeyboardMarkup()
key_adm1 = types.InlineKeyboardButton(text='Спонсоры', callback_data='sponsors')
key_adm2 = types.InlineKeyboardButton(text='Разыграть', callback_data='play out')
key_adm3 = types.InlineKeyboardButton(text='Block list', callback_data='block list')
key_adm4 = types.InlineKeyboardButton(text='Участники', callback_data='participants')
key_adm5 = types.InlineKeyboardButton(text='Пользователи', callback_data='users')
key_adm6 = types.InlineKeyboardButton(text='Админы', callback_data='admins')
keyboard_adm.add(key_adm1, key_adm2, key_adm3, key_adm4, key_adm5, key_adm6)

keyboard_block = types.InlineKeyboardMarkup()
key_block1 = types.InlineKeyboardButton(text='Забанить', callback_data='ban')
key_block2 = types.InlineKeyboardButton(text='Разбанить', callback_data='unban')
key_block3 = types.InlineKeyboardButton(text='Список', callback_data='block_list list')
keyboard_block.add(key_block3, key_block1, key_block2)

keyboard_sponsors = types.InlineKeyboardMarkup()
key_spon1 = types.InlineKeyboardButton(text='Список', callback_data='sponsors_list')
key_spon2 = types.InlineKeyboardButton(text='Редактировать', callback_data='edit')
keyboard_sponsors.add(key_spon1, key_spon2)

keyboard_users = types.InlineKeyboardMarkup()
key_users1 = types.InlineKeyboardButton(text='Количество', callback_data='users_count')
key_users2 = types.InlineKeyboardButton(text='Список', callback_data='users_list')
keyboard_users.add(key_users1, key_users2)

keyboard_admins = types.InlineKeyboardMarkup()
key_admins1 = types.InlineKeyboardButton(text='Список', callback_data='admins_list')
key_admins2 = types.InlineKeyboardButton(text='Добавить', callback_data='add_admin')
key_admins3 = types.InlineKeyboardButton(text='Удалить', callback_data='remove_admin')
keyboard_admins.add(key_admins1, key_admins2, key_admins3)

#massives
participants = []  #участники
part_only = []  #участники
part_check = []
users = []  #все пользователи
dict = {}
admins = ['791866049']

block_list = []

sponsors = []

member = ""

@bot.message_handler(commands=['start', 'admin', 'rules', 'help'])
def command_message(message):
    if message.text == '/start':
        if str(message.chat.id) in block_list:
            bot.send_message(message.chat.id, 'Вы забанены. Для разрешения вопроса пишите ему - @loydstop')
        elif str(message.chat.username) == 'None':
            users_true = []
            for i in range(len(users)):
                if str(message.chat.id) != users[i][0]:
                    users_true.append(False)
                else:
                    users_true.append(True)
            if True in users_true:
                pass
            else:
                row = str(message.chat.id), 'None'
                users.append(row)
            bot.send_message(message.chat.id, 'Привет ' + message.chat.first_name + ', я бот, который проводит раздачи для подписчиков на наших спонсоров.')
            bot.send_message(message.chat.id, text='Хочешь поучаствовать в нашем движе?', reply_markup=keyboard_want)
        else:
            users_true = []
            for i in range(len(users)):
                if str(message.chat.id) != users[i][0]:
                    users_true.append(False)
                else:
                    users_true.append(True)
            if True in users_true:
                pass
            else:
                row = str(message.chat.id), '@' + str(message.chat.username)
                users.append(row)
            bot.send_message(message.chat.id, 'Привет ' + message.chat.first_name + ', я бот, который проводит раздачи для подписчиков на наших спонсоров.')
            bot.send_message(message.chat.id, text='Хочешь поучаствовать в нашем движе?', reply_markup=keyboard_want)

    elif message.text == "/admin":
        admins_true = []
        for adm in admins:
            if adm == str(message.chat.id):
                admins_true.append(True)
            else:
                admins_true.append(False)
        if True in admins_true:
            bot.send_message(message.chat.id, text='Добро пожаловать, милорд', reply_markup=keyboard_adm)
        else:
            bot.send_message(message.chat.id, 'У вас недостаточно прав')

    elif message.text == '/help':
        bot.send_message(message.chat.id, text='По всем вопросам писать ему \n @loydstop')

@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == "want":
        if str(call.message.chat.id) in block_list:
            bot.send_message(call.message.chat.id, 'Вы забанены. Для разрешения вопроса пишите ему - @loydstop')
        elif str(sponsors) == '[]':
            bot.send_message(call.message.chat.id, 'Список спонсоров пуст')
        else:
            bot.send_message(call.message.chat.id, 'Отлично, тогда подпишись на данные каналы: \n' \
                  + '\n'.join(sponsors))
            bot.send_message(call.message.chat.id, 'Когда подпишешься на все каналы, бей по кнопке', reply_markup=keyboard_sub)

    elif call.data == "done":
        if str(call.message.chat.id) in block_list:
            bot.send_message(call.message.chat.id, 'Вы забанены. Для разрешения вопроса пишите ему - @loydstop')
        else:
            def status_checker(statuss):
                true_list = []
                for spon in sponsors:
                    if statuss == bot.get_chat_member(chat_id=spon, user_id=call.message.chat.id).status:
                        true_list.append(True)
                    else:
                        true_list.append(False)
                if False in true_list:
                    bot.send_message(call.message.chat.id, 'Вы подписались не на все каналы!')
                else:
                    if str(call.from_user.username) == 'None':
                        if str(call.from_user.id) in part_only:
                            bot.send_message(call.from_user.id, 'Ты уже участвуешь Проверяй результаты на канале @takeyourcash')
                        else:
                            part_only.append(str(call.from_user.id))
                            participants.append('c id ' + str(call.from_user.id))
                            dict.update({str(call.from_user.id): 'None'})
                            bot.send_message(call.message.chat.id, 'Ты участвуешь. Проверяй результаты на канале @takeyourcash')
                    else:
                        if '@' + str(call.from_user.username) in part_only:
                            bot.send_message(call.from_user.id, 'Ты уже участвуешь. \nПроверяй результаты на канале @takeyourcash')
                        else:
                            part_only.append('@' + str(call.from_user.username))
                            participants.append("@" + str(call.from_user.username))
                            dict.update({str(call.from_user.id): '@' + str(call.from_user.username)})
                            bot.send_message(call.message.chat.id, 'Ты участвуешь. Проверяй результаты на канале @takeyourcash')
            status_checker("member")

    elif call.data == 'block list':
        bot.send_message(call.message.chat.id, 'Выберите действие', reply_markup=keyboard_block)

    elif call.data == 'block_list list':
        if len(block_list) == 0:
            bot.send_message(call.message.chat.id, 'Забаненых нет')
        else:
            bot.send_message(call.message.chat.id, 'Забанено пользователей - ' + str(len(block_list)))
            block_msg = ""
            for i in range(0, len(block_list)):
                block_msg += str(i + 1) + ') ' + str(block_list[i]) + '\n'
                i += 1
            bot.send_message(call.message.chat.id, block_msg)

    elif call.data == 'ban':
        bot.send_message(call.message.chat.id, 'Введите id пользователя')
        bot.register_next_step_handler(call.message, ban)

    elif call.data == 'unban':
        bot.send_message(call.message.chat.id, 'Введите id пользователя')
        bot.register_next_step_handler(call.message, unban)

    elif call.data == 'participants':
        if len(participants) == 0:
            bot.send_message(call.message.chat.id, 'Участников нет')
        else:
            bot.send_message(call.message.chat.id, 'Участников - '+str(len(part_only)))
            part_msg = ""
            for i in range(0, len(part_only)):
                part_msg += str(i+1) + ') ' + str(part_only[i]) + '\n'
                i += 1
            bot.send_message(call.message.chat.id, part_msg)

    elif call.data == 'play out':
        if len(dict) == 0:
            bot.send_message(call.message.chat.id, 'Список участников пуст')
        else:
            def part_checker(statuss):
                true_checker = []
                for key in dict:
                    for spon in sponsors:
                        if statuss == bot.get_chat_member(chat_id=spon, user_id=key).status:
                            true_checker.append(True)
                        else:
                            true_checker.append(False)
                    if False in true_checker:
                        pass
                    else:
                        if str(dict[key]) == 'None':
                            part_check.append('c id ' + str(key))
                        else:
                            part_check.append(dict[key])
            part_checker("member")
            if len(part_check) == 0:
                bot.send_message('@takeyourcash', 'Победителей нет, так как никто из участников не выполнил все условия')
            else:
                winner = str(random.choice(part_check))
                bot.send_message('@takeyourcash', 'Победителем сегодняшнего розыгрыша стал пользователь ' + winner + '\nНапиши нашему админу @loydstop, чтобы получить выигрыш ')
                dict.clear()
                part_check.clear()
                participants.clear()
                part_only.clear()
                part_check.clear()

    elif call.data == 'users':
        bot.send_message(call.message.chat.id, 'Выберите действие', reply_markup=keyboard_users)

    elif call.data == 'users_count':
        bot.send_message(call.message.chat.id, 'Пользователей - ' + str(len(users)))

    elif call.data == 'users_list':
        if str(users) == '[]':
            bot.send_message(call.message.chat.id, 'Список пользователей пуст')
        else:
            users_msg = ""
            for i in range(0, len(users)):
                users_msg += str(i + 1) + ')  ' + str(users[i][0]) + ' - ' + str(users[i][1]) + '\n'
                i += 1
            bot.send_message(call.message.chat.id, users_msg)

    elif call.data == 'sponsors':
        bot.send_message(call.message.chat.id, 'Выберите действие', reply_markup=keyboard_sponsors)

    elif call.data == 'sponsors_list':
        if str(sponsors) == '[]':
            bot.send_message(call.message.chat.id, 'Список спонсоров пуст')
        else:
            sponsors_msg = ""
            for i in range(0, len(sponsors)):
                sponsors_msg += str(i + 1) + ') ' + str(sponsors[i]) + '\n'
                i += 1
            bot.send_message(call.message.chat.id, sponsors_msg)

    elif call.data == 'edit':
        sponsors.clear()
        bot.send_message(call.message.chat.id, 'Введите спонсоров')
        bot.register_next_step_handler(call.message, get_sponsors)

    elif call.data == 'admins':
        bot.send_message(call.message.chat.id, 'Выберите действие', reply_markup=keyboard_admins)

    elif call.data == 'admins_list':
        admins_msg = ""
        for i in range(0, len(admins)):
            admins_msg += str(i + 1) + ') ' + str(admins[i]) + '\n'
            i += 1
        bot.send_message(call.message.chat.id, admins_msg)

    elif call.data == 'add_admin':
        bot.send_message(call.message.chat.id, 'Введите id пользователя')
        bot.register_next_step_handler(call.message, add_admin)

    elif call.data == 'remove_admin':
        bot.send_message(call.message.chat.id, 'Введите id пользователя')
        bot.register_next_step_handler(call.message, remove_admin)


def get_sponsors(message):
    global sponsors
    bot.send_message(message.chat.id, 'Спонсоры изменены')
    sponsors = message.text.split()

def ban(message):
    if str(message.text) in block_list:
        bot.send_message(message.chat.id, 'Пользователь уже забанен')
    else:
        block_list.append(message.text)
    bot.send_message(message.chat.id, 'Пользователь забанен')

def unban(message):
    if str(message.text) in block_list:
        block_list.remove(message.text)
        bot.send_message(message.chat.id, 'Пользователь разбанен')
    else:
        bot.send_message(message.chat.id, 'Пользователь уже разбанен')

def add_admin(message):
    if str(message.text) in admins:
        bot.send_message(message.chat.id, 'Пользователь уже админ')
    else:
        admins.append(str(message.text))
        bot.send_message(message.chat.id, 'Пользователь добавлен в администраторы')

def remove_admin(message):
    if str(message.text) in admins:
        admins.remove(str(message.text))
    else:
        bot.send_message(message.chat.id, 'Пользователь не был администратором')

bot.polling()