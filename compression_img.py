import os
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from telebot.util import content_type_media
from PIL import Image
from helper import get_random_string


APITOKENIMGCOMP = os.environ.get('APITOKENIMGCOMP')

bot = telebot.TeleBot(APITOKENIMGCOMP)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    
    msg = bot.send_message(
        message.chat.id, "لتصغير حجم صورتك ، ارسلها الان \n To compress your picture, send it now")


@bot.message_handler(func=lambda message: True)
def message_handler(message):

    try:
        bot.send_message(
        message.chat.id, "لتصغير حجم صورتك ، ارسلها الان \n To compress your picture, send it now")
    except:
        bot.send_message(
            message.chat.id, 'Something went wrong try agin later')

@bot.message_handler(content_types=content_type_media)
def image_handler(message):
    try:

        fileID = message.photo[-1].file_id
        file_info = bot.get_file(fileID)
        downloaded_file = bot.download_file(file_info.file_path)
        imageName = get_random_string(16)
        with open(imageName+".jpg", 'wb') as new_file:
            new_file.write(downloaded_file)
        bot.reply_to(message, '10 second left ')
        image = Image.open(imageName+".jpg")
        image.save(imageName+'.jpg',optimize=True,quality=10)

        bot.reply_to(message, '5 second left ')
        chat_id = message.chat.id
        doc = open(imageName+".jpg", 'rb')
        bot.send_document(chat_id, doc)
        doc.close()
        os.remove(imageName+".jpg")
    except:
        bot.send_message(message.chat.id,'Something went wrong try again later')

bot.polling()
