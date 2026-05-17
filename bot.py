import requests
from flask import Flask, jsonify
import threading
import time
import os
import sqlite3
from datetime import datetime
from bs4 import BeautifulSoup
import json

app = Flask(__name__)

# --- VERİTABANI AYARI ---
DB_NAME = "products.db"

def init_database():
    """Ürün veritabanını oluştur"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_name TEXT NOT NULL,
            search_term TEXT,
            url TEXT,
            found_date TIMESTAMP,
            trend_score INTEGER,
            demand_level TEXT,
            status TEXT
        )
    ''')
    conn.commit()
    conn.close()

def save_product(product_name, search_term, url, trend_score, demand_level):
    """Ürünü veritabanına kaydet"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO products (product_name, search_term, url, found_date, trend_score, demand_level, status)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (product_name, search_term, url, datetime.now(), trend_score, demand_level, "ANALYZING"))
    conn.commit()
    conn.close()

def get_all_products():
    """Tüm kaydedilen ürünleri getir"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM products ORDER BY found_date DESC')
    products = cursor.fetchall()
    conn.close()
    return products

# --- ARAMA TERİMLERİ ---
ARAMA_TERIMLERI = [
    "trending dropshipping products 2026",
    "best selling items aliexpress",
    "viral products may 2026",
    "top dropshipping niches 2026",
    "most profitable products shopify"
]

islem_defteri = [f"[{datetime.now().strftime('%H:%M:%S')}] BOT BAŞLATILDI - Ürün Taraması Aktif"]

def analyze_demand(product_name, search_results_count):
    """Ürünün talep seviyesini analiz et"""
    if search_results_count > 100000:
        return "ÇOOK YÜKSEK", 95
    elif search_results_count > 50000:
        return "YÜKSEK", 80
    elif search_results_count > 10000:
        return "ORTA-YÜKSEK", 65
    elif search_results_count > 1000:
        return "ORTA", 50
    else:
        return "DÜŞÜK", 30

def google_product_search():
    """Google'da ürün arayışı yap ve analiz et"""
    global islem_defteri
    simdi = datetime.now().strftime("%H:%M:%S")
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'tr-TR,tr;q=0.9',
    }

    for terim in ARAMA_TERIMLERI:
        try:
            # Google'da arama yap
            search_url = f"https://www.google.com/search?q={terim.replace(' ', '+')}"
            response = requests.get(search_url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Arama sonuç sayısını çek
                result_stats = soup.find('div', {'id': 'result-stats'})
                results_text = result_stats.get_text() if result_stats else "0"
                
                try:
                    results_count = int(''.join(filter(str.isdigit, results_text.split()[0])))
                except:
                    results_count = 0
                
                log = f"[{simdi}] 🔍 ARANDI: '{terim}' - {results_count:,} sonuç"
                islem_defteri.insert(0, log)
                
                # Sayfadaki başlıkları (h3) çek - potansiyel ürünler
                basliklar = soup.find_all('h3')
                
                for i, baslik in enumerate(basliklar[:5]):  # İlk 5 sonuç
                    urun_adi = baslik.get_text().strip()
                    
                    if urun_adi and len(urun_adi) > 3:
                        # Talep seviyesi analiz et
                        demand, score = analyze_demand(urun_adi, results_count)
                        
                        # Veritabanına kaydet
                        save_product(
                            product_name=urun_adi,
                            search_term=terim,
                            url=search_url,
                            trend_score=score,
                            demand_level=demand
                        )
                        
                        # Log ekle
                        islem_defteri.insert(0, f"   ✅ KAYITLANDI: {urun_adi[:40]}... | Talep: {demand} | Skor: {score}/100")
            
            time.sleep(8)  # Google rate limit için
            
        except Exception as e:
            islem_defteri.insert(0, f"[{simdi}] ⚠️ Hata: {str(e)[:50]}")
            continue

def bot_loop():
    """Ana bot döngüsü"""
    while True:
        google_product_search()
        time.sleep(300)  # 5 dakikada bir ara

# --- WEB ARAYÜZÜ ---
@app.route("/")
def home():
    """Ana dashboard"""
    products = get_all_products()
    
    # Talep seviyesine göre ürünleri sınıflandır
    high_demand = [p for p in products if p[7] == "ÇOOK YÜKSEK" or p[7] == "YÜKSEK"]
    medium_demand = [p for p in products if p[7] == "ORTA-YÜKSEK" or p[7] == "ORTA"]
    low_demand = [p for p in products if p[7] == "DÜŞÜK"]
    
    # HTML oluştur
    rapor_html = "".join([f"<div style='margin-bottom:8px; color:#00ffcc; padding:8px; border-left: 3px solid #00ffcc;'>{islem}</div>" for islem in islem_defteri[:20]])
    
    urun_html = ""
    if high_demand:
        urun_html += "<h3 style='color:#ff6b6b; margin-top:20px;'>🔥 ÇOOK YÜKSEK TALEP (İdeal Ürünler)</h3>"
        for p in high_demand[:10]:
            urun_html += f"<div style='background:#1a1a1a; padding:12px; margin:8px 0; border-left:4px solid #ff6b6b; border-radius:4px;'><strong>{p[1]}</strong><br/>Talep: <span style='color:#ff6b6b;'>{p[7]}</span> | Skor: {p[6]}/100</div>"
    
    if medium_demand:
        urun_html += "<h3 style='color:#ffd93d; margin-top:20px;'>📈 ORTA-YÜKSEK TALEP</h3>"
        for p in medium_demand[:10]:
            urun_html += f"<div style='background:#1a1a1a; padding:12px; margin:8px 0; border-left:4px solid #ffd93d; border-radius:4px;'><strong>{p[1]}</strong><br/>Talep: <span style='color:#ffd93d;'>{p[7]}</span> | Skor: {p[6]}/100</div>"
    
    if low_demand:
        urun_html += "<h3 style='color:#888; margin-top:20px;'>📉 DÜŞÜK TALEP</h3>"
        for p in low_demand[:5]:
            urun_html += f"<div style='background:#1a1a1a; padding:12px; margin:8px 0; border-left:4px solid #888; border-radius:4px;'><strong>{p[1]}</strong><br/>Talep: <span style='color:#888;'>{p[7]}</span> | Skor: {p[6]}/100</div>"
    
    html_content = f"""
    <!DOCTYPE html>
    <html lang="tr">
    <head>
        <meta charset="UTF-8">
        <meta http-equiv="refresh" content="30">
        <title>Shopify Bot - Ürün Bulucusu</title>
        <style>
            body {{ margin:0; background:#050505; color:#fff; font-family:'Segoe UI', sans-serif; }}
            .container {{ max-width:1200px; margin:0 auto; padding:20px; }}
            .header {{ background:linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding:20px; border-radius:10px; margin-bottom:20px; }}
            .header h1 {{ margin:0; color:#fff; }}
            .header p {{ margin:5px 0 0 0; color:#e0e0e0; }}
            .stats {{ display:grid; grid-template-columns:repeat(auto-fit, minmax(200px, 1fr)); gap:15px; margin-bottom:20px; }}
            .stat-box {{ background:#1a1a1a; border:2px solid #667eea; padding:15px; border-radius:8px; text-align:center; }}
            .stat-box h3 {{ margin:0; color:#667eea; }}
            .stat-box p {{ margin:8px 0 0 0; font-size:24px; font-weight:bold; color:#fff; }}
            .panel {{ background:#0d0d0d; border:2px solid #333; border-radius:10px; padding:20px; margin-bottom:20px; }}
            .panel h2 {{ margin-top:0; color:#667eea; border-bottom:2px solid #667eea; padding-bottom:10px; }}
            .rapor {{ background:#000; border:1px solid #333; padding:15px; border-radius:8px; max-height:300px; overflow-y:auto; font-family:monospace; font-size:0.9em; }}
            h3 {{ margin-top:0; margin-bottom:10px; }}
            .rapor div {{ line-height:1.6; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🛍️ SHOPIFY BOT - TREND ÜRÜN BULUCUSU</h1>
                <p>Otomatik olarak Google'dan trend olan ürünleri bulup analiz ediyor...</p>
            </div>
            
            <div class="stats">
                <div class="stat-box">
                    <h3>Toplam Ürün</h3>
                    <p>{len(products)}</p>
                </div>
                <div class="stat-box">
                    <h3>Yüksek Talep</h3>
                    <p style="color:#ff6b6b;">{len(high_demand)}</p>
                </div>
                <div class="stat-box">
                    <h3>Orta Talep</h3>
                    <p style="color:#ffd93d;">{len(medium_demand)}</p>
                </div>
                <div class="stat-box">
                    <h3>Son Güncelleme</h3>
                    <p>{datetime.now().strftime('%H:%M:%S')}</p>
                </div>
            </div>
            
            <div class="panel">
                <h2>📊 CANLI İŞLEM KAYITI</h2>
                <div class="rapor">{rapor_html}</div>
            </div>
            
            <div class="panel">
                <h2>🎯 BULDUĞU ÜRÜNLER (Talep Seviyesine Göre)</h2>
                {urun_html if urun_html else "<p style='color:#999;'>Henüz ürün bulunamadı...</p>"}
            </div>
        </div>
    </body>
    </html>
    """
    return html_content

@app.route("/api/products")
def api_products():
    """API olarak tüm ürünleri JSON ile döndür"""
    products = get_all_products()
    product_list = []
    for p in products:
        product_list.append({
            "id": p[0],
            "name": p[1],
            "search_term": p[2],
            "demand": p[7],
            "score": p[6],
            "found_date": p[5]
        })
    return jsonify(product_list)

if __name__ == "__main__":
    init_database()
    threading.Thread(target=bot_loop, daemon=True).start()
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
