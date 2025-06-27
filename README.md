# 🚗 MCP Araç Arama Sistemi - AI Tabanlı Araç Galeri Asistanı

![MCP Logo](mcp.jpeg)

Bu proje, **Model Context Protocol (MCP)** kullanarak AI asistanlarına gerçek zamanlı araç veritabanı erişimi sağlayan kapsamlı bir örnek uygulamadır. Claude, ChatGPT gibi büyük dil modellerinin veritabanlarıyla nasıl etkileşim kurabileceğini gösterir.

## 🎯 Proje Özeti

MCP (Model Context Protocol), AI modellerinin dış veri kaynaklarına standartlaştırılmış şekilde erişmesini sağlayan devrimsel bir protokoldür. Bu proje, araç galeri senaryosu üzerinden MCP'nin gücünü pratik olarak göstermektedir.

### 🔥 Temel Özellikler

- **🤖 AI Asistanı**: Claude ile doğal dil kullanarak araç arama
- **🗄️ MCP Server**: MySQL veritabanına güvenli erişim
- **📊 Gelişmiş Filtreleme**: 15+ farklı arama kriteri
- **🌐 Web Entegrasyonu**: Tavily API ile güncel araç bilgileri
- **📱 Çoklu Arayüz**: Terminal, Streamlit ve web tabanlı
- **🔒 Güvenlik**: Parametrized queries ile SQL injection koruması

## 🏗️ Proje Mimarisi

![MCP Akış Diyagramı](diyagram.png)

### 📦 Dosya Yapısı

```
mcp-anlatim/
├── 📱 Uygulamalar
│   ├── app.py              # Ana terminal uygulaması (Claude + MCP)
│   ├── appst.py            # Streamlit web uygulaması-mcpsiz (OpenAI + LangChain)
│   └── mcpanlatim.py       # Kapsamlı eğitim ve demo uygulaması
├── 🔧 MCP Server
│   └── dataturkmcp.py      # FastMCP tabanlı araç arama server'ı
├── 🗄️ Veri
│   └── veri.xlsx           # Excel format araç verileri
├── 📋 Yapılandırma
│   ├── requirements.txt    # Python bağımlılıkları
│   └── .env               # Ortam değişkenleri (API anahtarları)
├── 📚 Dokümantasyon
│   ├── README.md          # Bu dosya
│   ├── kaynak.txt         # Kaynaklar ve bağlantılar
│   └── *.png, *.jpeg      # Görsel materyaller
└── 📄 LICENSE             # MIT lisansı
```

## 🚀 Hızlı Başlangıç

### 1️⃣ Kurulum

```bash
# Projeyi klonla
git clone https://github.com/halilkkaya/mcp-anlatim.git
cd mcp-anlatim

# Sanal ortam oluştur (önerilen)
python -m venv venv
source venv/bin/activate  # Linux/Mac
# veya
venv\Scripts\activate     # Windows

# Bağımlılıkları yükle
pip install -r requirements.txt
```

### 2️⃣ Ortam Değişkenlerini Ayarla

`.env` dosyası oluşturun:

```env
# AI API Anahtarları
ANTHROPIC_API_KEY=your_claude_api_key_here
OPENAI_API_KEY=your_openai_api_key_here

# Veritabanı Ayarları
MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=your_mysql_password
MYSQL_DATABASE=mcp_deneme

# Web Arama API'si
TAVILY_API_KEY=your_tavily_api_key

# MCP Server URL'i
MCP_URL=http://localhost:8000/mcp
```

### 3️⃣ Veritabanını Hazırla

```bash
# MySQL'de veritabanı oluştur
mysql -u root -p
CREATE DATABASE mcp_deneme;
USE mcp_deneme;

# Araç verilerini import et (varsa)
# Veya SQLite dosyasını kullan: arabalar.db
```

### 4️⃣ Uygulamaları Çalıştır

#### 🎓 Eğitim ve Demo (Önerilen)
```bash
streamlit run mcpanlatim.py
```
**Kapsamlı MCP anlatımı, tool tanıtımları ve canlı test ortamı**

#### 🖥️ Terminal Uygulaması
```bash
python app.py
```
**Claude ile terminal tabanlı araç asistanı**

#### 🌐 Web Uygulaması
```bash
streamlit run appst.py
```
**OpenAI tabanlı web araç danışmanı**

#### ⚙️ MCP Server
```bash
python dataturkmcp.py
```
**8000 portunda MCP server başlatır**

## 🛠️ MCP Tools (Araçlar)

### 🔍 `araba_ara` - Ana Arama Tool'u

Gelişmiş filtreleme seçenekleri ile araç arama:

```python
# Temel filtreleme
araba_ara(
    marka="toyota",           # Araç markası
    model="corolla",          # Model adı  
    min_fiyat=100000,         # Minimum fiyat
    max_fiyat=500000,         # Maksimum fiyat
    il="istanbul"             # Şehir
)

# Gelişmiş özellikler
araba_ara(
    ozel_arama="ekonomik",    # Önceden tanımlı kategoriler
    siralama="fiyat_artan",   # Sıralama tipi
    limit=10,                 # Sonuç sayısı
    detayli=True,             # Detaylı bilgiler
    istatistik=True           # İstatistiksel veriler
)
```

#### 📋 Tam Parametre Listesi

| Parametre | Tip | Açıklama | Örnek |
|-----------|-----|----------|-------|
| `marka` | str/list | Araç markası | "toyota" veya ["ford", "bmw"] |
| `model` | str | Model adı | "focus", "corolla" |
| `min_fiyat`/`max_fiyat` | int | Fiyat aralığı | 50000, 200000 |
| `min_yil`/`max_yil` | int | Model yılı | 2015, 2023 |
| `min_km`/`max_km` | int | Kilometre aralığı | 0, 100000 |
| `il` | str | Şehir | "istanbul", "ankara" |
| `yakit` | str | Yakıt türü | "benzin", "dizel", "hibrit" |
| `vites` | str | Vites türü | "manuel", "otomatik" |
| `durum` | str | Araç durumu | "yeni", "mükemmel", "iyi" |
| `tip` | str | Araç tipi | "sedan", "suv", "hatchback" |
| `renk` | str | Araç rengi | "beyaz", "siyah", "gri" |
| `ozel_arama` | str | Özel kategoriler | "ekonomik", "lüks", "aile", "spor" |
| `siralama` | str | Sıralama | "fiyat_artan", "yil_yeni", "km_az" |
| `limit` | int | Sonuç sayısı | 5 (varsayılan) |
| `detayli` | bool | Detaylı bilgi | True/False |
| `benzer_araclar` | bool | Benzer öneriler | True/False |
| `istatistik` | bool | İstatistiksel veri | True/False |

### 🔧 Diğer Tools

| Tool | Açıklama | Kullanım |
|------|----------|---------|
| `sql_sorgusu_calistir` | Özel SQL sorguları | Gelişmiş analiz |
| `tablolari_listele` | Veritabanı tabloları | Yapı keşfi |
| `tablo_yapisi_goster` | Tablo şeması | Sütun bilgileri |
| `web_arama` | Tavily API araması | Güncel bilgiler |

## 💡 Örnek Kullanım Senaryoları

### 🏠 Aile Aracı Arama
```python
araba_ara(
    ozel_arama="aile",
    min_fiyat=100000,
    max_fiyat=300000,
    yakit="dizel",
    siralama="fiyat_artan"
)
```

### ⚡ Ekonomik Araç Bulma
```python
araba_ara(
    ozel_arama="ekonomik",
    max_fiyat=150000,
    yakit=["hibrit", "dizel"],
    limit=10
)
```

### 🏎️ Lüks Spor Araç
```python
araba_ara(
    marka=["bmw", "mercedes", "audi"],
    tip="coupe",
    ozel_arama="lüks",
    min_yil=2020,
    detayli=True
)
```

### 📊 Pazar Analizi
```python
araba_ara(
    marka="toyota",
    istatistik=True,
    benzer_araclar=True,
    limit=20
)
```

## 🤖 AI Asistan Örnekleri

### 💬 Doğal Dil Sorguları

```
Kullanıcı: "Aileme uygun, ekonomik bir araç arıyorum"
AI: araba_ara(ozel_arama="aile", yakit="dizel", siralama="fiyat_artan")

Kullanıcı: "BMW veya Mercedes, 2020 sonrası, coupe"  
AI: araba_ara(marka=["bmw", "mercedes"], tip="coupe", min_yil=2020)

Kullanıcı: "İstanbul'da 200 bin TL altı Toyota araçlar"
AI: araba_ara(marka="toyota", il="istanbul", max_fiyat=200000)
```

## 🔒 Güvenlik Özellikleri

- **🛡️ SQL Injection Koruması**: Parametrized queries
- **🔐 API Anahtarı Güvenliği**: Ortam değişkenleri
- **🚫 Erişim Kontrolü**: Aktif kayıt filtreleme
- **⚠️ Hata Yönetimi**: Güvenli hata mesajları
- **🔍 Input Validation**: Parametre doğrulama

## 📈 Performans Optimizasyonları

- **📊 Veritabanı İndeksleri**: Hızlı sorgular
- **🔗 Connection Pooling**: Kaynak yönetimi
- **📝 Query Logging**: Performans takibi
- **⚡ Caching**: Yanıt hızlandırma

## 🎓 MCP Öğrenme Kaynakları

- 📺 **YouTube**: [MCP Server Anlatımı](https://youtu.be/u1PYSKqfHEw?si=h3td5CuEk24zhQlK)
- 📚 **HuggingFace**: [MCP Kursu](https://huggingface.co/learn/mcp-course)

## 🛠️ Teknik Detaylar

### 🔧 Kullanılan Teknolojiler

| Kategori | Teknoloji | Versiyon |
|----------|-----------|----------|
| **AI Models** | Anthropic Claude | 3.5 Haiku |
| | OpenAI GPT | 3.5 Turbo |
| **MCP Framework** | FastMCP | Latest |
| **Database** | MySQL | 8.0+ |
| **Web Framework** | Streamlit | Latest |
| **ML Framework** | LangChain | Latest |
| **Search API** | Tavily | v1 |

### ⚙️ Sistem Gereksinimleri

- **Python**: 3.8+
- **RAM**: 2GB+ (önerilen 4GB)
- **Disk**: 1GB boş alan
- **Network**: İnternet bağlantısı (API'lar için)

### 🔧 API Anahtarları

| Servis | Neden Gerekli | Ücretsiz Limitler |
|--------|---------------|-------------------|
| **Anthropic** | Claude AI model | $5 kredi |
| **OpenAI** | GPT model | $5 kredi |
| **Tavily** | Web araması | 1000 arama/ay |

## 📋 Kurulum Sorun Giderme

### ❌ Yaygın Sorunlar

**1. ModuleNotFoundError**
```bash
pip install -r requirements.txt
```

**2. Database Connection Error**
```bash
# MySQL servisinin çalıştığından emin olun
# .env dosyasındaki credentials'ları kontrol edin
```

**3. API Key Errors**
```bash
# .env dosyasındaki API anahtarlarını kontrol edin
# Anahtarların geçerli olduğundan emin olun
```

**4. Port Already in Use**
```bash
# MCP server için farklı port kullanın
python dataturkmcp.py --port 8001
```

## 🤝 Katkıda Bulunma

1. Fork yapın
2. Feature branch oluşturun (`git checkout -b feature/amazing-feature`)
3. Commit yapın (`git commit -m 'Add amazing feature'`)
4. Push yapın (`git push origin feature/amazing-feature`)
5. Pull Request açın

## 📄 Lisans

Bu proje MIT lisansı altında yayınlanmıştır. Detaylar için [LICENSE](LICENSE) dosyasına bakın.

## 👨‍💻 Geliştirici

**Halil Kaya**
- 🌐 GitHub: [@halilkkaya](https://github.com/halilkkaya)

## 🙏 Teşekkürler

- **Anthropic** - Claude AI modeli
- **OpenAI** - GPT modelleri  
- **FastMCP** - MCP framework
- **Tavily** - Web arama API'si
- **Streamlit** - Web arayüzü

---

⭐ **Bu projeyi beğendiyseniz yıldız vermeyi unutmayın!**

📧 **Sorularınız için**: [Issues](https://github.com/halilkkaya/mcp-anlatim/issues) bölümünü kullanın

🔄 **Güncellemeler için**: Repository'yi watch edin
