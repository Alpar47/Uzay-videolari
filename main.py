import os
import random
import requests
from gtts import gTTS
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
PEXELS_API_KEY = os.environ.get("PEXELS_API_KEY")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Merhaba baba! Uzun ve farklı uzay videoları, senaryo ve sesli anlatım üretmeye hazırım. Bana bir konu yaz yeterli (Örn: Kara Delikler)."
    )

async def search_videos(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.message.text
    await update.message.reply_text(f"'{query}' için uzun ve farklı bir uzay videosu, senaryo ve ses hazırlanıyor baba...")
    
    headers = {"Authorization": PEXELS_API_KEY}
    url = f"https://api.pexels.com/videos/search?query={query}&per_page=15&min_duration=10"
    
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        videos = data.get("videos", [])
        if videos:
            random_video = random.choice(videos)
            video_files = random_video.get("video_files", [])
            
            if video_files:
                video_url = video_files[0]["link"]
                await update.message.reply_video(video_url)
                
                script_text = (
                    f"Hoş geldiniz uzay maceraperestleri! Bugün evrenin en gizemli köşelerinden biri olan {query} konusunu inceliyoruz. "
                    f"Bilim insanlarının yıllardır üzerinde çalıştığı bu olağanüstü fenomen, uzay-zaman dokusunu tamamen değiştiriyor. "
                    f"Bu tarz uzay içeriklerinin devamı için beğenmeyi ve abone olmayı unutmayın. Karanlıkta kalın, esen kalın!"
                )
                
                await update.message.reply_text(f"🎬 **YOUTUBE VİDEO SENARYOSU: {query.upper()}**\n\n{script_text}")
                
                tts = gTTS(text=script_text, lang='tr')
                audio_path = "seslendirme.mp3"
                tts.save(audio_path)
                
                with open(audio_path, 'rb') as audio:
                    await update.message.reply_audio(audio, title=f"{query} Senaryosu")
                
                if os.path.exists(audio_path):
                    os.remove(audio_path)
                return

    await update.message.reply_text("Uzun video bulunamadı baba, farklı bir kelime deneyebilirsin.")

def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), search_videos))
    app.run_polling()

if __name__ == "__main__":
    main()
