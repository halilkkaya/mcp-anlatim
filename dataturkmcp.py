import os
import json
import logging
import mysql.connector
from fastmcp import FastMCP
from dotenv import load_dotenv
from tavily import TavilyClient

load_dotenv()
# Logging ayarları - Detaylı SQL logları için
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger("mysql-mcp")

# Ortam değişkenleri
MYSQL_HOST = os.getenv("MYSQL_HOST")
MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

# tavily client oluştur
def get_tavily_client():
    if not TAVILY_API_KEY:
        raise ValueError("TAVILY_API_KEY environment variable bulunamadı!")
    return TavilyClient(api_key=TAVILY_API_KEY)

# MySQL bağlantısı
def get_mysql_connection():
    return mysql.connector.connect(
        host=MYSQL_HOST,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DATABASE
    )

# MCP sunucusu
mcp = FastMCP("Araba Arama MCP",include_tags={"public"},
              exclude_tags={"private"})

@mcp.tool(tags={"public"})
def sql_sorgusu_calistir(sorgu: str) -> str:
    """SQL sorgusunu çalıştır ve sonucu döndür."""
    try:
        # SQL sorgusunu logla
        logger.info(f"🔍 ÖZEL SQL SORGUSU: {sorgu}")
        
        conn = get_mysql_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(sorgu)
        
        # Sorgu türüne bakılmaksızın sonuç almaya çalış
        try:
            sonuc = cursor.fetchall()
            if sonuc:
                logger.info(f"✅ ÖZEL SQL SONUÇ: {len(sonuc)} satır döndürüldü")
                return json.dumps(sonuc, ensure_ascii=False, indent=2)
            else:
                # Boş sonuç kümesi
                logger.info("ℹ️  ÖZEL SQL SONUÇ: Boş sonuç kümesi")
                return "Sorgu başarıyla çalıştırıldı ancak sonuç bulunamadı"
        except mysql.connector.errors.InterfaceError:
            # Sorgu sonuç döndürmüyor (INSERT, UPDATE, DELETE vb.)
            conn.commit()
            logger.info(f"✅ ÖZEL SQL SONUÇ: {cursor.rowcount} satır etkilendi")
            return f"{cursor.rowcount} satır etkilendi"
            
    except Exception as e:
        return f"Hata: {str(e)}"
    finally:
        cursor.close()
        conn.close()

@mcp.tool(tags={"public"})
def tablolari_listele() -> str:
    """Veritabanındaki tabloları listele."""
    logger.info("🔧 TOOL ÇAĞRISI: tablolari_listele")
    try:
        conn = get_mysql_connection()
        cursor = conn.cursor()
        cursor.execute("SHOW TABLES")
        tablolar = [row[0] for row in cursor.fetchall()]
        return json.dumps(tablolar, ensure_ascii=False)
    except Exception as e:
        return f"Hata: {str(e)}"
    finally:
        cursor.close()
        conn.close()

@mcp.tool(tags={"public"})
def tablo_yapisi_goster(tablo_adi: str) -> str:
    """Tablonun yapısını göster."""
    logger.info(f"🔧 TOOL ÇAĞRISI: tablo_yapisi_goster - tablo_adi={tablo_adi}")
    try:
        conn = get_mysql_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(f"DESCRIBE {tablo_adi}")
        yapı = cursor.fetchall()
        return json.dumps(yapı, ensure_ascii=False, indent=2)
    except Exception as e:
        return f"Hata: {str(e)}"
    finally:
        cursor.close()
        conn.close()

@mcp.tool(tags={"public"})
def araba_ara(
    marka = None,  # str veya list kabul eder
    model: str = None,
    min_fiyat: int = None,
    max_fiyat: int = None,
    min_yil: int = None,
    max_yil: int = None,
    min_km: int = None,
    max_km: int = None,
    il: str = None,
    yakit: str = None,
    vites: str = None,
    durum: str = None,
    tip: str = None,
    renk: str = None,
    ozel_arama: str = None,
    siralama: str = "fiyat_artan",
    limit: int = 5,
    detayli: bool = False,
    benzer_araclar: bool = False,
    istatistik: bool = False
) -> str:
    """
    Gelişmiş araba arama tool'u
    
    Parametreler:
    - marka: Araç markası (örn: "ford", "toyota") veya çoklu marka ["ford", "toyota", "bmw"]
    - model: Model adı (örn: focus, corolla)
    - min_fiyat/max_fiyat: Fiyat aralığı
    - min_yil/max_yil: Yıl aralığı (1988-2023)
    - min_km/max_km: Kilometre aralığı
    - il: İl adı
    - yakit: Yakıt tipi (gaz, benzin, dizel, hibrit, elektrik)
    - vites: Vites tipi (manuel, otomatik, diğer)
    - durum: Araç durumu (yeni, mükemmel, iyi, orta)
    - tip: Araç tipi (sedan, hatchback, SUV, pickup, truck, van, coupe, convertible, wagon, offroad, bus)
    - renk: Araç rengi (beyaz, siyah, gri, kırmızı, mavi, yeşil vs.)
    - ozel_arama: Özel arama terimleri (ekonomik, lüks, aile, spor, yakıt_cimrisi vs.)
    - siralama: Sıralama tipi (fiyat_artan, fiyat_azalan, yil_yeni, yil_eski, km_az, km_cok)
    - limit: Gösterilecek sonuç sayısı
    - detayli: True ise daha detaylı bilgi gösterir
    - benzer_araclar: True ise benzer araçları önerir
    - istatistik: True ise istatistiksel bilgileri gösterir
    """
    
    # Tool çağrısını logla
    logger.info(f"🔧 TOOL ÇAĞRISI: araba_ara")
    logger.info(f"📝 GİRDİ PARAMETRELERİ: marka={marka}, model={model}, min_fiyat={min_fiyat}, max_fiyat={max_fiyat}, il={il}, yakit={yakit}, limit={limit}")
    
    try:
        conn = get_mysql_connection()
        # MySQL bağlantısından cursor oluşturuyoruz - SQL sorgularını çalıştırmak için gerekli
        cursor = conn.cursor()
        
        # Ana sorgu oluşturma
        query = "SELECT * FROM arabalar WHERE aktif = 1"
        params = []
        
        # Marka parametresi string veya liste olabilir
        if marka:
            if isinstance(marka, str):
                # String ise normal arama
                # JSON string formatında gelirse parse et
                if marka.startswith('[') and marka.endswith(']'):
                    try:
                        import json
                        marka = json.loads(marka.replace('\\', ''))
                    except:
                        # Parse edilemezse string olarak kullan
                        pass
                
                if isinstance(marka, str):
                    query += " AND LOWER(marka) = LOWER(%s)"
                    params.append(marka)
                else:
                    # Liste parse edilmişse OR kondisyonu ekle
                    marka_conditions = []
                    for m in marka:
                        marka_conditions.append("LOWER(marka) = LOWER(%s)")
                        params.append(str(m).strip())
                    query += f" AND ({' OR '.join(marka_conditions)})"
            elif isinstance(marka, list):
                # Liste ise OR kondisyonu
                marka_conditions = []
                for m in marka:
                    marka_conditions.append("LOWER(marka) = LOWER(%s)")
                    params.append(str(m).strip())
                query += f" AND ({' OR '.join(marka_conditions)})"
        
        if model:
            query += " AND LOWER(model) LIKE LOWER(%s)"
            params.append(f"%{model}%")
        
        if min_fiyat:
            query += " AND fiyat >= %s AND fiyat > 0"  # 0 fiyatlı araçları hariç tut
            params.append(min_fiyat)
        
        if max_fiyat:
            query += " AND fiyat <= %s"
            params.append(max_fiyat)
        
        if min_yil:
            query += " AND yil >= %s"
            params.append(min_yil)
        
        if max_yil:
            query += " AND yil <= %s"
            params.append(max_yil)
        
        if min_km:
            query += " AND km >= %s"
            params.append(min_km)
        
        if max_km:
            query += " AND km <= %s"
            params.append(max_km)
        
        if il:
            query += " AND LOWER(il) = LOWER(%s)"
            params.append(il)
        
        if yakit:
            query += " AND LOWER(yakit) = LOWER(%s)"
            params.append(yakit)
        
        if vites:
            query += " AND LOWER(vites) = LOWER(%s)"
            params.append(vites)
        
        if durum:
            query += " AND LOWER(durum) = LOWER(%s)"
            params.append(durum)
        
        if tip:
            query += " AND LOWER(tip) = LOWER(%s)"
            params.append(tip)
            
        # Yeni: Renk filtresi
        if renk:
            query += " AND LOWER(renk) = LOWER(%s)"
            params.append(renk)
            
        # Yeni: Özel arama terimleri
        if ozel_arama:
            ozel_arama = ozel_arama.lower()
            if ozel_arama == "ekonomik":
                query += " AND ((yakit = 'dizel' OR yakit = 'hibrit') AND fiyat <= (SELECT AVG(fiyat) FROM arabalar))"
            elif ozel_arama == "lüks":
                query += " AND fiyat >= (SELECT AVG(fiyat)*1.5 FROM arabalar) AND durum IN ('yeni', 'mükemmel')"
            elif ozel_arama == "aile":
                query += " AND tip IN ('sedan', 'SUV', 'wagon') AND durum IN ('yeni', 'mükemmel', 'iyi')"
            elif ozel_arama == "spor":
                query += " AND tip IN ('coupe', 'convertible') AND yil >= 2015"
            elif ozel_arama == "yakıt_cimrisi":
                query += " AND yakit IN ('hibrit', 'elektrik', 'dizel')"

        # Sıralama
        if siralama == "fiyat_artan":
            query += " ORDER BY fiyat ASC"
        elif siralama == "fiyat_azalan":
            query += " ORDER BY fiyat DESC"
        elif siralama == "yil_yeni":
            query += " ORDER BY yil DESC"
        elif siralama == "yil_eski":
            query += " ORDER BY yil ASC"
        elif siralama == "km_az":
            query += " ORDER BY km ASC"
        elif siralama == "km_cok":
            query += " ORDER BY km DESC"
        
        # Limit uygula
        query += f" LIMIT {limit}"
        
        # SQL sorgusunu logla
        logger.info(f"🔍 SQL SORGUSU: {query}")
        logger.info(f"📋 PARAMETRELER: {params}")
        
        # Sorguyu çalıştır
        cursor.execute(query, params)
        results = cursor.fetchall()
        
        # Sonuç sayısını logla
        logger.info(f"✅ SONUÇ: {len(results)} adet araç bulundu")
        
        # Sonuçları formatla
        output = f"🔍 Filtrelenmiş araçlar içinden {len(results)} sonuç bulundu (ilk {min(len(results), limit)} gösteriliyor):\n\n"
        
        # Yeni: İstatistiksel bilgiler
        if istatistik:
            # Ortalama değerler için sorgu
            stats_query = """
            SELECT 
                ROUND(AVG(fiyat)) as ort_fiyat,
                ROUND(AVG(km)) as ort_km,
                ROUND(AVG(yil)) as ort_yil,
                COUNT(*) as toplam_arac
            FROM arabalar 
            WHERE aktif = 1
            """
            
            stats_params = []
            if marka:
                stats_query += " AND LOWER(marka) = LOWER(%s)"
                stats_params.append(marka)
            if model:
                stats_query += " AND LOWER(model) LIKE LOWER(%s)"
                stats_params.append(f"%{model}%")
                
            cursor.execute(stats_query, stats_params)
            stats = cursor.fetchone()
            
            if stats and stats[0] is not None:
                output += f"""
                📊 İstatistiksel Bilgiler:
                • Ortalama Fiyat: {int(stats[0]):,} TL
                • Ortalama Kilometre: {int(stats[1]):,} km
                • Ortalama Yıl: {int(stats[2])}
                • Toplam İlan Sayısı: {stats[3]}

                """

        # Ana araç listesi
        for row in results:
            # None değerleri kontrol et ve güvenli string dönüşümü yap
            marka_str = str(row[4]).lower() if row[4] is not None else "belirtilmemiş"
            model_str = str(row[5]).lower() if row[5] is not None else "belirtilmemiş"
            yil_str = str(row[3]) if row[3] is not None else "belirtilmemiş"
            km_str = f"{int(row[9]):,}" if row[9] is not None else "belirtilmemiş"
            fiyat_str = f"{int(row[2]):,}" if row[2] is not None else "belirtilmemiş"
            il_str = str(row[1]).lower() if row[1] is not None else "belirtilmemiş"
            
            output += f"\n• {marka_str} {model_str} - {yil_str} model - {km_str} km - {fiyat_str} TL - {il_str}\n"
            
            # Temel özellikler
            ozellikler = []
            if row[7] is not None: ozellikler.append(str(row[7]).lower())  # yakit
            if row[11] is not None: ozellikler.append(str(row[11]).lower())  # vites
            if row[6] is not None: ozellikler.append(str(row[6]).lower())  # durum
            if row[13] is not None: ozellikler.append(str(row[13]).lower())  # tip
            
            # Ekstra özellikler
            ekstralar = []
            if row[10] is not None: ekstralar.append(f"Statü: {str(row[10]).lower()}")  # statu
            if row[12] is not None: ekstralar.append(f"Çekiş: {str(row[12]).lower()}")  # cekis
            if row[8] is not None: ekstralar.append(f"Motor: {str(row[8]).lower()}")  # silindir
            
            if ozellikler or ekstralar:
                output += "  " + ", ".join(ozellikler + ekstralar) + "\n"
                
            if detayli and row[15] is not None:  # aciklama varsa
                output += f"  📝 {str(row[15])}\n"
                
        # Yeni: Benzer araçlar önerisi
        if benzer_araclar and (marka or model) and len(results) > 0:
            try:
                similar_query = """
                SELECT * FROM arabalar 
                WHERE aktif = 1 
                AND (
                    (LOWER(marka) = LOWER(%s) AND ABS(yil - %s) <= 2)
                    OR 
                    (LOWER(model) LIKE LOWER(%s) AND ABS(yil - %s) <= 2)
                )
                AND id NOT IN ({})
                ORDER BY RAND()
                LIMIT 3
                """.format(','.join(['%s'] * len(results)))
                
                similar_params = []
                first_result_year = results[0][3] if results[0][3] is not None else 2020
                
                if marka:
                    similar_params.extend([marka, first_result_year])
                if model:
                    similar_params.extend([f"%{model}%", first_result_year])
                similar_params.extend([r[0] for r in results])  # mevcut sonuçların ID'leri
                
                cursor.execute(similar_query, similar_params)
                similar_results = cursor.fetchall()
                
                if similar_results:
                    output += "\n🔍 Benzer Araçlar:\n"
                    for row in similar_results:
                        marka_str = str(row[4]).lower() if row[4] is not None else "belirtilmemiş"
                        model_str = str(row[5]).lower() if row[5] is not None else "belirtilmemiş"
                        yil_str = str(row[3]) if row[3] is not None else "belirtilmemiş"
                        km_str = f"{int(row[9]):,}" if row[9] is not None else "belirtilmemiş"
                        fiyat_str = f"{int(row[2]):,}" if row[2] is not None else "belirtilmemiş"
                        output += f"• {marka_str} {model_str} - {yil_str} model - {km_str} km - {fiyat_str} TL\n"
            except Exception as e:
                output += f"\n⚠️ Benzer araçlar aranırken hata oluştu: {str(e)}\n"
        
        return output
        
    except Exception as e:
        return f"Hata oluştu: {str(e)}"
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    # MySQL bağlantısını test et    
    mcp.run(transport="streamable-http",host="0.0.0.0",port=8000)
    #mcp.run()