import streamlit as st
import requests
import json
import anthropic
import os
from dotenv import load_dotenv

# .env dosyasını yükle
load_dotenv()

# Sayfa yapılandırması
st.set_page_config(
    page_title="MCP Server Anlatımı",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Ana başlık
st.title("🚗 Araba Arama MCP Server Anlatımı")
st.markdown("---")

# Sidebar - İçindekiler
st.sidebar.title("📋 İçindekiler")
page = st.sidebar.radio(
    "Konuları seçin:",
    [
        "MCP Nedir?",
        "Server Özellikleri", 
        "Tool'lar",
        "Örnek Kullanım",
        "Teknik Detaylar",
        "Canlı Test"
    ]
)

if page == "MCP Nedir?":
    st.header("MCP (Model Context Protocol) Nedir?")
    
    # Temel tanım
    st.markdown("""
    <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                padding: 20px; border-radius: 10px; color: white; margin-bottom: 20px;'>
        <h3>🎯 MCP Basit Tanımı</h3>
        <p style='font-size: 18px; margin: 0;'>
        <strong>Model Context Protocol (MCP)</strong>, AI modellerinin dış sistemlere (veritabanları, API'lar, dosya sistemleri) 
        güvenli ve standart bir şekilde erişebilmesini sağlayan bir protokoldür.
        </p>
        <br>
        <p style='font-size: 16px; margin: 0; opacity: 0.9;'>
        ✨ <strong>Tek cümle:</strong> "AI'ların function calling yapmasının standart yolu"
        </p>
        <p style='font-size: 14px; margin-top: 10px; opacity: 0.8;'>
        💡 <em>Not: Modern LLM'ler zaten function calling yapabiliyor, MCP bunu organize ediyor!</em>
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Pratik örnek
    st.subheader("🧠 MCP Nasıl Çalışır? - Pratik Örnek")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("""
        **🤔 MCP Öncesi Durum:**
        
        **Entegrasyon Karmaşası:**
        - LLM'ler eğitim verilerindeki bilgilerle sınırlı
        - Canlı/güncel verilere erişimleri yok
        - Her uygulama kendi function calling formatını kullanıyordu
        - Aynı araç farklı uygulamalarda farklı şekilde tanımlanıyordu
        
        **Örnek:** Claude function calling yapabiliyor ama her uygulama farklı tool formatı kullanıyor
        """)
    
    with col2:
        st.markdown("""
        **✅ MCP ile Çözüm:**
        
        **Standartlaştırılmış Protokol:**
        - Tüm uygulamalar aynı tool format standardını kullanıyor
        - JSON-RPC 2.0 tabanlı tutarlı iletişim
        - Bir kez yazılan tool tüm MCP uygulamalarında çalışıyor
        - Modeller zaten function calling yapabiliyor, MCP bunu organize ediyor
        
        **Sonuç:** Aynı araçlar farklı uygulamalarda tutarlı şekilde kullanılabiliyor!
        """)
    
    # Mimari açıklama
    st.markdown("""
    ### 🏗️ MCP Mimarisi Basitçe
    
    **MCP'nin 3 Ana Bileşeni:**
    
    **🖥️ 1. MCP Server (Tool Sağlayıcısı):**
    - Gerçek işlemleri yapan araçları (tools) barındırır
    - Veritabanı sorguları, API çağrıları, dosya işlemleri vb.
    - JSON-RPC 2.0 protokolü üzerinden iletişim kurar
    - Tool'ların açıklamalarını (schema) standart formatta sunar
    
    **🔗 2. MCP Client (Aracı Katman):**  
    - LLM ile MCP Server arasında köprü görevi görür
    - Server'dan tool listesini alır ve modele sunar
    - Model'in tool çağrılarını Server'a iletir
    - Sonuçları model için uygun formata dönüştürür
    
    **🤖 3. LLM (Büyük Dil Modeli):**
    - Function calling yeteneği built-in olarak gelir (GPT-4, Claude vb.)
    - MCP Client'tan gelen tool açıklamalarını anlayıp kullanır
    - Kullanıcı ihtiyacına göre uygun tool'u seçer  
    - MCP standardında doğru parametrelerle tool çağrısı yapar
    
    **🔄 İletişim Akışı:**
    `Kullanıcı ↔ LLM ↔ MCP Client ↔ MCP Server ↔ Veri Kaynağı`
    """)
    
    # N x M problemi
    st.subheader("🚨 MCP Neden Gerekli Oldu? - N×M Entegrasyon Problemi")
    
    # Somut örnek senaryosu
    st.markdown("""
    **🏢 Gerçek Dünya Problemi:** 
    
    Modern AI modelleri (GPT-4, Claude, Gemini) function calling yapabiliyordu, ama her uygulama kendi tool formatını kullanıyordu. Aynı veritabanı aracını farklı uygulamalarda farklı şekilde tanımlamak gerekiyordu.
    
    **📊 Matematik:** N tane Uygulama × M tane Tool = N×M farklı tool tanımı!
    """)
    
    st.info("""
    **💡 Örnek Senaryo:** 3 AI Uygulaması × 4 Araç = 12 Farklı Tool Tanımı!
    
    Aynı "veritabanı sorgula" aracı, her uygulamada farklı parametre adları ve formatlarla tanımlanıyordu.
    """)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("""
        **⚠️ MCP Öncesi: Kaos Ortamı**
        
        **3 Model × 4 Sistem = 12 Farklı Entegrasyon!**
        
        **📊 Modeller:**
        - GPT-4 (OpenAI)
        - Claude (Anthropic) 
        - Gemini (Google)
        
        **🔧 Sistemler:**
        - MySQL Veritabanı
        - GitHub Repository
        - Slack Workspace
        - Google Drive
        """)
        
        st.markdown("""
        **💀 Her Model İçin Ayrı Kod:**
        
        ```python
        # GPT-4 için MySQL bağlantısı
        def gpt4_mysql_connect():
            # GPT-4 özel format
            return {"type": "openai_sql", "query": sql}
        
        # Claude için MySQL bağlantısı  
        def claude_mysql_connect():
            # Anthropic özel format
            return {"tool": "database", "sql": sql}
            
        # Gemini için MySQL bağlantısı
        def gemini_mysql_connect():
            # Google özel format
            return {"function": "sql_exec", "command": sql}
        ```
        """)
    
    with col2:
        st.markdown("""
        **✅ MCP ile: Düzen**
        
        **1 Standart × Tüm Modeller = 1 Entegrasyon!**
        
        **🎯 Tek MCP Server:**
        - Tüm modeller aynı server'ı kullanır
        - Aynı tool açıklamaları
        - Aynı protokol (JSON-RPC 2.0)
        - Aynı güvenlik katmanı
        """)
        
        st.markdown("""
        **🚀 Tek Kod, Tüm Modeller:**
        
        ```python
        # MCP ile - TÜM modeller için aynı kod
        @mcp_tool("araba_ara")
        def search_cars(marka: str, model: str):
            # Bu tool'u HERKES kullanabilir:
            # - GPT-4 ✅
            # - Claude ✅  
            # - Gemini ✅
            # - Yeni modeller ✅
            return db.query(marka, model)
        ```
        """)
    
    # Detaylı custom protokol örnekleri
    st.markdown("""
    ### 🔥 Custom Protokol Cehenneminden Örnekler
    """)
    
    examples = {
        "🗄️ Veritabanı Erişimi": {
            "openai": """
            # OpenAI için custom kod
            {
                "functions": [{
                    "name": "query_database",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "sql_query": {"type": "string"}
                        }
                    }
                }]
            }
            """,
            "anthropic": """
            # Anthropic için farklı format
            {
                "tools": [{
                    "name": "database_tool",
                    "input_schema": {
                        "type": "object", 
                        "properties": {
                            "query": {"type": "string"}
                        }
                    }
                }]
            }
            """,
            "google": """
            # Google için başka format
            {
                "function_declarations": [{
                    "name": "execute_sql",
                    "parameters": {
                        "type": "OBJECT",
                        "properties": {
                            "sql_statement": {"type": "STRING"}
                        }
                    }
                }]
            }
            """
        },
        "🐙 GitHub API": {
            "openai": "OpenAI: functions.github_search({'repo': 'name', 'query': 'text'})",
            "anthropic": "Anthropic: tools.github_tool({'repository': 'name', 'search_term': 'text'})", 
            "google": "Google: function_calls.search_github({'project': 'name', 'keyword': 'text'})"
        },
        "💬 Slack Entegrasyonu": {
            "openai": "OpenAI: slack_integration.send_message(channel, text)",
            "anthropic": "Anthropic: slack_tool.post_message(room, content)",
            "google": "Google: slack_function.message_send(workspace, message)"
        }
    }
    
    for system, formats in examples.items():
        with st.expander(f"{system} - Her Model Farklı Format!", expanded=False):
            if isinstance(formats, dict) and 'openai' in formats:
                # Veritabanı örneği - kod blokları
                tab1, tab2, tab3 = st.tabs(["OpenAI Format", "Anthropic Format", "Google Format"])
                
                with tab1:
                    st.code(formats['openai'], language='json')
                with tab2:
                    st.code(formats['anthropic'], language='json')
                with tab3:
                    st.code(formats['google'], language='json')
            else:
                # Diğer örnekler - basit metin
                for provider, example in formats.items():
                    st.markdown(f"**{provider.upper()}:** `{example}`")
    
    # Geliştirici yaşadığı zorluklar
    st.markdown("""
    ### 😤 Geliştiricinin Yaşadığı Zorluklar
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **⏰ Zaman Kaybı Örnekleri:**
        - Model değiştirmek = 2-3 hafta yeniden yazma
        - Yeni API eklemek = Her model için ayrı implementation  
        - Bug fix = 3 farklı yerde aynı hatayı düzeltme
        - Testing = 3×4=12 farklı test senaryosu
        - Documentation = Her model için ayrı döküman
        """)
    
    with col2:
        st.markdown("""
        **💸 Maliyet Artışları:**
        - 3 farklı AI takımı (OpenAI, Anthropic, Google uzmanları)
        - 12 farklı API entegrasyonu maintenance
        - Çoklu support contract'ları
        - Her model değişikliğinde full regression test
        - Developer onboarding: 1 ay → 3 ay
        """)
    
    # MCP ile nasıl çözülüyor
    st.success("""
    🎯 **MCP Çözümü:** Bir tool yazıyorsun, tüm modeller kullanıyor! 
    - `araba_ara` tool'unu bir kez yaz → GPT-4, Claude, Gemini hepsi kullanır
    - Yeni model çıktı? → Anında uyumlu, ek kod yok
    - Bug fix? → Tek yerde düzelt, heryerde çalışır
    """)
    
    # MCP ile tek tool örneği
    st.markdown("""
    ### 🚀 MCP ile Tek Tool - Tüm Modeller İçin
    """)
    
    st.markdown("""
    **Yukarıdaki 12 farklı entegrasyonu tek bir MCP server'da nasıl yazıyoruz:**
    """)
    
    # Tab'lar ile farklı sistemler
    tab1, tab2, tab3, tab4 = st.tabs(["🗄️ Veritabanı", "🐙 GitHub", "💬 Slack", "📁 Google Drive"])
    
    with tab1:
        st.markdown("**MCP ile Veritabanı Tool'u - Tüm modeller kullanır:**")
        st.code("""
# Tek tool - TÜM modeller için çalışır
@mcp_tool("veritabani_sorgula")
def query_database(
    sorgu: str,
    tablo: str = "arabalar",
    limit: int = 10
) -> dict:
    \"\"\"
    Veritabanında SQL sorgusu çalıştırır.
    
    Args:
        sorgu: SQL sorgu metni  
        tablo: Hedef tablo adı
        limit: Maksimum sonuç sayısı
    \"\"\"
    try:
        # Güvenli SQL execution
        result = db.execute(sorgu, tablo, limit)
        return {
            "durum": "başarılı",
            "sonuc_sayisi": len(result),
            "veriler": result
        }
    except Exception as e:
        return {"durum": "hata", "mesaj": str(e)}

# Kullanım - TÜM modeller aynı syntax:
# - GPT-4: veritabani_sorgula("SELECT * FROM arabalar", limit=5)
# - Claude: veritabani_sorgula("SELECT * FROM arabalar", limit=5) 
# - Gemini: veritabani_sorgula("SELECT * FROM arabalar", limit=5)
        """, language='python')
    
    with tab2:
        st.markdown("**MCP ile GitHub Tool'u - Tüm modeller kullanır:**")
        st.code("""
@mcp_tool("github_ara")
def search_github(
    repo_sahibi: str,
    repo_adi: str,
    arama_terimi: str,
    dosya_tipi: str = "py"
) -> dict:
    \"\"\"
    GitHub repository'de kod araması yapar.
    
    Args:
        repo_sahibi: Repository sahibinin kullanıcı adı
        repo_adi: Repository adı
        arama_terimi: Aranacak kod parçası
        dosya_tipi: Dosya uzantısı (py, js, ts vb.)
    \"\"\"
    try:
        # GitHub API çağrısı
        results = github_api.search_code(
            f"repo:{repo_sahibi}/{repo_adi} {arama_terimi} extension:{dosya_tipi}"
        )
        return {
            "durum": "başarılı", 
            "bulunan_dosya_sayisi": results.total_count,
            "dosyalar": [{"dosya": item.name, "yol": item.path} for item in results.items]
        }
    except Exception as e:
        return {"durum": "hata", "mesaj": str(e)}

# Önceden: 3 farklı GitHub integration 
# Şimdi: 1 tool → Herkes kullanır!
        """, language='python')
    
    with tab3:
        st.markdown("**MCP ile Slack Tool'u - Tüm modeller kullanır:**")
        st.code("""
@mcp_tool("slack_mesaj_gonder")
def send_slack_message(
    kanal: str,
    mesaj: str,
    kullanici_etiketle: str = None
) -> dict:
    \"\"\"
    Slack kanalına mesaj gönderir.
    
    Args:
        kanal: Slack kanal adı (#genel, #ai-team vb.)
        mesaj: Gönderilecek mesaj içeriği
        kullanici_etiketle: Etiketlenecek kullanıcı (@ahmet vb.)
    \"\"\"
    try:
        # Slack API entegrasyonu
        full_message = f"{kullanici_etiketle} {mesaj}" if kullanici_etiketle else mesaj
        response = slack_client.chat_postMessage(
            channel=kanal,
            text=full_message
        )
        return {
            "durum": "başarılı",
            "mesaj_id": response["ts"],
            "kanal": response["channel"]
        }
    except Exception as e:
        return {"durum": "hata", "mesaj": str(e)}

# Tüm modeller aynı şekilde kullanır:
# slack_mesaj_gonder("#ai-team", "Deployment tamamlandı!", "@takım")
        """, language='python')
    
    with tab4:
        st.markdown("**MCP ile Google Drive Tool'u - Tüm modeller kullanır:**")
        st.code("""
@mcp_tool("drive_dosya_ara")
def search_drive_files(
    arama_terimi: str,
    dosya_tipi: str = "document",
    klasor_id: str = None
) -> dict:
    \"\"\"
    Google Drive'da dosya araması yapar.
    
    Args:
        arama_terimi: Dosya adında aranacak terim
        dosya_tipi: document, spreadsheet, presentation
        klasor_id: Belirli klasörde arama (opsiyonel)
    \"\"\"
    try:
        # Google Drive API sorgusu
        query = f"name contains '{arama_terimi}' and mimeType contains '{dosya_tipi}'"
        if klasor_id:
            query += f" and parents in '{klasor_id}'"
            
        results = drive_service.files().list(q=query).execute()
        files = results.get('files', [])
        
        return {
            "durum": "başarılı",
            "bulunan_dosya_sayisi": len(files),
            "dosyalar": [{"ad": f["name"], "id": f["id"], "link": f["webViewLink"]} for f in files]
        }
    except Exception as e:
        return {"durum": "hata", "mesaj": str(e)}

# Önceden: Her model için farklı Google Drive kodu
# Şimdi: Tek tool, evrensel kullanım!
        """, language='python')
    
    # Karşılaştırma tablosu
    st.markdown("""
    ### 📊 Kod Karşılaştırması: Öncesi vs Sonrası
    """)
    
    comparison_data = {
        "Sistem": ["Veritabanı", "GitHub API", "Slack API", "Google Drive"],
        "MCP Öncesi": [
            "3 farklı DB connector", 
            "3 farklı GitHub client",
            "3 farklı Slack integration", 
            "3 farklı Drive wrapper"
        ],
        "MCP ile": [
            "1 tool → Herkes kullanır",
            "1 tool → Herkes kullanır", 
            "1 tool → Herkes kullanır",
            "1 tool → Herkes kullanır"
        ],
        "Kod Azalması": [
            "75% ↓", "75% ↓", "75% ↓", "75% ↓"
        ]
    }
    
    st.table(comparison_data)
    
    # Tool açıklamalarının modellere nasıl gözüktüğü
    st.markdown("""
    ### 🔍 Modeller Tool'ları Nasıl Görüyor?
    """)
    
    st.info("""
    **🤖 Model'in gözünden tool açıklaması:**
    
    ```
    Tool: veritabani_sorgula
    Açıklama: Veritabanında SQL sorgusu çalıştırır
    Parametreler:
      - sorgu (string, zorunlu): SQL sorgu metni
      - tablo (string, opsiyonel): Hedef tablo adı, varsayılan: arabalar  
      - limit (integer, opsiyonel): Maksimum sonuç sayısı, varsayılan: 10
    ```
    
    **Model düşüncesi:** "Toyota Supra araması yapmak istiyorum. Bu tool tam ihtiyacım olan şey! 
    Parametreleri şöyle vereyim: sorgu='SELECT * FROM arabalar WHERE marka=Toyota AND model=Supra', limit=5"
    """)
    
    st.success("""
    🎯 **Sonuç:** 12 farklı entegrasyon → 4 MCP tool → Tüm modeller mutlu!
    
    - **Geliştirici:** Bir kez yaz, her yerde çalışır
    - **Model:** Açıklama oku, parametreleri ver, işlem yapsın  
    - **Kullanıcı:** Hangi model olursa olsun aynı kalitede hizmet
    """)
    
    # Function calling açıklaması
    st.info("""
    **💡 Önemli:** MCP, function calling (fonksiyon çağırma) yapma işleminin standartlaştırılmış halidir. 
    """)
    
    # LLM sınırları
    st.markdown("""
    ### 📚 LLM'lerin Bilgi Sınırları ve MCP Çözümü
    
    **🔒 LLM'lerin Doğal Sınırları:**
    - Eğitim verilerindeki bilgiler sınırlı
    - Güncel bilgileri bilmiyorlar
    - Canlı verilere erişimleri yok
    - Özel şirket verilerine ulaşamazlar
    
    **🔓 MCP ile Çözüm:**
    - Gerçek zamanlı veri erişimi
    - Özel veritabanlarına bağlantı
    - Güncel API'lara erişim
    - Şirket içi sistemlere güvenli erişim
    """)
    
    # Ana Before/After görsel
    st.markdown("---")
    st.image("MCP-Before-After-1024x576.jpeg", 
             caption="MCP Öncesi vs MCP Sonrası: AI uygulamalarında veri erişimi ve tool kullanımındaki devrim",
             use_container_width=True)
    
    st.markdown("---")
    
    # Before MCP bölümü
    st.subheader("🔴 MCP Öncesi Durum: Karmaşa ve Zorluklar")
    
    col1, col2 = st.columns([1, 2])
        
    with col1:
            st.markdown("""
        **Görselde ne görüyoruz?**
        
        Soldaki resimde bir geliştirici:
        - Laptopunda farklı AI araçları
        - Telefonunda ayrı uygulamalar  
        - Her tool için farklı API'lar
        - Kafası karışık, soru işaretleri
        - Dağınık, bağlantısız ekosistem
        """)
        
    with col2:
            st.markdown("""
        **MCP Öncesinde Geliştiriciler Ne Yaşardı?**
        
        **🔧 Teknik Zorluklar:**
        - Her veri kaynağı için ayrı API (uygulama arayüzü) entegrasyonu
        - Farklı kimlik doğrulama (authentication) sistemleri
        - Çoklu SDK (yazılım geliştirme kiti) ve kütüphane yönetimi
        - Her servis için farklı hata yönetimi (error handling)
        - Tutarsız veri formatları
        
        **⏰ Zaman Kayıpları:**
        - Her yeni entegrasyon için haftalarca geliştirme
        - API dokümantasyonlarını öğrenme süreci
        - Hız sınırlaması (rate limiting) ve kota yönetimi
        - Hata ayıklama (debugging) ve sorun giderme karmaşası
        
        **💰 Maliyet Artışları:**
        - Ayrı ayrı destek maliyetleri
        - Bakım yükü (maintenance overhead)
        - Geliştirme kaynak israfı
        """)
    
    # Detaylı problem analizi
    st.markdown("""
    ### 📊 MCP Öncesi Problemlerin Detaylı Analizi
    """)
    
    problem_areas = {
        "🔌 API Entegrasyonu": {
            "problemler": [
                "Her API için farklı kimlik doğrulama (API anahtarı, OAuth, Bearer token)",
                "Farklı istek/yanıt formatları (REST, GraphQL, SOAP)",
                "Tutarsız hata kodları ve yönetimi",
                "Hız sınırlaması (rate limiting) politikaları",
                "Sürüm yönetimi (version management) karmaşası"
            ],
            "örnek": "GitHub API + Slack API + Google Drive API = 3 farklı kimlik sistemi, 3 farklı geliştirme kiti, 3 farklı hata yönetimi"
        },
        "🔒 Güvenlik Yönetimi": {
            "problemler": [
                "Çoklu API anahtarı yönetimi",
                "Farklı izin (permission) sistemleri", 
                "Erişim jetonu (token) yenileme mekanizmaları",
                "Kimlik bilgisi değiştirme zorluğu",
                "Denetim izi (audit trail) karmaşası"
            ],
            "örnek": "Her servis için ayrı .env dosyası, farklı güvenlik en iyi uygulamaları"
        },
        "📈 Ölçeklenebilirlik Sorunları": {
            "problemler": [
                "Bağlantı havuzu (connection pool) yönetimi",
                "Yük dengeleme (load balancing) karmaşası",
                "İzleme (monitoring) ve uyarı sistemleri",
                "Performans optimizasyonu",
                "Kaynak yönetimi (resource management)"
            ],
            "örnek": "Veritabanı + Redis + API + Dosya Sistemi = 4 farklı ölçeklendirme stratejisi"
        },
        "👥 Geliştirici Deneyimi": {
            "problemler": [
                "Dik öğrenme eğrisi (steep learning curve)",
                "Dokümantasyon avcılığı",
                "Hata ayıklama (debugging) zorlukları",
                "Test etme karmaşıklığı",
                "Bakım yükü (maintenance burden)"
            ],
            "örnek": "Yeni geliştirici işe alıştırma: 2-3 hafta sadece araçları öğrenmek için"
        }
    }
    
    for area, details in problem_areas.items():
        with st.expander(area, expanded=False):
            col1, col2 = st.columns([2, 1])
            with col1:
                st.markdown("**Ana Problemler:**")
                for problem in details["problemler"]:
                    st.markdown(f"- {problem}")
            with col2:
                st.markdown("**Gerçek Dünya Örneği:**")
                st.info(details["örnek"])
    
    st.markdown("---")
    
    # After MCP bölümü
    st.subheader("🟢 MCP Sonrası Durum: Birlik ve Kolaylık")
    
    col1, col2 = st.columns([1, 2])
        
    with col1:
            st.markdown("""
        **Görselde ne görüyoruz?**
        
        Sağdaki resimde:
        - MCP merkezi hub olarak
        - Tüm servisler tek noktadan
        - GitHub, Google, Slack unified
        - Rahat, güvenli kullanım
        - Organize edilmiş ekosistem
            """)
        
    with col2:
            st.markdown("""
        **MCP ile Neler Değişti?**
        
        **🚀 Teknik Avantajlar:**
        - Tek standart protokol (JSON-RPC 2.0)
        - Birleşik kimlik doğrulama sistemi
        - Standartlaştırılmış hata yönetimi
        - Otomatik araç keşfi (tool discovery)
        - Yerleşik güvenlik önlemleri
        
        **⚡ Geliştirme Hızı:**
        - Tak ve çalıştır (plug & play) entegrasyonlar
        - 5 dakikada yeni araç ekleme
        - Sıfır yapılandırma kurulumu
        - Otomatik yedekleme (failover)
        - Gerçek zamanlı hata ayıklama
        
        **💡 Geliştirici Deneyimi:**
        - Tek entegrasyon noktası
        - Tutarlı API desenler
        - Yerleşik izleme sistemi
        - Otomatik ölçeklendirme
        - Topluluk odaklı ekosistem
        """)
    
    # MCP'nin getirdiği çözümler
    st.markdown("""
    ### ✅ MCP'nin Getirdiği Devrimsel Çözümler
    """)
    
    solutions = {
        "🔧 Standardizasyon": {
            "açıklama": "Tek protokol, tutarlı deneyim",
            "detay": [
                "JSON-RPC 2.0 tabanlı iletişim",
                "Standartlaştırılmış araç tanımları", 
                "Tutarlı hata formatları",
                "Birleşik kimlik doğrulama akışı",
                "Ortak izleme arayüzleri"
            ],
            "before_after": {
                "before": "5 farklı API → 5 farklı entegrasyon deseni",
                "after": "5 farklı API → 1 MCP entegrasyon deseni"
            }
        },
        "🔌 Tak ve Çalıştır Mimarisi": {
            "açıklama": "Anında bağlan, anında kullan",
            "detay": [
                "Otomatik keşif mekanizmaları",
                "Dinamik araç kaydı",
                "Çalışır durumda değiştirilebilir bileşenler",
                "Sıfır kesinti güncellemeleri",
                "Modüler mimari"
            ],
            "before_after": {
                "before": "Yeni API entegrasyonu: 2-3 hafta geliştirme",
                "after": "Yeni MCP sunucusu: 5-10 dakika kurulum"
            }
        },
        "🛡️ Yerleşik Güvenlik": {
            "açıklama": "Güvenlik varsayılan olarak gelir",
            "detay": [
                "Merkezi kimlik doğrulama",
                "Rol tabanlı erişim kontrolü",
                "Otomatik kimlik bilgisi yönetimi",
                "Denetim günlüğü",
                "Güvenlik politikası uygulaması"
            ],
            "before_after": {
                "before": "Her API için ayrı güvenlik uygulaması",
                "after": "MCP güvenlik katmanı tüm araçları korur"
            }
        },
        "📊 İzleme ve Gözlemlenebilirlik": {
            "açıklama": "Her şeyi görebilir, kontrol edebilirsiniz",
            "detay": [
                "Gerçek zamanlı ölçümler",
                "Dağıtık izleme",
                "Performans analitiği",
                "Hata takibi",
                "Kullanım öngörüleri"
            ],
            "before_after": {
                "before": "5 farklı izleme gösterge paneli",
                "after": "Tek birleşik izleme arayüzü"
            }
        }
    }
    
    for solution, details in solutions.items():
        with st.expander(solution, expanded=False):
            st.markdown(f"**{details['açıklama']}**")
            
            col1, col2 = st.columns(2)
        
        with col1:
                st.markdown("**Teknik Detaylar:**")
                for item in details["detay"]:
                    st.markdown(f"- {item}")
        
        with col2:
                st.markdown("**Before vs After:**")
                st.error(f"**Önce:** {details['before_after']['before']}")
                st.success(f"**Sonra:** {details['before_after']['after']}")
    
    st.markdown("---")
    
    # MCP'nin gerçek dünya etkisi
    st.subheader("🌍 MCP'nin Gerçek Dünya Etkisi")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        **🚀 Yeni Girişimler İçin**
        - Minimum Uygulanabilir Ürün geliştirme: Aylardan haftalara
        - Entegrasyon maliyeti: %80 azalma
        - Pazara çıkış süresi: %60 hızlanma
        - Geliştirici verimliliği: %3x artış
        """)
    
    with col2:
        st.markdown("""
        **🏢 Kurumsal Şirketler İçin**
        - Eski sistem modernizasyonu
        - Mikroservis iletişimi
        - API geçidi basitleştirmesi
        - Satıcı bağımlılığı azaltması
        """)
        
    with col3:
        st.markdown("""
        **👨‍💻 Geliştiriciler İçin**
        - Öğrenme eğrisi: Çok daha düz
        - Kod bakımı: %70 azalma
        - Hata giderme: %50 hızlanma
        - Özellik geliştirme: %2x hız
        """)
    
    # Sonuç ve özet
    st.markdown("""
    ### 🎯 Özet: MCP Neden Devrimsel?
    
    MCP sadece bir protokol değil, AI uygulama geliştirme paradigmasını tamamen değiştiren bir yaklaşım. 
    Görselde gördüğünüz gibi, karmaşadan düzene, zorluklardan kolaylığa, dağınıklıktan birliğe geçiş sağlıyor.
    
    **Bu projede MCP'yi nasıl kullandık?**
    - Araç veritabanımıza erişim için MCP server geliştirdik
    - Claude gibi AI modelleri bu server'ı kullanarak veri sorgulayabiliyor
    - Tek seferde kurulum, sürekli kullanım
    - Güvenli, hızlı ve ölçeklenebilir çözüm
    """)
    
    # Call to action
    st.info("""
    💡 **Sonraki adım:** Server Özellikleri bölümünde bizim MCP server implementasyonumuzu detaylı olarak inceleyelim!
    """)

elif page == "Server Özellikleri":
    st.header("Server Özellikleri")
    
    # Pratik örnek - MCP akışı
    st.subheader("🚗 Gerçek Dünya Örneği: Toyota Supra Araması")
    
    st.markdown("""
    **Senaryo:** Kullanıcı modele şunu soruyor: *"Bana 2 adet Toyota Supra arada öner"*
    
    İşte MCP'nin bu basit soru için nasıl devreye girdiği:
    """)
    
    # Adım adım akış
    st.markdown("""
    ### 🔄 MCP Akış Diyagramı
    """)
    
             # MCP Akış Diyagramı
    st.image("diyagram.png", 
             caption="MCP Akış Diyagramı: Toyota Supra arama süreci - Kullanıcıdan veritabanına kadar tüm adımlar",
             use_container_width=True)
    
    st.markdown("""
    ### 📋 Diyagramda Gösterilen Akış:
    
    **🔄 Soldan Sağa Akış:**
    1. **👤 Kullanıcı**: "2 adet Toyota Supra öner" talebi
    2. **🤖 Model (Claude)**: Veri eksikliğini fark ediyor
    3. **🔗 MCP Client**: Tool listesini kontrol ediyor  
    4. **⚙️ MCP Server**: `araba_ara` tool'unu tanıtıyor
    5. **🗄️ Veritabanı**: SQL sorgusu çalıştırılıyor
    
    **🔙 Sağdan Sola Yanıt:**
    1. **🗄️ Veritabanı**: Sonuç verileri döndürüyor
    2. **⚙️ MCP Server**: JSON formatında veri hazırlıyor
    3. **🤖 Model**: Formatlanmış veriyi alıyor
    4. **👤 Kullanıcı**: "İşte 2 Toyota Supra önerim..." yanıtını alıyor
    
    **🎯 Kritik Noktalar:**
    - Model SQL bilmiyor ama tool açıklamasını anlıyor
    - Parametreler otomatik olarak doğru formatta iletiliyor
    - Güvenlik katmanı devrede (direkt DB erişimi yok)
    - Tüm süreç standart MCP protokolü ile yönetiliyor
    """)
    
    # Adım adım açıklama
    st.markdown("""
    ### 📋 Adım Adım MCP Süreci
    """)
    
    steps = [
        {
            "step": "1️⃣ Kullanıcı Sorusu",
            "actor": "👤 Kullanıcı",
            "action": '"Bana 2 adet Toyota Supra arada öner"',
            "detail": "Basit bir araç önerisi talebi"
        },
        {
            "step": "2️⃣ Model Farkındalığı", 
            "actor": "🤖 Model (Claude)",
            "action": "Bu verilerin kendimde olmadığını anlıyorum",
            "detail": "Model kendi sınırlarını biliyor ve dış veriye ihtiyaç duyduğunu anlıyor"
        },
        {
            "step": "3️⃣ Tool Keşfi",
            "actor": "🔗 MCP Client", 
            "action": "MCP Server'a bağlanıp mevcut tool'ları kontrol ediyor",
            "detail": "Client, server'ın sunduğu tool'ları ve açıklamalarını alıyor"
        },
        {
            "step": "4️⃣ Tool Analizi",
            "actor": "⚙️ MCP Server",
            "action": "araba_ara tool'unu tanıtıyor",
            "detail": "Tool açıklaması: marka, model, limit parametreleri gerekli"
        },
        {
            "step": "5️⃣ Tool Seçimi",
            "actor": "🤖 Model",
            "action": '"Bu tool tam ihtiyacım olan şey!"',
            "detail": "Model tool açıklamasını okuyup uygun parametreleri hazırlıyor"
        },
        {
            "step": "6️⃣ Tool Çağrısı",
            "actor": "🤖 Model → ⚙️ Server",
            "action": 'araba_ara(marka="Toyota", model="Supra", limit=2)',
            "detail": "Doğru parametrelerle tool çağrısı yapılıyor"
        },
        {
            "step": "7️⃣ Veritabanı Sorgusu",
            "actor": "⚙️ Server → 🗄️ DB",
            "action": "SQL sorgusu otomatik oluşturuluyor ve çalıştırılıyor",
            "detail": "SELECT * FROM arabalar WHERE marka='Toyota' AND model='Supra' LIMIT 2"
        },
        {
            "step": "8️⃣ Veri Formatlaması",
            "actor": "⚙️ MCP Server",
            "action": "Sonuçları JSON formatında hazırlıyor",
            "detail": "Ham veritabanı verileri model için uygun formata dönüştürülüyor"
        },
        {
            "step": "9️⃣ Model Yanıtı",
            "actor": "🤖 Model",
            "action": "Verileri kullanıcı dostu formatta sunuyor",
            "detail": "JSON verileri doğal dille açıklamalı şekilde kullanıcıya sunuluyor"
        }
    ]
    
    for i, step_info in enumerate(steps):
        with st.expander(f"{step_info['step']} {step_info['actor']}", expanded=False):
            col1, col2 = st.columns([1, 2])
                
            with col1:
                    st.markdown(f"""
                **Eylem:**
                {step_info['action']}
                """)
                
            with col2:
                    st.markdown(f"""
                **Detay:**
                {step_info['detail']}
                """)
    
    # Bu sürecin avantajları
        st.markdown("""
    ### ✅ Bu Sürecin Avantajları
    """)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
        **🎯 Model Açısından:**
        - SQL bilmek zorunda değil
        - Veritabanı yapısını bilmek zorunda değil  
        - Sadece tool açıklamasını anlayabilmesi yeterli
        - Her yeni tool otomatik kullanılabilir
        
        **🛠️ Geliştirici Açısından:**
        - Model eğitmeye gerek yok
        - Custom API yazmaya gerek yok
        - Standart MCP protokolü yeterli
        - Yeni tool ekleme 5 dakika
            """)
        
        with col2:
            st.markdown("""
        **🔒 Güvenlik Açısından:**
        - Model direkt veritabanına erişmiyor
        - MCP Server güvenlik katmanı
        - Parametreler doğrulanıyor
        - SQL injection koruması
        
        **📈 Performans Açısından:**
        - Optimize edilmiş sorgular
            - Connection pooling
        - Caching mekanizması
        - Error handling
        """)
    
    # Gerçek dünya karşılaştırması
        st.markdown("""
    ### 🆚 MCP ile vs MCP olmadan
    """)
    
    comparison_data = {
        "Süreç": [
            "API Geliştirme",
            "Veritabanı Erişimi", 
            "Yeni Tool Ekleme",
            "Güvenlik Yönetimi",
            "Maintenance"
        ],
        "MCP Olmadan": [
            "Custom REST API geliştir",
            "Direct SQL connection",
            "2-3 hafta geliştirme",
            "Manual implementation",
            "Her API ayrı ayrı"
        ],
        "MCP ile": [
            "MCP standardı yeterli",
            "Güvenli MCP layer",
            "5-10 dakika setup",
            "Built-in security",
            "Tek noktadan yönetim"
        ]
    }
    
    st.table(comparison_data)
    
    # Call to action
    st.success("""
    🎯 **Sonuç:** MCP, karmaşık backend işlemlerini basit tool açıklamalarına dönüştürüyor. 
    Model ne istediğini söylüyor, MCP Server nasıl yapacağını biliyor!
    """)
    
    st.markdown("""
    Bu bolumde server ozelliklerini inceleyecegiz.
    """)
    
    # Buraya beraber server ozellikleri yazacagiz

elif page == "Tool'lar":
    st.header("🛠️ Mevcut Tool'lar")
    
    # Ana arama tool'u
    st.subheader("🔍 araba_ara - Ana Arama Tool'u")
    
    with st.expander("Parametreler ve Özellikler", expanded=True):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            **🔸 Temel Filtreler:**
            - `marka`: Araç markası (ford, toyota, vb.)
            - `model`: Model adı (focus, corolla, vb.)
            - `min_fiyat` / `max_fiyat`: Fiyat aralığı
            - `min_yil` / `max_yil`: Model yılı aralığı
            - `min_km` / `max_km`: Kilometre aralığı
            - `il`: Şehir filtreleme
            
            **🔸 Araç Özellikleri:**
            - `yakit`: Yakıt türü (benzin, dizel, hibrit, elektrik)
            - `vites`: Vites türü (manuel, otomatik)
            - `durum`: Araç durumu (yeni, sıfır, ikinci el)
            - `tip`: Araç tipi (sedan, SUV, hatchback)
            - `renk`: Araç rengi
            """)
        
        with col2:
            st.markdown("""
            **🔸 Gelişmiş Özellikler:**
            - `ozel_arama`: Önceden tanımlanmış kategoriler
              - `ekonomik`: Düşük yakıt tüketimi + uygun fiyat
              - `lüks`: Yüksek fiyat + mükemmel durum
              - `aile`: Sedan/SUV + güvenilir
              - `spor`: Coupe/convertible + yeni model
              - `yakıt_cimrisi`: Hibrit/elektrik/dizel
            
            **🔸 Görünüm Seçenekleri:**
            - `siralama`: fiyat_artan, fiyat_azalan, yil_yeni, km_az
            - `limit`: Sonuç sayısı (varsayılan: 5)
            - `detayli`: Açıklama bilgileri
            - `benzer_araclar`: Benzer araç önerileri
            - `istatistik`: Ortalama değerler
            """)
    
    # Diğer tool'lar
    st.subheader("📊 Diğer Tool'lar")
    
    tools_info = {
        "sql_sorgusu_calistir": {
            "açıklama": "Özel SQL sorguları çalıştırma",
            "kullanım": "Gelişmiş filtreleme ve analiz için",
            "örnek": "SELECT COUNT(*) FROM arabalar WHERE marka='BMW'"
        },
        "tablolari_listele": {
            "açıklama": "Veritabanındaki tüm tabloları listeler",
            "kullanım": "Veritabanı yapısını keşfetmek için",
            "örnek": "Hangi tablolar var?"
        },
        "tablo_yapisi_goster": {
            "açıklama": "Belirli bir tablonun sütunlarını gösterir",
            "kullanım": "Tablo şemasını incelemek için",
            "örnek": "arabalar tablosunun yapısı nedir?"
        },
        "web_arama": {
            "açıklama": "Tavily API ile web araması",
            "kullanım": "Güncel araç bilgileri için",
            "örnek": "2024 Toyota Corolla fiyatları"
        }
    }
    
    for tool_name, info in tools_info.items():
        with st.expander(f"🔧 {tool_name}"):
            st.write(f"**Açıklama:** {info['açıklama']}")
            st.write(f"**Kullanım:** {info['kullanım']}")
            st.code(f"Örnek: {info['örnek']}")

elif page == "Örnek Kullanım":
    st.header("💡 Örnek Kullanım Senaryoları")
    
    scenarios = {
        "🏠 Aile Aracı Arama": {
            "sorgu": "50-100 bin TL arası, 2018 sonrası, aile araçları",
            "parametreler": {
                "ozel_arama": "aile",
                "min_fiyat": 50000,
                "max_fiyat": 100000,
                "min_yil": 2018,
                "siralama": "fiyat_artan",
                "limit": 10
            }
        },
        "⚡ Ekonomik Araç": {
            "sorgu": "Yakıt cimrisi olan, ekonomik araçlar",
            "parametreler": {
                "ozel_arama": "ekonomik",
                "yakit": "hibrit",
                "max_fiyat": 150000,
                "siralama": "fiyat_artan"
            }
        },
        "🏎️ Spor Araç": {
            "sorgu": "BMW, coupe, yeni modeller",
            "parametreler": {
                "marka": "BMW",
                "tip": "coupe",
                "min_yil": 2020,
                "siralama": "yil_yeni",
                "detayli": True
            }
        },
        "📊 İstatistik Analizi": {
            "sorgu": "Toyota araçları için ortalama fiyat analizi",
            "parametreler": {
                "marka": "Toyota",
                "istatistik": True,
                "benzer_araclar": True,
                "limit": 15
            }
        }
    }
    
    for scenario_name, details in scenarios.items():
        with st.expander(scenario_name, expanded=False):
            st.write(f"**Arama Sorgusu:** {details['sorgu']}")
            st.json(details['parametreler'])
            
            if st.button(f"Bu sorguyu çalıştır", key=scenario_name):
                st.info("🚀 Bu özellik canlı test sayfasında mevcuttur!")

elif page == "Teknik Detaylar":
    st.header("🔧 Teknik Detaylar")
    
    tab1, tab2, tab3, tab4 = st.tabs(["📋 Kurulum", "⚙️ Yapılandırma", "🔒 Güvenlik", "📈 Performans"])
    
    with tab1:
        st.subheader("Kurulum Adımları")
        
        st.code("""
# 1. Gerekli paketleri yükleyin
pip install fastmcp mysql-connector-python python-dotenv tavily-python

# 2. Ortam değişkenlerini ayarlayın (.env dosyası)
MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=your_password
MYSQL_DATABASE=mcp_deneme
TAVILY_API_KEY=your_tavily_key

# 3. Veritabanını oluşturun
CREATE DATABASE mcp_deneme;

# 4. Server'ı başlatın
python dataturkmcp.py
        """)
    
    with tab2:
        st.subheader("Server Yapılandırması")
        
        st.markdown("""
        **🌐 Server Ayarları:**
        - **Host:** 0.0.0.0 (tüm network interface'lerde dinleme)
        - **Port:** 8000 (HTTP port)
        - **Transport:** streamable-http
        - **Tags:** public (herkese açık tool'lar)
        
        **📊 Veritabanı Ayarları:**
        - **Engine:** MySQL 8.0+
        - **Charset:** UTF-8
        - **Collation:** utf8mb4_unicode_ci
        - **Connection Pool:** Otomatik yönetim
        """)
    
    with tab3:
        st.subheader("Güvenlik Özellikleri")
        
        security_features = [
            "🔐 Ortam değişkenleri ile kimlik bilgileri koruması",
            "🛡️ SQL injection koruması (parametrized queries)",
            "🔒 Connection pooling ve otomatik cleanup",
            "⚠️ Error handling ve güvenli hata mesajları",
            "🚫 Aktif olmayan kayıtların filtrelenmesi",
            "🔍 Input validation ve sanitization"
        ]
        
        for feature in security_features:
            st.markdown(f"- {feature}")
    
    with tab4:
        st.subheader("Performans Optimizasyonları")
        
        st.markdown("""
        **🚀 Sorgu Optimizasyonları:**
        - İndexli sütunlar üzerinde arama
        - LIMIT kullanarak sonuç kısıtlama
        - Lazy loading ile bellek yönetimi
        - Connection pooling
        
        **📊 Veritabanı İndexleri:**
        """)
        
        st.code("""
# Önerilen indeksler
CREATE INDEX idx_marka ON arabalar(marka);
CREATE INDEX idx_model ON arabalar(model);
CREATE INDEX idx_fiyat ON arabalar(fiyat);
CREATE INDEX idx_yil ON arabalar(yil);
CREATE INDEX idx_il ON arabalar(il);
CREATE INDEX idx_aktif ON arabalar(aktif);
        """)

elif page == "Canlı Test":
    st.header("🤖 AI Araç Asistanı")
    
    st.info("🚗 Doğal dilde araç arama yapın! AI asistanım MCP server kullanarak size yardımcı olacak.")
    
    # API anahtarları ve server ayarları
    col1, col2 = st.columns(2)
    
    with col1:
        # .env dosyasından API key'i otomatik yükle
        default_api_key = os.getenv("ANTHROPIC_API_KEY", "")
        anthropic_api_key = st.text_input("🔑 Anthropic API Key:", type="password", 
                                        value=default_api_key,
                                        help="API key .env dosyasından otomatik yüklenir")
    
    with col2:
        server_url = st.text_input("🌐 MCP Server URL:", 
                                 value="https://cce0-2a09-bac5-58c6-252d-00-3b4-1f.ngrok-free.app/mcp")
    
    if not anthropic_api_key:
        st.warning("⚠️ Lütfen Anthropic API anahtarınızı girin.")
    else:
        st.markdown("---")
        
        # Chat geçmişi için session state
        if "chat_messages" not in st.session_state:
            st.session_state.chat_messages = [
                {
                    "role": "assistant", 
                    "content": "🚗 Merhaba! Ben araç arama asistanınızım. Size nasıl yardımcı olabilirim?\n\nÖrnek sorular:\n- 'BMW marka, 2020 sonrası araçlar'\n- '100-200 bin TL arası Toyota araçlar'\n- 'İstanbul'da dizel, ekonomik araçlar'\n- 'Aile için uygun SUV araçlar'"
                }
            ]
        
        # Chat arayüzü
        st.subheader("💬 Sohbet")
        
        # Chat geçmişini göster
        for message in st.session_state.chat_messages:
            if message["role"] == "user":
                st.chat_message("user").write(message["content"])
            else:
                st.chat_message("assistant").write(message["content"])
        
        # Kullanıcı girişi
        if prompt := st.chat_input("Araç arama konusunda ne istiyorsunuz?"):
            # Kullanıcı mesajını ekle
            st.session_state.chat_messages.append({"role": "user", "content": prompt})
            st.chat_message("user").write(prompt)
            
            # AI yanıtını oluştur
            with st.chat_message("assistant"):
                with st.spinner("🤔 Düşünüyorum..."):
                    try:
                        # app.py gibi MCP beta client kullan
                        client = anthropic.Anthropic(api_key=anthropic_api_key)
                        
                        # MCP server config (app.py formatı)
                        mcp_config = {
                            "type": "url", 
                            "url": server_url,
                            "name": "MySQL MCP Server"
                        }
                        
                        # System prompt (app.py'den)
                        system_prompt = """
Sen bir araba galerisi asistanısın. SADECE veritabanındaki araç bilgilerini kullanarak cevap verebilirsin.

🔒 MUTLAK KURALLAR:
1. HER MESAJDA TOOL ÇAĞIRMALISIN - Tool çağırmadan cevap YASAK
2. SADECE tool sonuçlarını kullan - Kendi bilgin YASAK
3. Veritabanında yoksa "bulunamadı" de - Başka öneri YASAK
4. Tool sonucu boşsa genel bilgi verme - YASAK
5. fiyatlar dolar cinsindendir. satış fiyatıdır. cevapta tl kullanma ve satış fiyatı olduğunu belirt.

🔍 ARAMA STRATEJİLERİ:
- Tek marka: marka="toyota" 
- Çoklu marka: marka=["toyota", "ford", "bmw"] (liste formatı)
- "toyota veya ford" derse: marka=["toyota", "ford"]
- "hem toyota hem de ford" derse: marka=["toyota", "ford"]

TOOLS:
- araba_ara (normal arama - tek veya çoklu marka destekler)
- sql_sorgusu_calistir (özel sorgular için)

ARAÇ ÖZELLİKLERİ:
- Marka: ford, toyota, bmw, mercedes, audi vs.
- Model: focus, corolla, x5, e-class vs.
- Yakıt: benzin, dizel, hibrit, elektrik, gaz
- Vites: manuel, otomatik, diğer
- Tip: sedan, hatchback, suv, pickup, coupe vs.
- Durum: yeni, mükemmel, iyi, orta

Her zaman Türkçe cevap ver ve samimi bir dil kullan.
                        """
                        
                        # Chat mesajlarını hazırla
                        messages = [{"role": "user", "content": prompt}]
                        
                        # MCP beta client ile streaming (app.py gibi)
                        stream = client.beta.messages.create(
                            model="claude-3-5-haiku-20241022",
                            system=system_prompt,
                            messages=messages,
                            max_tokens=8192,
                            betas=["mcp-client-2025-04-04"],
                            mcp_servers=[mcp_config],
                            stream=True  # App.py gibi streaming
                        )
                        
                        # Streaming yanıtı topla (app.py formatı)
                        response_text = ""
                        response_placeholder = st.empty()
                        
                        for chunk in stream:
                            if chunk.type == "content_block_delta":
                                if hasattr(chunk.delta, "text") and chunk.delta.text:
                                    response_text += chunk.delta.text
                                    # Real-time güncelleme
                                    response_placeholder.write(f"### 🤖 AI Yanıtı:\n{response_text}")
                        
                        # Final yanıt
                        if not response_text.strip():
                            response_text = "Tool çağrısı yapıldı ancak sonuç görüntülenemedi."
                        
                        # Chat geçmişine ekle
                        st.session_state.chat_messages.append({
                            "role": "assistant", 
                            "content": response_text
                        })
                        
                    except Exception as e:
                        error_message = f"❌ Hata oluştu: {str(e)}"
                        st.error(error_message)
                        st.session_state.chat_messages.append({
                            "role": "assistant", 
                            "content": error_message
                        })

        # Chat geçmişini temizle butonu
        if st.button("🗑️ Sohbeti Temizle"):
            st.session_state.chat_messages = [
                {
                    "role": "assistant", 
                    "content": "🚗 Merhaba! Ben araç arama asistanınızım. Size nasıl yardımcı olabilirim?"
                }
            ]
            st.rerun()



# Alt bilgi
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p>🚗 <strong>Araba Arama MCP Server</strong> - Gelişmiş araç arama sistemi</p>
    <p>Bu proje MCP (Model Context Protocol) kullanarak AI asistanlarına araç veritabanı erişimi sağlar.</p>
</div>
""", unsafe_allow_html=True)
