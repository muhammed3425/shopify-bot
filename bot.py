from flask import Flask, jsonify
import requests
import threading
import time

app = Flask(__name__)

# --- AYARLAR (Abdurrahman gelince buraları dolduracak) ---
SHOP_URL = "https://MAGAZA-ADIN.myshopify.com"
TOKEN = "SHPAT_ANAHTARIN"
YASAKLI_KELIMELER = ["çakma", "replika", "silah", "illegal", "kumar"]

status = {"bot": "uyanıyor", "eklenen_urun": 0}




# --- GÜVENLİK FİLTRESİ ---
def guvenli_mi(urun_adi):
    for kelime in YASAKLI_KELIMELER:
        if kelime in urun_adi.lower():
            return False
    return True




# --- BOTUN ANA DÖNGÜSÜ ---
def bot_loop():
    while True:
        # Burada Abdurrahman'ın dükkanından siparişleri kontrol edecek
        # ve 3'ten fazla satanı analiz edip yeni ürün bulacak.
        print("Luvrenzo AI dükkanı gözlüyor...")
        time.sleep(60)




@app.route("/")
def home():
    return f"<h1>🤖 LUVRENZO AI PANEL</h1><p>Durum: {status['bot']}</p>"

if __name__ == "__main__":
    # Render için port ayarı
    threading.Thread(target=bot_loop).start()
    app.run(host="0.0.0.0", port=10000)
   
    
    
    
    def pazar_taramasi():
    print("🚀 Luvrenzo AI Keşfe Çıkıyor...")
    # Burada bot, popüler dropshipping sitelerini ve Google Trends başlıklarını 
    # (ücretsiz ve yasal yollarla) tarayacak bir simülasyon başlatıyor.
    bulunan_urunler = [
        {"ad": "Mini Taşınabilir Yazıcı", "trend": "Yüksek", "kar_marji": "%40"},
        {"ad": "Akıllı Temizleme Fırçası", "trend": "Orta-Yüksek", "kar_marji": "%35"}
    ]
    
    for urun in bulunan_urunler:
        if guvenli_mi(urun["ad"]):
            print(f"✅ ANALİZ EDİLDİ: {urun['ad']} - SEO Hazırlanıyor...")
            # Burada bot kendi kendine SEO açıklaması ve Meta tag oluşturuyor
    return bulunan_urunler




def pazar_taramasi():
    print("🚀 Luvrenzo AI Keşfe Çıkıyor...") # Bu satır tam 4 boşluk içerde olacak!
    bulunan_urunler = [
        {"ad": "Mini Taşınabilir Yazıcı", "trend": "Yüksek"},
        {"ad": "Akıllı Temizleme Fırçası", "trend": "Orta-Yüksek"}
    ]
    return bulunan_urunler

