from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import re as re
import sqlalchemy as db
data = {"10" : "Привет мир"}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Привет {update.effective_user.first_name}.\nКоманды:\n /get "code" - получить сообщение по коду \n /add "code" - добавить сообщение по коду \n /getn получить новость по id  \n /addn добавить новость')

async def get(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    raw = re.findall(r'\".*?\"', update.message.text)
    if len(raw) != 1 :
        await update.message.reply_text("bruh")
        return
    code = raw[0].replace('"', ' ')
    await update.message.reply_text(data[code])

async def add(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    raw = re.findall(r'\".*?\"', update.message.text)
    if len(raw) != 2 :
        await update.message.reply_text("bruh")
        return
    code = re.findall(r'\".*?\"', update.message.text)[0].replace('"', ' ')
    message = re.findall(r'\".*?\"', update.message.text)[1].replace('"', ' ')
    data[code] = message
    await update.message.reply_text("ok")
async def get_one_news(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    raw = update.message.text.split(" ")
    if len(raw) != 2 : 
        await update.message.reply_text("Проблема!")
        return
    id = int(raw[1])
    engine = db.create_engine("mysql+pymysql://root@127.0.0.1/db?charset=utf8mb4")
    conn = engine.connect()
    query = db.text(f"SELECT * FROM news WHERE id = {id}")
    news = conn.execute( query).fetchall()
    await update.message.reply_text(str(news[0][0]) + "\n" + str(news[0][1]))  
async def add_one_news(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    raw = update.message.text.split(" ")
    if len(raw) != 3 : 
        await update.message.reply_text("Проблема!")
        return
    name = str(raw[1])
    description = str(raw[2])
    engine = db.create_engine("mysql+pymysql://root@127.0.0.1/db?charset=utf8mb4")
    conn = engine.connect()
    query = db.text(f"INSERT INTO news (`name`,`description`) VALUES ('{name}','{description}');")
    news = conn.execute(query)
    conn.commit()
    await update.message.reply_text("ok")  

app = ApplicationBuilder().token("7699100126:AAElXwC_nMbwQaTzcXMo45AVRoQpIjCXkxM").build()

app.add_handler(CommandHandler("start",start))

app.add_handler(CommandHandler("get",get))

app.add_handler(CommandHandler("add",add))

app.add_handler(CommandHandler("getn",get_one_news))

app.add_handler(CommandHandler("addn",add_one_news))

app.run_polling()