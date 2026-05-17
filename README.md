# 🚀 SHOPIFY BOT - PROFESYONEL ÜRÜN ANALİZ ROBOTU

## ✨ ÖZELLİKLER

### 1️⃣ **Google Arama Analizi**
- Google'da gerçekten ürün arıyor
- Arama sonuç sayısından talep ölçüyor
- Proxy desteği ile IP ban'dan korunuyor

### 2️⃣ **Google Trends API**
- Trend skor hesaplıyor (0-100)
- Popülarite göstergesi

### 3️⃣ **Amazon API (RapidAPI)**
- Gerçek satış verisi çıkarıyor
- Ürün fiyatı ve rating

### 4️⃣ **AliExpress API**
- Fiyat bilgisi
- Stok durumu

### 5️⃣ **Shopify API**
- Kendi mağazandan satış verisi
- Stok takibi

### 6️⃣ **Gelişmiş Skorlama**
```
Genel Skor = 
  Google Arama (30puan) +
  Amazon Satışları (35puan) +
  Shopify Satışları (20puan) +
  Google Trends (15puan)
```

---

## 🔧 **SETUP - API KEYS NASIL ALINIR**

### **1. Google Trends API (RapidAPI)**
```
1. https://rapidapi.com/ git
2. "google-trends" ara
3. Subscribe (free tier var)
4. API Key kopyala
5. .env dosyasına yapıştır:
   GOOGLE_TRENDS_API_KEY=your_key_here
```

### **2. Amazon API (RapidAPI)**
```
1. https://rapidapi.com/ → "amazon-api" ara
2. Subscribe
3. API Key al
4. .env'ye ekle:
   AMAZON_API_KEY=your_key_here
```

### **3. AliExpress API**
```
1. https://open.aliexpress.com/ git
2. Developer Register
3. API Key al
4. .env'ye ekle:
   ALIEXPRESS_API_KEY=your_key_here
```

### **4. Shopify API (Kendi Mağazan için)**
```
1. Shopify Admin → Ayarlar → Apps ve Kanallar
2. "App ve satış kanalı gömme" → App'ler ve Entegrasyonlar
3. "Yönetim API erişim tokenı" oluştur
4. .env'ye ekle:
   SHOPIFY_API_KEY=your_key
   SHOPIFY_API_PASSWORD=your_password
   SHOPIFY_STORE_URL=your-store.myshopify.com
```

### **5. Proxy (Opsiyonel - IP Ban'dan Korun)**
```
1. https://www.freeproxylists.net/ → Proxy listesi indir
2. .env'ye ekle:
   USE_PROXY=true
   PROXY_LIST=proxy1.com:8080,proxy2.com:8080
```

---

## 🚀 **DEPLOY - RENDER'A**

```bash
# 1. .env dosyası oluştur (API keys ile)
cp .env.example .env
# API keys yazınız

# 2. Push et
git add .
git commit -m "API keys eklendi"
git push origin main

# 3. Render otomatik deploy edecek
```

---

## 📊 **DASHBOARD GÖRÜNTÜLERİ**

- **🔥 Mükemmel Ürünler** (80-100 Skor) - Direkt satışa al!
- **📈 İyi Ürünler** (60-80 Skor) - Potansiyel var
- **📉 Orta Ürünler** (0-60 Skor) - Araştır

---

## 🎯 **RAPOR ÖRNEĞİ**

```
Ürün: "Smart Watch 2026"
📊 Genel Skor: 92/100 🔥 (MÜKEMMEL)
🔍 Google: 850,000 sonuç
📈 Amazon: 4,523 satış
💰 AliExpress: $25.99 | 2,345 stok
🏪 Shopify: 523 satış
📈 Google Trends: 87/100

↓ SONUÇ: SATIŞA AL! 💰
```

---

## 🔗 **API ENDPOINTS**

```
GET / → Dashboard paneli
GET /api/products → JSON formatında tüm ürünler
```

---

## ⚙️ **AYARLAR**

### .env Dosyası
```
# Google Trends
GOOGLE_TRENDS_API_KEY=your_key

# Amazon
AMAZON_API_KEY=your_key
AMAZON_API_HOST=amazon-api.rapidapi.com

# AliExpress
ALIEXPRESS_API_KEY=your_key

# Shopify
SHOPIFY_API_KEY=your_key
SHOPIFY_API_PASSWORD=your_password
SHOPIFY_STORE_URL=your-store.myshopify.com

# Proxy (Opsiyonel)
USE_PROXY=false
PROXY_LIST=proxy1:8080,proxy2:8080

# Port
PORT=10000
```

---

## 📞 **SORUN ÇÖZÜMÜ**

| Sorun | Çözüm |
|-------|-------|
| API hata | API Key doğru mu kontrol et |
| IP Ban | USE_PROXY=true yap |
| Slow performance | Arama sıklığını azalt (bot.py line 280) |
| Database error | Render restart et |

---

## 📈 **İLERİ ÖZELLIKLER (Gelecek)**
- [ ] Email notifications (trend ürün bulunca)
- [ ] Discord webhook integration
- [ ] Multi-language support
- [ ] Mobile app
- [ ] ML-based predictions

---

**Made with ❤️ by Muhammed**
