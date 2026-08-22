import asyncio
import os
import requests
import edge_tts
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from moviepy.editor import VideoFileClip, AudioFileClip

# Environment Değişkenlerinden Anahtarları Al
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
PEXELS_API_KEY = os.environ.get("PEXELS_API_KEY")

async def make_video(text, chat_id):
    # 1. Yapay Zeka Türkçe Seslendirme Üret
    tts = edge_tts.Communicate(text, "tr-TR-AhmetNeural")
    audio_file = f"voice_{chat_id}.mp3"
    await tts.save(audio_file)
    
    # 2. Stok Uzay Videosu Çek (Pexels API)
    headers = {"Authorization": PEXELS_API_KEY}
    res = requests.get("https://api.pexels.com/videos/search?query=space&per_page=1", headers=headers).json()
    video_url = res['videos'][0]['video_files'][0]['link']
    
    video_file = f"raw_{chat_id}.mp4"
    with open(video_file, "wb") as f:
        f.write(requests.get(video_url).content)
        
    # 3. Ses ve Videoyu Birleştir (MoviePy)
    audio_clip = AudioFileClip(audio_file)
    video_clip = VideoFileClip(video_file).subclip(0, audio_clip.duration)
    final_clip = video_clip.set_audio(audio_clip)
    
    output_file = f"final_{chat_id}.mp4"
    final_clip.write_videofile(output_file, codec="libx264", audio_codec="aac")
    
    # Temizlik
    audio_clip.close()
    video_clip.close()
    os.remove(audio_file)
    os.remove(video_file)
    
    return output_file

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    chat_id = update.message.chat_id
    
    await update.message.reply_text("Videonu ve seslendirmeyi hazırlıyorum, lütfen bekle...")
    
    try:
        final_video = await make_video(user_text, chat_id)
        # Videoyu Telegram'a Gönder
        with open(final_video, 'rb') as video:
            await context.bot.send_video(chat_id=chat_id, video=video)
        os.remove(final_video)
    except Exception as e:
        await update.message.reply_text(f"Bir hata oluştu: {str(e)}")

if __name__ == "__main__":
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()
