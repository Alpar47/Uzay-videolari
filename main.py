import os
import requests
from gtts import gTTS
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
PEXELS_API_KEY = os.environ.get("PEXELS_API_KEY")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Merhaba baba! Bot aktif. Konu yaz yeterli.")

async def search_videos(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.message.text
    await update.message.reply_text(f"'{query}' için içerik hazırlanıyor baba...")
    
    headers = {"Authorization": PEXELS_API_KEY}
    url = f"https://api.pexels.com/videos/search?query={query}&per_page=1"
    
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        videos = data.get("videos", [])
        if videos:
            video_files = videos[0].get("video_files", [])
            if video_files:
                video_url = video_files[0]["link"]
                await update.message.reply_video(video_url)
                
                script_text = f"Hoş geldiniz uzay maceraperestleri! Bugün {query} konusunu inceliyoruz. Beğenmeyi ve abone olmayı unutmayın."
                await update.message.reply_text(f"🎬 **SENARYO:**\n\n{script_text}")
                
                tts = gTTS(text=script_text, lang='tr')
                audio_path = "ses.mp3"
                tts.save(audio_path)
                
                with open(audio_path, 'rb') as audio:
                    await update.message.reply_audio(audio)
                
                if os.path.exists(audio_path):
                    os.remove(audio_path)
                return

    await update.message.reply_text("Bulunamadı baba.")

def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), search_videos))
    app.run_polling()

if __name__ == "__main__":
    main()
