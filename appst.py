import streamlit as st
import os
from langchain_community.chat_models import ChatOpenAI
from langchain_experimental.sql import SQLDatabaseChain
from langchain.sql_database import SQLDatabase
import mysql.connector
from sqlalchemy import create_engine
from dotenv import load_dotenv
import requests
import json

# .env dosyasındaki environment variable'ları yükle
load_dotenv()

# MySQL bağlantı bilgileri
MYSQL_HOST = os.getenv("MYSQL_HOST")
MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE")

# Tavily API bilgileri
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

# Streamlit sayfa yapılandırması
st.set_page_config(page_title="Araç Asistanı", page_icon="🚗")

# SQLAlchemy engine oluştur
try:
    engine = create_engine(f"mysql+mysqlconnector://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DATABASE}")
except Exception as e:
    st.error(f"Veritabanı bağlantısı oluşturulurken hata: {e}")
    st.stop()

# LLM modelini başlat
try:
    llm = ChatOpenAI(
        model_name="gpt-3.5-turbo",
        temperature=0.2,
        openai_api_key=os.getenv("OPENAI_API_KEY")
    )
except Exception as e:
    st.error(f"LLM başlatılırken hata oluştu: {e}")
    st.stop()

# SQLDatabase nesnesini oluştur
try:
    db = SQLDatabase(engine)
except Exception as e:
    st.error(f"SQLDatabase başlatılırken hata oluştu: {e}")
    st.stop()

# Tavily arama fonksiyonu
def tavily_search(query):
    """Tavily API kullanarak web araması yapar"""
    try:
        url = "https://api.tavily.com/search"
        payload = {
            "api_key": TAVILY_API_KEY,
            "query": query,
            "search_depth": "basic",
            "include_answer": True,
            "include_raw_content": False,
            "max_results": 3,
            "include_domains": [],
            "exclude_domains": []
        }
        
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()
        
        return response.json()
    except Exception as e:
        st.error(f"Tavily arama hatası: {e}")
        return None

# Sorgu türünü belirle
def classify_query(query):
    """Sorgunun araç arama mı yoksa genel araç bilgisi mi olduğunu belirler"""
    # Araç arama anahtar kelimeleri
    search_keywords = [
        "arıyorum", "bul", "ara", "öneri", "öner", "seç", "hangi araç", "nasıl araç",
        "fiyat aralığı", "bütçe", "satın al", "almak istiyorum", "kriterler",
        "specifications", "spec", "özellikleri neler", "hangi model"
    ]
    
    # Genel bilgi anahtar kelimeleri
    info_keywords = [
        "nedir", "nasıl", "ne demek", "açıkla", "anlat", "bilgi ver", "öğren",
        "tarihçe", "hikaye", "gelişim", "teknoloji", "motor", "yakıt tüketimi hesaplama",
        "bakım", "servis", "sigorta", "vergi", "mtv", "trafik", "ehliyet", "sürüş",
        "ne zaman", "kim", "nerede", "hangi şirket", "marka", "üretici"
    ]
    
    query_lower = query.lower()
    
    # Önce araç arama kontrolü
    for keyword in search_keywords:
        if keyword in query_lower:
            return "database_search"
    
    # Sonra genel bilgi kontrolü
    for keyword in info_keywords:
        if keyword in query_lower:
            return "web_search"
    
    # Varsayılan olarak veritabanı araması
    return "database_search"

# Araç asistanı için özel prompt şablonu
PROMPT_TEMPLATE = """
Sen profesyonel bir araç danışmanısın. Veritabanından gelen bilgileri kullanarak müşteriye uygun araç önerileri sunacaksın.
Cevapların her zaman Türkçe olacak. Müşteri herhangi bir profil belirtmediyse elindeki sonuçları normal olarak ilet.

Kullanıcının belirttiği profiline göre özelleştirilmiş öneriler sun:
- Aile için: Geniş bagaj, güvenlik özellikleri, ekonomik yakıt tüketimi
- Şehir içi kullanım için: Kompakt boyut, park kolaylığı, düşük yakıt tüketimi
- Lüks segment için: Premium özellikler, yüksek performans, konfor
- İş için: Güvenilirlik, dayanıklılık, yakıt ekonomisi
- Spor/performans için: Yüksek beygir gücü, sportif süspansiyon, hızlanma

Veritabanından gelen ham veriyi şu şekilde formatla:
1. Önce müşterinin isteğini ve profilini özetle
2. Bulunan araçları müşteri profiline uygun şekilde detaylı anlat
3. Her araç için müşterinin ihtiyaçlarına yönelik öne çıkan özellikleri vurgula
4. Son olarak müşterinin profiline en uygun seçenekleri belirterek genel bir değerlendirme yap

Veritabanından gelen veri: {query_result}
"""

# Web bilgisi için prompt şablonu
WEB_INFO_TEMPLATE = """
Sen profesyonel bir araç uzmanısın. Aşağıdaki web arama sonuçlarını kullanarak kullanıcının araç ile ilgili sorusunu detaylı şekilde yanıtla.
Cevabın her zaman Türkçe olacak ve güncel, doğru bilgiler içerecek.

Kullanıcının sorusu: {user_query}

Web arama sonuçları: {web_results}

Yanıtını şu şekilde yapılandır:
1. Soruya doğrudan ve net yanıt ver
2. Detaylı açıklamalar ekle
3. Güncel bilgiler ve gelişmeler varsa belirt
4. Kullanıcıya faydalı ipuçları sun

ÖNEMLİ: Sadece araç ile ilgili konularda yanıt ver. Başka konularda soru gelirse "Ben bir araç uzmanıyım ve sadece araç konularında size yardımcı olabilirim." şeklinde yanıtla.
"""

# LangChain SQLDatabaseChain'i oluştur
try:
    chain = SQLDatabaseChain.from_llm(llm, db, verbose=True)
except Exception as e:
    st.error(f"SQLDatabaseChain başlatılırken hata oluştu: {e}")
    st.stop()

# Streamlit arayüzü
st.title("🚗 Akıllı Araç Danışmanı")
st.caption("Size en uygun aracı bulmama yardım edin! Nasıl bir araç arıyorsunuz?")

# Kullanıcı girişi için form
with st.form(key="query_form"):
    user_query = st.text_area("Arama kriterlerinizi girin (örneğin: 'Dizel yakıtlı, otomatik vites bir SUV arıyorum') veya araç hakkında soru sorun", height=100)
    submit_button = st.form_submit_button(label="🔍 Sorgula")

# Eğer kullanıcı bir sorgu gönderdiyse
if submit_button and user_query:
    query_type = classify_query(user_query)
    
    if query_type == "database_search":
        st.info(f"Veritabanımızda araç arıyorum: '{user_query}'")
        with st.spinner("Size en uygun seçenekleri arıyorum..."):
            try:
                # Veritabanından SQLDatabaseChain ile sonucu al
                db_result = chain.run(user_query)

                # Sonucu özel prompt şablonuna yerleştir
                final_prompt_for_llm = PROMPT_TEMPLATE.format(query_result=db_result)
                
                # Formatlanmış prompt'u LLM'e gönder
                final_answer = llm.predict(final_prompt_for_llm)
                
                st.success("İşte size özel önerilerim:")
                st.markdown(final_answer)

            except Exception as e:
                st.error(f"İsteğiniz işlenirken bir sorun oluştu: {e}")
                st.warning("Lütfen sorunuzu farklı bir şekilde ifade etmeyi deneyin veya daha sonra tekrar deneyin.")
    
    else:  # web_search
        st.info(f"Web üzerinden araç bilgisi arıyorum: '{user_query}'")
        with st.spinner("Güncel bilgileri getiriyorum..."):
            try:
                # Tavily ile web araması yap
                web_results = tavily_search(user_query + " araç otomobil")
                
                if web_results and web_results.get('results'):
                    # Web sonuçlarını formatla
                    formatted_results = ""
                    for result in web_results['results'][:3]:
                        formatted_results += f"Başlık: {result.get('title', '')}\n"
                        formatted_results += f"İçerik: {result.get('content', '')}\n"
                        formatted_results += f"Kaynak: {result.get('url', '')}\n\n"
                    
                    # Web bilgisini LLM'e gönder
                    web_prompt = WEB_INFO_TEMPLATE.format(
                        user_query=user_query,
                        web_results=formatted_results
                    )
                    
                    final_answer = llm.predict(web_prompt)
                    
                    st.success("İşte güncel bilgiler:")
                    st.markdown(final_answer)
                    
                    # Kaynakları göster
                    with st.expander("📚 Kaynaklar"):
                        for i, result in enumerate(web_results['results'][:3], 1):
                            st.markdown(f"**{i}.** [{result.get('title', 'Başlık yok')}]({result.get('url', '#')})")
                
                else:
                    st.warning("Üzgünüm, bu konuda güncel bilgi bulamadım. Lütfen sorunuzu farklı şekilde ifade etmeyi deneyin.")
                    
            except Exception as e:
                st.error(f"Web araması sırasında bir sorun oluştu: {e}")
                st.warning("Lütfen daha sonra tekrar deneyin.")

elif submit_button and not user_query:
    st.warning("Lütfen aramak istediğiniz özellikleri veya sorunuzu girin.")

st.sidebar.header("Nasıl Kullanılır?")
st.sidebar.info(
    "**Araç Arama (Veritabanı):**\n"
    "• 'Dizel SUV arıyorum'\n"
    "• 'Otomatik vites araç öner'\n"
    "• 'Aile için ekonomik araç bul'\n\n"
    "**Genel Bilgi (Web):**\n"
    "• 'Hibrit araç nedir?'\n"
    "• 'BMW tarihçesi anlat'\n"
    "• 'Yakıt tüketimi nasıl hesaplanır?'\n"
    "• 'Elektrikli araç bakımı nasıl?'"
)
st.sidebar.markdown("---")
st.sidebar.markdown("🔍 **Veritabanı**: Araç arama ve öneri")
st.sidebar.markdown("🌐 **Web**: Güncel araç bilgileri")


# Terminalde çalıştırmak için: streamlit run app.py
