import logging
import requests
import random
import sqlite3
import sys

from telegram import ReplyKeyboardMarkup
from telegram.ext import Application, MessageHandler, filters, CommandHandler

"""logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)
logger = logging.getLogger(__name__)"""

# Основные переменные
Flag = True
Ege_Flag = 0
nabor_gitler = ""
final_nabor_gitler = list("гитлерГИТЛЕР")

# Импорт базы данных тренажера
dbname = "data/trng.db"
con = sqlite3.connect(dbname)
cur = con.cursor()

# Импорт анектодов про штирлица
stirliz = ("".join(open("data/stirliz.txt", encoding="utf-8", mode="r").readlines())).split("***\n")

async def General(update, context): 
    global nabor_gitler
    global final_nabor_gitler
    global stirliz
    global Flag
    global Ege_Flag, current_task_var, num_ege

    if "хах" in update.message.text.lower():
        await update.message.reply_text("а чего смешного")
    elif "хуй" in update.message.text.lower():
        await update.message.reply_text("не материтесь")
    elif "пизд" in update.message.text.lower():
        await update.message.reply_text("не материтесь")
    elif "бля" in update.message.text.lower():
        await update.message.reply_text("не материтесь")


    # Сборка гитлера
    elif update.message.text in final_nabor_gitler:
        if (update.message.text == "Г" or update.message.text == "г") and nabor_gitler == "":
            nabor_gitler = "ГИ"
            await update.message.reply_text("и")
        elif (update.message.text == "Т" or update.message.text == "т") and nabor_gitler == "ГИ":
            nabor_gitler = "ГИТЛ"
            await update.message.reply_text("л")
        elif (update.message.text == "Е" or update.message.text == "е") and nabor_gitler == "ГИТЛ":
            nabor_gitler = ""
            await update.message.reply_text("р")
            await update.message.reply_text("ура")
        else:
            nabor_gitler = ""
            await update.message.reply_text("ой")


    # Анекдоты
    elif any(el in update.message.text.lower().split() for el in ["расскажи анетод", "анекдот", "штирлиц", "штирлица"]):
        await update.message.reply_text("анекдот про штрилица:")
        await update.message.reply_text(stirliz[random.randint(1, len(stirliz))].lower())


    # Егэ
    elif any(el in update.message.text.lower().split() for el in ["егэ", "русский", "подготовка"]):
        await update.message.reply_text("Выбери задание (1-26)")
        Ege_Flag = 1
        
    elif Ege_Flag == 1:
        num_ege = update.message.text
        if num_ege in "1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21".split():
            current_task_var = Ege_vib(update.message.text)
            await update.message.reply_text(current_task_var[1])
            Ege_Flag = 2
        else:
            await update.message.reply_text("Что-то не то, ой")

    elif Ege_Flag == 2:
        if update.message.text == str(current_task_var[2]):
          await update.message.reply_text("Правильно! Решаем дальше?")
        else:
           await update.message.reply_text(f"Неправильно! Ответ: {str(current_task_var[2])}. Решаем дальше?")
        Ege_Flag = 3

    elif Ege_Flag == 3:
        if update.message.text.lower() == "да":
            current_task_var = Ege_vib(num_ege)
            await update.message.reply_text(current_task_var[1])
            Ege_Flag = 2
        else:
            await update.message.reply_text("Хорошо.")
            Ege_Flag = 0

    # Валюты
    elif any(el in update.message.text.lower().split() for el in ["валюта", "валюты", "курс"]):
        valutes = Api_Valut()
        await update.message.reply_text(f"Доллар: {valutes[0]}, Евро: {valutes[1]}")

     # Коты
    elif any(el in update.message.text.lower().split() for el in ["кот", "кошка", "кошак", "котенок", "котёнок"]):
        filename = ["data/1pic.jpg", "data/2pic.jpg", "data/3pic.jpg", "data/4pic.jpg",  "data/4pic.jpg"][random.randint(0, 4)]
        await context.bot.send_photo(chat_id=update.effective_chat.id, photo=open(filename, 'rb'))
        await update.message.reply_text("кот")


    #Общее     
    else:
        await update.message.reply_text(f"Я получил сообщение {update.message.text}")

async def start(update, context):
    """Отправляет сообщение когда получена команда /start"""
    user = update.effective_user
    await update.message.reply_html(
        rf"Привет {user.mention_html()}! Я мяу-бот. Напишите мне что-нибудь, и я пришлю это назад!",
    )

async def help_command(update, context):
    """Отправляет сообщение когда получена команда /help"""
    await update.message.reply_text("Я пока не умею помогать... Я только ваше эхо.")

def Ege_vib(num):
    if True:
            Tasks = ["First_task", "Second_task", "Third_task", "Fourth_task",
            "Fifth_task", "Sixth_task", "Seventh_task", "Eighth_task",
            "Ninth_task", "Tenth_task", "Eleventh_task", "Twelfth_task",
            "Thirteenth_task", "Fourteenth_task", "Fifteenth_task", "Sixteenth_task",
            "Seventeenth_task", "Eighteenth_task", "Nineteenth_task", "Twentieth_task",
            "Twenty_first_task", "Twenty_second_task", "Twenty_third_task", "Twenty_fourth_task",
            "Twenty_fifth_task", "Twenty_sixth_task"]
            current_task = Tasks[int(num) - 1]
            current_task_var = cur.execute(f"""SELECT * FROM {current_task}""").fetchall()
            current_task_var = current_task_var[random.randint(0, len(current_task_var) - 1)]
            return current_task_var
    else:
        return 0


def Api_Valut():
    valutes = []
    api_valut_request = "https://open.er-api.com/v6/latest/USD"
    response = requests.get(api_valut_request)
    if response:
        json_response = response.json()
        valutes.append(json_response["rates"]["RUB"])
    api_valut_request = "https://open.er-api.com/v6/latest/EUR"
    response = requests.get(api_valut_request)
    if response:
        json_response = response.json()
        valutes.append(json_response["rates"]["RUB"])

    if len(valutes) == 2:
        return valutes
    else:
       valutes.append("ОШИБКА")
       valutes.append("ОШИБКА")
       return valutes 


reply_keyboard = [['/start', '/help'],
                  ['/start', '/start']]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)

def main():
    global Flag, Ege_Flag
    application = Application.builder().token("6599286651:AAGVniRQsFwKtKNNDMXdPoc_tcU23qHoIKw").build()
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, General))
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.run_polling()


if __name__ == '__main__':
    main()
