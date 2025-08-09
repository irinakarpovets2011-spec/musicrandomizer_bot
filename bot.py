from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, filters
import random

TOKEN = "8279651212:AAEuwK2AWNxxUOLz1qsGGNwmUeW2GAJeJmk"
songs = []

async def start(update, context):
    await update.message.reply_text(
        "Привіт! 🎵 Скидай мені пісні (аудіо), а коли закінчиш — напиши /shuffle"
    )

async def save_song(update, context):
    audio = update.message.audio
    if audio:
        songs.append(audio.file_id)
        await update.message.reply_text(f"Додав пісню: {audio.title or 'Без назви'}")

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
app.add_handler(MessageHandler(filters.AUDIO, save_song))

app.run_polling()
