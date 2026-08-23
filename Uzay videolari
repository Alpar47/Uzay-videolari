import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
PEXELS_API_KEY = os.environ.get("PEXELS_API_KEY")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Merhaba baba! YouTube için uzay videosu ve senaryo üretmeye hazırım. Bana bir konu yaz yeterli (Örn: Kara Delikler)."
    )

async def search_videos(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.message.text
    await update.message.reply_text(f"'{query}' için uzay videosu ve YouTube senaryosu hazırlanıyor baba...")
    
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
                
                script_text = (
                    f"🎬 **YOUTUBE VİDEO SENARYOSU: {query.upper()}**\n\n"
                    f"**Giriş:** Hoş geldiniz uzay maceraperestleri! Bugün evrenin en gizemli köşelerinden biri olan {query} konusunu inceliyoruz...\n"
                    f"**Gelişme:** Bilim insanlarının yıllardır üzerinde çalıştığı bu olağanüstü fenomen, uzay-zaman dokusunu tamamen değiştiriyor...\n"
                    f"**Kapanış:** Bu tarz uzay içeriklerinin devamı için beğenmeyi ve abone olmayı unutmayın. Karanlıkta kalın, esen kalın!"
                )
                await update.message.reply_text(script_text)
                return

    await update.message.reply_text("Video bulunamadı baba, farklı bir kelime deneyebilirsin.")

def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), search_videos))
    app.run_polling()

if __name__ == "__main__":
    main()
