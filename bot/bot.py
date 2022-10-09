import os
from dotenv import load_dotenv
import telebot
from sqlalchemy.orm import sessionmaker
from database import *

load_dotenv()

bot = telebot.TeleBot(os.getenv('TOKEN'))
engine = ENGINE
Session = sessionmaker(engine)
session = Session()

admins_arr = [1050696532]


def extract_arg(arg):
	return arg.split()[1:]


@bot.message_handler(commands=['start'])
def analyse(message):
	global admins_arr
	if message.text == "/start" and admins_arr.count(message.from_user.id) == 0:
		user = session.query(TeleusersAlanica).filter_by(teleid=message.from_user.id).first()
		if not user:
			user = TeleusersAlanica (
				teleid = message.from_user.id,
				username = message.from_user.username,
				f_name = message.from_user.first_name,
				l_name = message.from_user.last_name,
				language = message.from_user.language_code
			)
			session.add(user)
			session.commit()
			markup = telebot.types.ReplyKeyboardMarkup(row_width=2)
			markup.row("Технические проблемы", "Проблемы с оплатой")
			markup.row("Как это работает", "Другое")
			markup.row('Помощь в получении гражданства Болгарии, Венгрии, Румынии')
			markup.row('Междуныродные переводы юр. Лица')
			markup.row('Междуныродные переводы физ. Лица')
			markup.row('Оплата товаров услуг картами visa, MC, UnionPay, paypal')
			markup.row('Помощь в получение загранпаспорта Украины без выезда в Украину')
			markup.row('Украина (НДС)')
			inputName = bot.send_message(message.from_user.id, "Alanica на связи!🦄\nВыберите тему разговора из меню", reply_markup=markup)
			bot.register_next_step_handler(inputName, save_topic)
		else:
			markup = telebot.types.ReplyKeyboardMarkup(row_width=2)
			markup.row("Технические проблемы", "Проблемы с оплатой")
			markup.row("Как это работает", "Другое")
			markup.row('Помощь в получении гражданства Болгарии, Венгрии, Румынии')
			markup.row('Междуныродные переводы юр. Лица')
			markup.row('Междуныродные переводы физ. Лица')
			markup.row('Оплата товаров услуг картами visa, MC, UnionPay, paypal')
			markup.row('Помощь в получение загранпаспорта Украины без выезда в Украину')
			markup.row('Украина (НДС)')
			inputName = bot.send_message(message.from_user.id, "Alanica на связи!🦄\nВыберите тему разговора из меню", reply_markup=markup)
			bot.register_next_step_handler(inputName, save_topic)
	elif message.text == '/start' and admins_arr.count(message.from_user.id) == 1:
		user = session.query(TeleusersAlanica).filter_by(teleid=message.from_user.id).first()
		if not user:
			user = TeleusersAlanica (
				teleid = message.from_user.id,
				username = message.from_user.username,
				f_name = message.from_user.first_name,
				l_name = message.from_user.last_name,
				language = message.from_user.language_code,
			)
			session.add(user)
			session.commit()
			markup = telebot.types.ReplyKeyboardMarkup(row_width=2)
			markup.row("Ожидающие", "Завершить")
			bot.send_message(message.from_user.id, 'Добро пожаловать в команду поддержки!\nНажмите на кнопку <b>Ожидающие</b>, что бы посмотреть список вопросов и людей, которые ожидают ответа.\nНажмите на кнопку <b>Завершить</b>, что бы завершить разговор.', parse_mode='html', reply_markup=markup)
		else:
			markup = telebot.types.ReplyKeyboardMarkup(row_width=2)
			markup.row("Ожидающие", "Завершить")
			bot.send_message(message.from_user.id, 'Добро пожаловать в команду поддержки!\nНажмите на кнопку <b>Ожидающие</b>, что бы посмотреть список вопросов и людей, которые ожидают ответа.\nНажмите на кнопку <b>Завершить</b>, что бы завершить разговор.', parse_mode='html', reply_markup=markup)


def save_topic(message):
	try:
		inputName = bot.send_message(message.from_user.id, "Напишите, пожалуйста ваш вопрос мы всегда рады помочь🦄")
		bot.register_next_step_handler(inputName, your_questioin)
		session.query(TeleusersAlanica).filter(TeleusersAlanica.teleid == message.from_user.id).update({'topic': message.text})
		session.commit()
	except Exception:
		markup = telebot.types.ReplyKeyboardMarkup(row_width=2)
		markup.row("Технические проблемы", "Проблемы с оплатой")
		markup.row("Как это работает", "Другое")
		markup.row('Помощь в получении гражданства Болгарии, Венгрии, Румынии')
		markup.row('Междуныродные переводы юр. Лица')
		markup.row('Междуныродные переводы физ. Лица')
		markup.row('Оплата товаров услуг картами visa, MC, UnionPay, paypal')
		markup.row('Помощь в получение загранпаспорта Украины без выезда в Украину')
		markup.row('Украина (НДС)')
		bot.send_message(message.from_user.id, 'Alanica на связи!🦄\nВыберите тему разговора из меню', parse_mode='html', reply_markup=markup)


def your_questioin(message):
	global admins_arr
	markup = telebot.types.InlineKeyboardMarkup(row_width=1)
	activate = telebot.types.InlineKeyboardButton(text="✅Начать разговор✅", callback_data=f"select{message.from_user.id}")
	markup.add(activate)
	if message.from_user.id != None and message.text != "/start":
		user = session.query(TeleusersAlanica).filter_by(teleid=message.from_user.id).first()
		user.status = 'active'
		session.commit()
	else:
		inputName = bot.send_message(message.from_user.id, "Напишите, пожалуйста ваш вопрос мы обязательно вам поможем🦄")
		bot.register_next_step_handler(inputName, your_questioin)
	user = session.query(TeleusersAlanica).filter_by(teleid=message.from_user.id).first()
	if user.question != '0':
		user.question += f'\n {message.text}'
	else:
		user.question = f'{message.text}'
	
	msg = ''
	for admin in admins_arr:
		msg =  f'<b>📇ID:</b> <a href=\'tg://user?id={user.teleid}\'>{user.teleid}</a>\n'
		msg += f'<b>😎Имя: </b>{user.f_name}\n'
		msg += f'<b>💫Тема: </b>{user.topic}\n'
		msg += f'<b>📝Вопрос: </b>{user.question}'
		markup_select = telebot.types.InlineKeyboardMarkup(row_width=1)
		activate = telebot.types.InlineKeyboardButton(text="✅Помочь✅", callback_data=f"select{user.teleid}")
		markup_select.add(activate)
		bot.send_message(admin, "{0}".format(msg), reply_markup=markup_select, parse_mode='html')
	bot.send_message(message.from_user.id, "Спасибо, администратор свяжется с Вами в скором времени.")
	session.commit()


@bot.message_handler(content_types=["photo"])
def photo_sending(message):
	try:
		user = session.query(TeleusersAlanica).filter_by(teleid=message.from_user.id).first()
		if user:
			if (user.status == "busy" or user.status == "in_progress") and user.chat != "123":
				fileID = message.photo[-1].file_id
				file_info = bot.get_file(fileID)
				downloaded_file = bot.download_file(file_info.file_path)
				bot.send_photo(user.chat, downloaded_file)
	except Exception:
		pass

@bot.message_handler(content_types=['video'])
def sending_video(message):
	try:
		user = session.query(TeleusersAlanica).filter_by(teleid=message.from_user.id).first()
		if (user.status == "busy" or user.status == "in_progress") and user.chat != "123":
			fileID = message.video.file_id
			file_info = bot.get_file(fileID)
			downloaded_file = bot.download_file(file_info.file_path)
			bot.send_video(user.chat, downloaded_file, timeout=1000)
	except Exception:
		pass

@bot.message_handler(content_types=['document'])
def sending_document(message):
	try:
		user = session.query(TeleusersAlanica).filter_by(teleid=message.from_user.id).first()
		if (user.status == "busy" or user.status == "in_progress") and user.chat != "123":
			fileID = message.document.file_id
			file_info = bot.get_file(fileID)
			downloaded_file = bot.download_file(file_info.file_path)
			bot.send_document(user.chat, downloaded_file, timeout=1000)
	except Exception:
		pass

@bot.message_handler(content_types=['location'])
def sending_message(message):
	try:
		user = session.query(TeleusersAlanica).filter_by(teleid=message.from_user.id).first()
		if (user.status == "busy" or user.status == "in_progress") and user.chat != "123":
			fileID = message.location
			bot.send_message(user.chat, "longitude:{0}\nlatitude:{1}".format(fileID.longitude, fileID.latitude))
	except Exception:
		pass

@bot.message_handler(content_types=['sticker'])
def sticker_sending(message):
	try:
		user = session.query(TeleusersAlanica).filter_by(teleid=message.from_user.id).first()
		if (user.status == "busy" or user.status == "in_progress") and user.chat != "123":
			bot.send_sticker(user.chat, message.sticker.file_id)
	except Exception:
		pass


@bot.message_handler(content_types=['text'])
def answer_owner(message):
	global admins_arr
	user = session.query(TeleusersAlanica).filter_by(teleid=message.from_user.id).first()
	message_collect_id = ""
	if (user.status == "busy" or user.status == "in_progress") and message_collect_id == "" and message.text != "Завершить" and message.text != "Ожидающие":
		bot.send_message(user.chat, '{0}'.format(message.text))
	if 1==1:
		if message.text == "Ожидающие" and admins_arr.count(message.from_user.id) != 0:
			user_info = session.query(TeleusersAlanica).filter_by(status='active').all()
			msg = ''
			if len(user_info) != 0:
				for item in user_info:
					topic_get = item.topic
					if topic_get == 'Технические проблемы' or topic_get == 'Проблемы с оплатой' or topic_get == 'Как это работает' or topic_get == 'Другое':
						msg =  f'<b>📇ID:</b> <a href=\'tg://user?id={item.teleid}\'>{item.teleid}</a>\n'
						msg += f'<b>😎Имя: </b>{item.f_name}\n'
						msg += f'<b>💫Тема: </b>{item.topic}\n'
						msg += f'<b>📝Вопрос: </b>{item.question}'
						markup_select = telebot.types.InlineKeyboardMarkup(row_width=1)
						activate = telebot.types.InlineKeyboardButton(text="✅Помочь✅", callback_data=f"select{item.teleid}")
						markup_select.add(activate)
						bot.send_message(message.from_user.id, "{0}".format(msg), reply_markup=markup_select, parse_mode='html')
			else:
				bot.send_message(message.from_user.id, "Вы ответили на все вопросы".format(msg))
		elif message.text == "Завершить" and admins_arr.count(message.from_user.id) != 0:
			active_user = session.query(TeleusersAlanica).filter_by(teleid=user.chat).first()
			active_user.chat = '123'
			active_user.status = 'not_actual'
			active_user.question = '0'
			active_user.topic = '0'
			markup = telebot.types.ReplyKeyboardMarkup(row_width=2)
			markup.row("Ожидающие", "Завершить")
			try:
				bot.send_message(user.chat, "Было приятно с вами общатся💚!\nЖелаем наилучшего дня!\nСлужба поддержки .💪\n\nКак только возникнет любой вопрос,\nжмите на /start".format(message.from_user.first_name), parse_mode="html")
				bot.send_message(message.from_user.id, "Диалог завершен!", parse_mode="html", reply_markup=markup)
				user.status = 'free'
				user.chat = '123'
				session.commit()
			except Exception:
				bot.send_message(message.from_user.id, "У вас нет активных диалогов!", parse_mode="html", reply_markup=markup)
		if user.status == "active" and message.text != "Завершить" and message.text != "Ожидающие":
			if user.question != '0':
				user.question += f'\n {message.text}'
			else:
				user.question = f'{message.text}'
			session.commit()
			for item in admins_arr:
				bot.send_message(item, "<b>💚{0}:</b> \n📬{1}".format(message.from_user.first_name, message.text), parse_mode="html")


@bot.callback_query_handler(func=lambda call:True)
def start_conversation(call):
	global admins_arr
	if call.data[:6] == 'select':
		ask_user_id = call.data[6:]
		user = session.query(TeleusersAlanica).filter_by(teleid=ask_user_id).first()
		admin = session.query(TeleusersAlanica).filter_by(teleid=call.message.chat.id).first()
		if user.status == 'active':
			admin.status = 'busy'
			admin.chat = user.teleid
			user.status = 'in_progress'
			user.chat = admin.teleid
			session.commit()
			for item in admins_arr:
				bot.send_message(item, f"<a href=\'tg://user?id={user.teleid}\'><b>💚{user.teleid}:</b></a> \n📬Разговор начат с пользователем <a href=\'tg://user?id={ask_user_id}\'>{ask_user_id}</a>!", parse_mode="html")
			if user.f_name != '0':
				bot.send_message(ask_user_id, "Добрый день, {0}! Меня зовут Дмитрий, служба поддержки .💪".format(user.f_name), parse_mode="html")
			else:
				bot.send_message(int(ask_user_id), "Добрый день! Меня зовут Дмитрий, служба поддержки .💪", parse_mode="html")
		elif user.status == 'not_actual':
			bot.delete_message(call.message.chat.id, call.message.message_id)
			bot.send_message(call.message.chat.id, f'Разговор уже не актуален и завершен', parse_mode='html')
		elif user.status == 'in_progress':
			admin_active = user.chat
			bot.delete_message(call.message.chat.id, call.message.message_id)
			bot.send_message(call.message.chat.id, f'💪Разговор уже в прогрессе и начат администратором: <a href=\'tg://user?id={admin_active}\'>{admin_active}</a>', parse_mode='html')


while 1:
	try:
		bot.polling() 
	except Exception as e:
		print(e)
		os.system('python bot.py')