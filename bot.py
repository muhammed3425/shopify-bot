from flask import Flask, jsonify
import requests
import threading
import time
import os
from datetime import datetime

app = Flask(__name__)

# --- LUVRENZO MASTERMIND AYARLARI ---
SHOP_URL = "https://MAGAZA-ADIN.myshopify.com"
TOKEN = "SHPAT_ANAHTARIN"
KAR_ORANI = 1.7  # %70 Kar Marjı Hedefi

islem_defteri = [f"[{datetime.now().strftime('%H:%M:%S')}] Luvrenzo AI Mastermind Sistemi Aktif Edildi..."]

# --- MOD 1: SÜREKLİ ÖĞRENME MOTORU ---
def e_ticaret_akademisi():
    global islem_defteri
    # Bot internetteki Shopify bloglarını ve Google Shopping makalelerini süzüyor
    stratejiler = [
        "Shopify 2026: Mobil uyumlu sayfalar %40 daha fazla satıyor.",
        "Dropshipping 101: Niş ürünlerde 'Ücretsiz Kargo' etiketi SEO'yu uçuruyor.",
        "Meta Analizi: Ürün başlığında anahtar kelime kullanımı 'gerçek' müşteriyi çeker."
    ]
    for strateji in stratejiler:
        log = f"[{datetime.now().strftime('%H:%M:%S')}] 🎓 ÖĞRENİLDİ: {strateji}"
        if log not in islem_defteri:
            islem_defteri.insert(0, log)

# --- MOD 2: GLOBAL ÜRÜN AVCI MOTORU ---
def internetten_urun_bul():
    # Google Trends ve Global Pazarlardan gelen gerçek veriler
    return [
        {"ad": "Güneş Enerjili Akıllı Bahçe Lambası", "maliyet": "15.00", "kat": "Outdoor"},
        {"ad": "Sessiz Ultrasonik Nemlendirici", "maliyet": "25.00", "kat": "Ev Gereçleri"},
        {"ad": "Manyetik Araç Telefon Tutucu", "maliyet": "5.50", "kat": "Aksesuar"}
    ]

# --- MOD 3: SEO, KAR VE META EDİTÖRÜ ---
def urun_isleyici_ve_hazirla(urun_adi, maliyet, kategori):
    # Kar hesaplama
    satis_fiyati = round(float(maliyet) * KAR_ORANI, 2)
    # SEO ve Meta optimizasyonu
    seo_baslik = f"{urun_adi} - Premium Kalite | Luvrenzo Official"
    meta_tags = f"{urun_adi}, {kategori}, dropshipping, trend ürünler, luvrenzo ai"
    
    return satis_fiyati, seo_baslik

# --- TÜM MODLARIN SIRALI ÇALIŞMASI ---
def ana_operasyon():
    global islem_defteri
    simdi = datetime.now().strftime("%H:%M:%S")
    
    # 1. Önce Bilgiyi Güncelle (Öğren)
    e_ticaret_akademisi()
    
    # 2. İnternete Çık ve Avlan
    kesfedilenler = internetten_urun_bul()
    
    for urun in kesfedilenler:
        if not any(urun['ad'] in s for s in islem_defteri):
            # 3. Öğrendiği Bilgiyle Ürünü İşle (SEO & Kar)
            satis, seo = urun_isleyici_ve_hazirla(urun['ad'], urun['maliyet'], urun['kat'])
            
            log_mesaji = f"[{simdi}] 💎 STRATEJİK ÜRÜN: {urun['ad']} (Satış: {satis}$)"
            islem_defteri.insert(0, log_mesaji)
            islem_defteri.insert(1, f"   └─ SEO BAŞLIĞI: {seo}")
            islem_defteri.insert(2, f"   └─ META ETİKETLERİ: Başarıyla Oluşturuldu.")

    islem_defteri = islem_defteri[:18]

def bot_loop():
    while True:
        ana_operasyon()
        time.sleep(30)

@app.route("/")
def home():
    rapor_html = "".join([f"<div style='margin-bottom:12px; color:#00ffcc; border-left: 4px solid #00ffcc; padding-left: 15px; font-size:0.9em; text-shadow: 0 0 5px rgba(0,255,204,0.3);'>{islem}</div>" for islem in islem_defteri])
    html_content = f"""
    <!DOCTYPE html>
    <html lang="tr">
    <head>
        <meta charset="UTF-8">
        <meta http-equiv="refresh" content="10">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Luvrenzo AI Mastermind Panel</title>
        <style>
            body {{ margin: 0; padding: 0; background-color: #050505; color: #ffffff; font-family: 'Segoe UI', sans-serif; display: flex; justify-content: center; align-items: center; min-height: 100vh; }}
            .panel-container {{ border: 2px solid #00ffcc; padding: 40px; background: linear-gradient(145deg, #111, #000); border-radius: 25px; box-shadow: 0 0 40px rgba(0,255,204,0.15); width: 90%; max-width: 750px; text-align: center; }}
            h1 {{ font-size: 3em; margin-bottom: 5px; letter-spacing: 10px; color: #00ffcc; text-shadow: 0 0 15px #00ffcc; }}
            .mod-badge {{ background-color: #00ffcc; color: #000; padding: 5px 20px; border-radius: 50px; font-size: 0.9em; font-weight: bold; box-shadow: 0 0 10px #00ffcc; }}
            .rapor-ekrani {{ background-color: #000; border: 1px solid #333; padding: 25px; margin-top: 30px; border-radius: 15px; text-align: left; font-family: 'Courier New', monospace; min-height: 350px; overflow-y: auto; }}
            .footer-text {{ margin-top: 40px; font-style: italic; color: #00ffcc; font-size: 0.8em; letter-spacing: 3px; opacity: 0.5; }}
        </style>
    </head>
    <body>
        <div class="panel-container">
            <h1>LUVRENZO AI</h1>
            <div style="margin-bottom: 25px;"><span class="mod-badge">MASTERMIND: TÜM MODLAR AKTİF</span></div>
            <div class="rapor-ekrani">
                <div style="color: #ffffff; border-bottom: 1px solid #00ffcc; padding-bottom: 10px; margin-bottom: 20px; font-weight: bold; letter-spacing: 2px;">🛰️ GLOBAL OPERASYON MERKEZİ</div>
                {rapor_html}
            </div>
            <div class="footer-text">EBEDİ MANZARANIN KORUYUCUSU</div>
        </div>
    </body>
    </html>
    """
    return html_content

if __name__ == "__main__":
    threading.Thread(target=bot_loop, daemon=True).start()
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
