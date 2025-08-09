from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, filters
import random

TOKEN = "8279651212:AAEuwK2AWNxxUOLz1qsGGNwmUeW2GAJeJmk"
songs = []

async def start(update, context):
    await update.message.reply_text(
        "Привіт! 🎵 Скидай мені пісні (аудіо, голосові або файли), а коли закінчиш — напиши /shuffle"
    )

async def save_song(update, context):
    if update.message.audio:
        songs.append(update.message.audio.file_id)
        title = update.message.audio.title or "Без назви"
    elif update.message.voice:
        songs.append(update.message.voice.file_id)
        title = "Голосове повідомлення"
    elif update.message.document:
        if update.message.document.mime_type.startswith("audio"):
            songs.append(update.message.document.file_id)
            title = update.message.document.file_name or "Аудіофайл"
        else:
            await update.message.reply_text("Це не аудіо, будь ласка скидай тільки пісні.")
            return
    else:
        await update.message.reply_text("Не можу зберегти цей файл, скидай аудіо чи голосове.")
        return
    await update.message.reply_text(f"Додав пісню: {title}")

async def shuffle_songs(update, context):
    if not songs:
        await update.message.reply_text("Ти ще не скинув жодної пісні!")
        return
    random.shuffle(songs)
    await update.message.reply_text("Ось твій перемішаний список 🎶")
    for file_id in songs:
        await context.bot.send_audio(chat_id=update.effective_chat.id, audio=file_id)
    songs.clear()

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("shuffle", shuffle_songs))
app.add_handler(MessageHandler(filters.AUDIO | filters.VOICE | filters.Document.MIME("audio/*"), save_song))

app.run_polling()

