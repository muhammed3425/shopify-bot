from flask import Flask, jsonify
import requests
import threading
import time
import os

app = Flask(__name__)

# --- AYARLAR (Abdurrahman gelince buraları dolduracak) ---
SHOP_URL = "https://MAGAZA-ADIN.myshopify.com"
TOKEN = "SHPAT_ANAHTARIN"
YASAKLI_KELIMELER = ["çakma", "replika", "silah", "illegal", "kumar"]

status = {"bot": "çalışıyor", "eklenen_urun": 0}

# --- GÜVENLİK FİLTRESİ ---
def guvenli_mi(urun_adi):
    for kelime in YASAKLI_KELIMELER:
        if kelime in urun_adi.lower():
            return False
    return True

# --- PAZAR TARAMASI FONKSİYONU ---
def pazar_taramasi():
    print("🚀 Luvrenzo AI Keşfe Çıkıyor...")
    bulunan_urunler = [
        {"ad": "Mini Taşınabilir Yazıcı", "trend": "Yüksek", "kar_marji": "%40"},
        {"ad": "Akıllı Temizleme Fırçası", "trend": "Orta-Yüksek", "kar_marji": "%35"}
    ]
    
    for urun in bulunan_urunler:
        if guvenli_mi(urun["ad"]):
            print(f"✅ ANALİZ EDİLDİ: {urun['ad']} - SEO Hazırlanıyor...")
    return bulunan_urunler

# --- BOTUN ANA DÖNGÜSÜ ---
def bot_loop():
    while True:
        print("Luvrenzo AI dükkanı gözlüyor...")
        # Başlangıçta bir tarama yapması için ekledik
        pazar_taramasi()
        time.sleep(60)

@app.route("/")
def home():
    return f"""
    <h1>🤖 LUVRENZO AI PANEL</h1>
    <p>Durum: {status['bot']}</p>
    <p>Sistem: Hazır ve Abdurrahman'ı bekliyor.</p>
    <hr>
    <p><i>Luvrenzo İmparatorluğu Gururla Sunar...</i></p>
    """

if __name__ == "__main__":
    # Botu arka planda başlat
    threading.Thread(target=bot_loop, daemon=True).start()
    # Render için port ayarı (Portu Render otomatik de verebilir ama biz 10000 yapıyoruz)
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
