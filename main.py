# ========================================================
# PYTHON 3.14 CRITICAL AUDIOOP PATCH (MUST BE FIRST)
# ========================================================
import sys
import types
sys.modules['audioop'] = types.ModuleType('audioop')
# ========================================================

import discord
import asyncio
import os
from dotenv import load_dotenv

# .env dosyasındaki gizli verileri çeker
load_dotenv()

class MyClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Bilgiler dışarıdaki .env dosyasından çekiliyor (GitHub için güvenli)
        self.token = os.getenv('DISCORD_TOKEN')
        self.channel_id = os.getenv('VOICE_CHANNEL_ID')
        self.server_id = os.getenv('SERVER_ID')
        
        # Profilde dönecek emojili durumlar
        self.durumlar = [
            "👑 Self Bot By Efe",
            "🌐 https://discord.gg",
            "⚡ Ez Self"
        ]

    async def on_ready(self):
        print(f"giris temiz: {self.user.name}")
        await asyncio.sleep(2)
        await self.odaya_baglan()
        
        # Durum değiştirici döngüyü arka planda başlatır
        asyncio.create_task(self.durum_dongusu())

    async def odaya_baglan(self):
        if not self.server_id or not self.channel_id:
            print("Hata: Sunucu veya Kanal ID bulunamadi (.env dosyasini kontrol et)")
            return
        try:
            # Belirlenen ses kanalına ham sinyal göndererek giriş yapar
            await self.ws.send_as_json({
                "op": 4,
                "d": {
                    "guild_id": str(self.server_id),
                    "channel_id": str(self.channel_id),
                    "self_mute": True,
                    "self_deaf": True,
                    "self_video": False
                }
            })
            print("odaya gecis emri sunucuya iletildi.")
        except Exception as e:
            print(f"Baglanti hatasi olustu: {e}")

    async def durum_dongusu(self):
        while True:
            for yazi in self.durumlar:
                try:
                    await self.change_presence(activity=discord.CustomActivity(name=yazi))
                    await asyncio.sleep(5) # 5 saniyede bir değiştirir
                except Exception:
                    await asyncio.sleep(5)

    async def on_socket_response(self, msg):
        # Sesten düşme veya atılma durumunda otomatik geri bağlanma
        if msg.get('t') == 'VOICE_STATE_UPDATE':
            d = msg.get('d', {})
            if d.get('user_id') == str(self.user.id):
                if d.get('channel_id') is None:
                    print("sesten dusme algilandi, 3sn sonra geri giriliyor...")
                    await asyncio.sleep(3)
                    await self.odaya_baglan()

bot = MyClient()
bot.run(bot.token)