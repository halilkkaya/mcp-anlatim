
import os
import asyncio
import anthropic
import json
import time
import hashlib
from dotenv import load_dotenv

load_dotenv()

claude = anthropic.AsyncAnthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

MCP = {
    "type": "url",
    "url": os.getenv("MCP_URL"),
    "name": "MySQL MCP Server",
    "authorization_token": os.getenv("MCP_TOKEN") or None,
    }

SYSTEM_PROMPT = """
Sen bir araba galerisi asistanısın. SADECE veritabanındaki araç bilgilerini kullanarak cevap verebilirsin.

🔒 MUTLAK KURALLAR:
1. HER MESAJDA TOOL ÇAĞIRMALISIN - Tool çağırmadan cevap YASAK
2. SADECE tool sonuçlarını kullan - Kendi bilgin YASAK
3. Veritabanında yoksa "bulunamadı" de - Başka öneri YASAK
4. Tool sonucu boşsa genel bilgi verme - YASAK

🚫 YASAK DAVRANIŞLAR:
- "Genellikle arabada..." gibi genel bilgi
- "Tavsiye ederim..." gibi öneriler  
- "Piyasada..." gibi genel yorumlar
- Tool çağırmadan direkt cevap
- Kendi araç bilgilerini kullanmak
- Veritabanı dışından bilgi

✅ ZORUNLU DAVRANIŞLAR:
- Her mesajda uygun araç tool'unu çağır  
- SADECE tool sonuçlarını göster
- Tool sonucu yoksa: "Veritabanımızda bulunamadı"
- Toollara tam ve doğru parametreleri ver
- Kullanıcı ingilizce klavyeyle yazsa bile marka model bilgilerinde türkçe alfabe kullan!

TOOLS:
- araba_ara (normal arama)
- sql_sorgusu_calistir (özel sorgular için)
- tablolari_listele (veritabanı yapısı)
- tablo_yapisi_goster (tablo detayları)

ARAÇ ÖZELLİKLERİ:
- Marka: ford, toyota, bmw, mercedes, audi vs.
- Model: focus, corolla, x5, e-class vs.
- Yakıt: benzin, dizel, hibrit, elektrik, gaz
- Vites: manuel, otomatik, diğer
- Tip: sedan, hatchback, suv, pickup, coupe vs.
- Durum: yeni, mükemmel, iyi, orta

CEVAP FORMATI:
- Tool sonuçlarını olduğu gibi aktar
- Sadece tool çıktısını kullan
- Veritabanından gelen bilgileri net şekilde göster

EĞER VERİTABANINDA YOKSA:
"Aramanıza uygun araç veritabanımızda bulunamadı. Farklı kriterler deneyebilirsiniz."

EĞER ARAÇ DIŞI SORU:
"Ben sadece araç konularında yardımcı olabilirim."
"""

async def ai_chat(messages, system_prompt=None):
    """Araç asistanıyla iletişim kurmak için bir asenkron fonksiyon"""
    try:
        # System prompt'u kullan veya default'u al
        prompt_to_use = system_prompt if system_prompt else SYSTEM_PROMPT
        
        stream = await claude.beta.messages.create(
            model="claude-3-5-haiku-20241022",
            system=prompt_to_use,
            messages=messages,
            max_tokens=8192,
            betas=["mcp-client-2025-04-04"],
            mcp_servers=[MCP],
            stream=True
        )

        content = ""
        print("Araç Asistanı: ",end="",flush=True)  

        async for chunk in stream:
            if chunk.type == "content_block_delta":
                delta = chunk.delta.text if hasattr(chunk.delta,"text") else ""
                if delta:
                    print(delta, end="",flush=True)
                content += delta
        print("\n")
        return content
    except Exception as e:
        print(f"Hata: {e}")
        return "üzgünüm, devam edemiyorum. lütfen daha sonra tekrar deneyiniz."
    
def print_welcome():
    """Hoşgeldin mesajı"""
    print("🚗" + "="*60 + "🚗")
    print("    ARAÇ GALERİSİ ASİSTANI + MCP")
    print("🚗" + "="*60 + "🚗")
    print("💡 Örnekler:")
    print("   • 'Ford Focus var mı?'")
    print("   • 'En ucuz 5 arabayı göster'")
    print("   • '50000 TL altı araçları listele'")
    print("   • '/çıkış' - uygulamadan çık")
    print("-" * 62)

async def main():
    print_welcome()
    
    messages = []
    
    # İlk hoşgeldin mesajı
    print("🚗 Araç Asistanı: Merhaba! Hangi aracı arıyorsunuz? 🚙")
    print("💡 Örnek: 'Toyota Corolla arıyorum' veya 'Benzinli araçları göster'")
    print("-" * 62)
    
    while True:
        try:
            user_input = input("Kullanıcı: ").strip()
            if user_input.lower() == "/çıkış":
                print("Uygulamadan çıkılıyor...")
                break
            if not user_input:
                continue
            messages.append({"role": "user", "content": user_input})
            answer = await ai_chat(messages, system_prompt=SYSTEM_PROMPT)
            messages.append({"role": "assistant", "content": answer})
        except (EOFError, KeyboardInterrupt):
            print("\nUygulamadan çıkılıyor...")
            break
        except Exception as e:
            print(f"Hata: {e}")

if __name__ == "__main__":
    asyncio.run(main())

