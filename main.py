import os
import tweepy
import yfinance as yf
import feedparser
from datetime import datetime

# --- ŞİFRE ALMA KISMI (GitHub'dan okuyacak) ---
API_KEY = os.environ.get("API_KEY")
API_SECRET = os.environ.get("API_SECRET")
ACCESS_TOKEN = os.environ.get("ACCESS_TOKEN")
ACCESS_SECRET = os.environ.get("ACCESS_SECRET")

# --- AYARLAR ---
semboller = {
    'DOLAR': 'TRY=X',
    'EURO': 'EURTRY=X',
    'ALTIN': 'GC=F',
    'BITCOIN': 'BTC-USD'
}
haber_url = "https://tr.investing.com/rss/news.rss"

def tweet_hazirla():
    try:
        # 1. Tarih Başlığı
        zaman = datetime.now().strftime('%d.%m %H:%M')
        metin = f"🗓️ {zaman} | Piyasa Durumu\n\n"

        # 2. Finans Verileri
        for isim, kod in semboller.items():
            try:
                veri = yf.Ticker(kod).history(period="1d")
                if len(veri) > 0:
                    son = veri['Close'].iloc[-1]
                    acilis = veri['Open'].iloc[-1]
                    yuzde = ((son - acilis) / acilis) * 100
                    emoji = "🟢" if yuzde > 0 else "🔴"
                    metin += f"{isim}: {son:.2f} {emoji} (%{yuzde:.2f})\n"
            except: continue

        # 3. Son Haber (Opsiyonel)
        try:
            haber = feedparser.parse(haber_url).entries[0]
            metin += f"\n📢 {haber.title[:80]}...\n🔗 {haber.link}"
        except: pass

        metin += "\n\n#Borsa #Dolar #Altın"
        return metin
    except Exception as e:
        print(f"Hata: {e}")
        return None

def gonder():
    if not API_KEY:
        print("HATA: API Anahtarları bulunamadı!")
        return

    client = tweepy.Client(
        consumer_key=API_KEY,
        consumer_secret=API_SECRET,
        access_token=ACCESS_TOKEN,
        access_token_secret=ACCESS_SECRET
    )
    
    icerik = tweet_hazirla()
    if icerik:
        client.create_tweet(text=icerik)
        print("✅ Tweet başarıyla atıldı!")
    else:
        print("❌ Tweet oluşturulamadı.")

if __name__ == "__main__":
    gonder()
