from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import re as re
data = {10: "Привет мир"}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Привет {update.effective_user.first_name}.\nКоманды:\n /get "code" - получить сообщение по коду \n /add "code" - добавить сообщение по коду')

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

app = ApplicationBuilder().token("7699100126:AAElXwC_nMbwQaTzcXMo45AVRoQpIjCXkxM").build()

app.add_handler(CommandHandler("start",start))

app.add_handler(CommandHandler("get",get))

app.add_handler(CommandHandler("add",add))

app.run_polling()