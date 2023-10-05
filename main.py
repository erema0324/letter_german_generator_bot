import re
import logging
import io
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.types import ParseMode
from aiogram.utils import executor
from aiogram.utils.callback_data import CallbackData
from aiogram.utils.markdown import text, escape_md
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet
from aiogram.utils.exceptions import MessageToEditNotFound
from aiogram.types.input_file import InputFile
from export_utils import export_to_pdf, export_to_word
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from connect import SQLighter


import config
import messages
from gpt3 import generate_letter
from export_utils import export_to_pdf, export_to_word

bot = Bot(token=config.TELEGRAM_API_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

logging.basicConfig(level=logging.INFO)

language_cb = CallbackData("lang", "code")
letter_type_cb = CallbackData("type", "code")
user_data = {}

db = SQLighter('db.sqlite3')

my_profile_texts = ["My Profile", "Мой профиль", "پروفایل من", "Mein Profil", "Мій профіль"]

language_names = {
    "en": "English",
    "de": "Deutsch",
    "ru": "Русский",
    "fa": "فارسی",
    "uk": "Українська",
}

letter_types = ["request", "complaint", "proposal", "thanks", "cover_letter"]

@dp.message_handler(commands=["start"])
async def cmd_start(message: types.Message):

    markup = types.InlineKeyboardMarkup(row_width=2)
    language_flags = {
        "en": "🇬🇧",
        "de": "🇩🇪",
        "ru": "🇷🇺",
        "fa": "🇮🇷",
        "uk": "🇺🇦",
    }
    language_buttons = [
        types.InlineKeyboardButton(f"{language_flags[language]} {language_names[language]}", callback_data=language_cb.new(code=language))
        for language, _ in messages.messages.items()
    ]
    markup.add(*language_buttons)

    try:
        await message.reply(messages.messages["en"]["choose_language"], reply_markup=markup)
    except:
        await bot.send_message(chat_id=message.chat.id, text=messages.messages["en"]["choose_language"], reply_markup=markup)

@dp.callback_query_handler(language_cb.filter())
async def choose_language(call: types.CallbackQuery, callback_data: dict):
    language = callback_data["code"]
    user_data[call.from_user.id] = {"language": language}
    markup = types.InlineKeyboardMarkup()

    for letter_type in letter_types:
        markup.add(types.InlineKeyboardButton(messages.messages[language][letter_type], callback_data=letter_type_cb.new(code=letter_type)))

    try:
        await call.message.edit_text(messages.messages[language]["choose_type"], reply_markup=markup)
    except MessageToEditNotFound:
        await bot.send_message(chat_id=call.from_user.id, text=messages.messages[language]["choose_type"], reply_markup=markup)
    await call.answer()

@dp.callback_query_handler(letter_type_cb.filter())
async def choose_letter_type(call: types.CallbackQuery, callback_data: dict):

    user_data[call.from_user.id]["letter_type"] = callback_data["code"]
    language = user_data[call.from_user.id]["language"]

    main_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = KeyboardButton(messages.messages[language]["my_profile"])
    main_keyboard.add(button1)

    if user_data[call.from_user.id]["letter_type"] == "cover_letter":
        await bot.send_message(call.message.chat.id, messages.messages[language]["enter_job_position"], reply_markup=main_keyboard)
    else:
        await bot.send_message(call.message.chat.id, messages.messages[language]["enter_subject"], reply_markup=main_keyboard)
    await call.answer()



@dp.message_handler(lambda message: message.text in my_profile_texts)
async def my_profile(message: types.Message):
    language = user_data[message.from_user.id]["language"]

    await bot.send_message(message.from_user.id, f"""ID - {message.from_user.id}

{messages.messages[language]["username"]} - @{message.from_user.username}
{messages.messages[language]["tokens"]} - {db.get_tokens(message.from_user.id)}
{messages.messages[language]["letters"]} - {db.get_letters(message.from_user.id)}""")

@dp.message_handler(lambda message: message.text and message.from_user.id in user_data and "subject" not in user_data[message.from_user.id] and user_data[message.from_user.id]["letter_type"] != "cover_letter")
async def enter_subject(message: types.Message):

    user_data[message.from_user.id]["subject"] = message.text
    language = user_data[message.from_user.id]["language"]

    await message.reply(messages.messages[language]["enter_sender"])

@dp.message_handler(lambda message: message.text and message.from_user.id in user_data and "job_position" not in user_data[message.from_user.id] and user_data[message.from_user.id]["letter_type"] == "cover_letter")
async def enter_job_position(message: types.Message):
    user_data[message.from_user.id]["job_position"] = message.text
    language = user_data[message.from_user.id]["language"]

    await message.reply(messages.messages[language]["enter_education"])

@dp.message_handler(lambda message: message.text and message.from_user.id in user_data and "education" not in user_data[message.from_user.id] and user_data[message.from_user.id]["letter_type"] == "cover_letter")
async def enter_education(message: types.Message):
    user_data[message.from_user.id]["education"] = message.text
    language = user_data[message.from_user.id]["language"]

    await message.reply(messages.messages[language]["enter_certificates"])

@dp.message_handler(lambda message: message.text and message.from_user.id in user_data and "certificates" not in user_data[message.from_user.id] and user_data[message.from_user.id]["letter_type"] == "cover_letter")
async def enter_certificates(message: types.Message):
    user_data[message.from_user.id]["certificates"] = message.text
    language = user_data[message.from_user.id]["language"]

    await message.reply(messages.messages[language]["enter_sender"])



@dp.message_handler(lambda message: message.text and message.from_user.id in user_data and "sender" not in user_data[message.from_user.id])
async def enter_sender(message: types.Message):
    user_data[message.from_user.id]["sender"] = message.text
    language = user_data[message.from_user.id]["language"]

    await message.reply(messages.messages[language]["enter_receiver"])

@dp.message_handler(lambda message: message.text and message.from_user.id in user_data and "receiver" not in user_data[message.from_user.id])
async def enter_receiver(message: types.Message):
    user_data[message.from_user.id]["receiver"] = message.text
    language = user_data[message.from_user.id]["language"]

    letter_type = user_data[message.from_user.id]["letter_type"]
    if letter_type == "cover_letter":
        job_position = user_data[message.from_user.id]["job_position"]
        prompt = f"Составьте письмо на немецком. Меня зовут {user_data[message.from_user.id]['sender']}. Работа: {job_position}, образование: {user_data[message.from_user.id].get('education', '')}, сертификаты: {user_data[message.from_user.id].get('certificates', '')}. Создайте профессиональное сопроводительное письмо для работодателя на позицию: {job_position}."
    else:
        prompt = f"Напиши письмо на немецком языке с типом {letter_type}, темой {user_data[message.from_user.id]['subject']}, отправителем {user_data[message.from_user.id]['sender']} и получателем {user_data[message.from_user.id]['receiver']}."

    generated_text = generate_letter(prompt)
    user_data[message.from_user.id]["generated_text"] = generated_text
    user_data[message.from_user.id]["content"] = generated_text
    await message.reply(messages.messages[language]["letter_in_german"])
    await message.reply(generated_text)

    tokens = int(len(re.findall(r'\w+', generated_text)) / 4)
    db.update_tokens(message.from_user.id, tokens)
    db.update_letters(message.from_user.id)

    if language != "de":
        prompt_translation = f"Переведи следующий текст на {language_names[language]}: {generated_text}"
        translated_text = generate_letter(prompt_translation)
        await message.reply(messages.messages[language]["letter_in_target_language"])
        await message.reply(translated_text)

    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(messages.messages[language]["export_pdf"], callback_data="export_pdf"))
    markup.add(types.InlineKeyboardButton(messages.messages[language]["export_word"], callback_data="export_word"))
    markup.add(types.InlineKeyboardButton(messages.messages[language]["send_another"], callback_data="send_another"))

    await message.reply(messages.messages[language]["export_options"], reply_markup=markup)

@dp.callback_query_handler(lambda call: call.data == "export_word")
async def on_export_word_button(call: types.CallbackQuery):
    await call.answer()
    user_id = call.from_user.id
    letter_data = user_data.get(user_id, {})

    docx_buffer = export_to_word(letter_data)
    docx_buffer.seek(0)
    input_file = InputFile(docx_buffer, filename="letter_and_translation.docx")
    await bot.send_document(call.from_user.id, input_file, caption="Ваше письмо в формате Word")

@dp.callback_query_handler(lambda call: call.data == "export_pdf")
async def on_export_pdf_button(call: types.CallbackQuery):
    await call.answer(cache_time=0)
    user_id = call.from_user.id
    letter_data = user_data.get(user_id, {})

    pdf_buffer = export_to_pdf(letter_data)
    pdf_buffer.seek(0)
    input_file = InputFile(pdf_buffer, filename="letter_and_translation.pdf")
    await bot.send_document(call.from_user.id, input_file, caption="Ваше письмо в формате PDF")



@dp.callback_query_handler(lambda call: call.data == "send_another")
async def on_send_another_button(call: types.CallbackQuery):
    await call.answer()
    await send_another_letter(call.message)

async def send_another_letter(message: types.Message):
    if message.from_user.id not in user_data:
        await cmd_start(message)
    else:
        language = user_data[message.from_user.id]["language"]
        markup = types.InlineKeyboardMarkup()

        for letter_type in ["request", "complaint", "proposal", "thanks", "cover_letter"]:
            markup.add(types.InlineKeyboardButton(messages.messages[language][letter_type], callback_data=letter_type_cb.new(code=letter_type)))

        await message.reply(messages.messages[language]["choose_type"], reply_markup=markup)

if __name__ == "__main__":
    from aiogram import executor
    executor.start_polling(dp)
