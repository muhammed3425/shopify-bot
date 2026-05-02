from flask import Flask, jsonify
import requests
import threading
import time
import os
from datetime import datetime

app = Flask(__name__)

# --- DROPSHIPPING & SEO AYARLARI ---
SHOP_URL = "https://MAGAZA-ADIN.myshopify.com"
TOKEN = "SHPAT_ANAHTARIN"
KAR_ORANI = 1.5  # %50 kar marjı ekler (Örn: 10$'lık ürünü 15$ yapar)

islem_defteri = [f"[{datetime.now().strftime('%H:%M:%S')}] Luvrenzo AI SEO & Kar Motoru Aktif..."]

# --- SHOPIFY OTOMASYON MOTORU ---
def urun_isleyici_ve_yukle(urun_adi, maliyet, kategori):
    # 1. KAR MARJI HESAPLAMA
    satis_fiyati = round(float(maliyet) * KAR_ORANI, 2)
    
    # 2. SEO & META ETİKETİ OLUŞTURMA
    seo_baslik = f"En İyi {urun_adi} - Ücretsiz Kargo | Luvrenzo Store"
    meta_aciklama = f"Yeni nesil {urun_adi} şimdi stoklarda. {kategori} kategorisindeki en kaliteli ürün, en uygun fiyata."
    
    # 3. SHOPIFY'A GÖNDERİLECEK VERİ PAKETİ
    payload = {
        "product": {
            "title": seo_baslik,
            "body_html": f"<strong>{urun_adi}</strong> ile hayatınızı kolaylaştırın. <br>Hemen keşfedin!",
            "vendor": "Luvrenzo AI",
            "product_type": kategori,
            "variants": [{"price": str(satis_fiyati), "sku": "LVR-001"}],
            "metafields_global_title_tag": seo_baslik,
            "metafields_global_description_tag": meta_aciklama
        }
    }
    
    # Token gelince bu kısım gerçek yüklemeyi yapar
    if TOKEN != "SHPAT_ANAHTARIN":
        # requests.post(f"{SHOP_URL}/admin/api/2023-01/products.json", json=payload, headers=...)
        pass
    
    return satis_fiyati

# --- PAZAR TARAMASI VE AKILLI ANALİZ ---
def pazar_taramasi():
    global islem_defteri
    simdi = datetime.now().strftime("%H:%M:%S")
    
    kesfedilenler = [
        {"ad": "Mini Nemlendirici", "maliyet": "12.00", "kat": "Ev Gereçleri"},
        {"ad": "Duruş Düzeltici", "maliyet": "8.50", "kat": "Sağlık"},
        {"ad": "Şarjlı El Atarisi", "maliyet": "15.00", "kat": "Elektronik"}
    ]
    
    for urun in kesfedilenler:
        if not any(urun['ad'] in s for s in islem_defteri):
            satis = urun_isleyici_ve_yukle(urun['ad'], urun['maliyet'], urun['kat'])
            log_mesaji = f"[{simdi}] ✅ SEO & KAR TAMAM: {urun['ad']} (Maliyet: {urun['maliyet']}$ -> Satış: {satis}$)"
            islem_defteri.insert(0, log_mesaji)
            islem_defteri.insert(1, f"   └─ Meta Etiketleri ve SEO Açıklaması Hazırlandı.")
    
    islem_defteri = islem_defteri[:15]

def bot_loop():
    while True:
        pazar_taramasi()
        time.sleep(30)

@app.route("/")
def home():
    rapor_html = "".join([f"<div style='margin-bottom:12px; color:#28a745; border-left: 4px solid #28a745; padding-left: 15px;'>{islem}</div>" for islem in islem_defteri])
    html_content = f"""
    <!DOCTYPE html>
    <html lang="tr">
    <head>
        <meta charset="UTF-8">
        <meta http-equiv="refresh" content="15">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Luvrenzo AI Smart Dropship</title>
        <style>
            body {{ margin: 0; padding: 0; background-color: #1a1a1a; color: #ffffff; font-family: 'Segoe UI', sans-serif; display: flex; justify-content: center; align-items: center; min-height: 100vh; text-align: center; }}
            .panel-container {{ border: 1px solid #444; padding: 40px; background-color: #262626; border-radius: 20px; box-shadow: 0 15px 35px rgba(0,0,0,0.7); width: 85%; max-width: 650px; }}
            h1 {{ font-size: 2.8em; margin-bottom: 5px; letter-spacing: 6px; text-transform: uppercase; background: linear-gradient(to bottom, #ffffff, #888888); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }}
            .status-badge {{ background-color: #6f42c1; color: white; padding: 5px 15px; border-radius: 50px; font-size: 0.85em; font-weight: bold; }}
            .rapor-ekrani {{ background-color: #111; border: 1px solid #333; padding: 25px; margin-top: 30px; border-radius: 12px; text-align: left; font-family: 'Courier New', monospace; font-size: 0.85em; min-height: 250px; }}
            .footer-text {{ margin-top: 40px; font-style: italic; color: #555; font-size: 0.8em; letter-spacing: 2px; }}
        </style>
    </head>
    <body>
        <div class="panel-container">
            <h1>LUVRENZO AI</h1>
            <div style="margin-bottom: 20px;">MOD: <span class="status-badge">AKILLI ÜRÜN EDİTÖRÜ & SEO MODU</span></div>
            <div class="rapor-ekrani">
                <div style="color: #6f42c1; border-bottom: 1px solid #333; padding-bottom: 10px; margin-bottom: 15px; font-weight: bold;">🛰️ CANLI SEO VE KAR ANALİZİ</div>
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
