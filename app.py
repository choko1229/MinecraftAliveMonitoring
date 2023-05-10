import socket
import time
import discord
import asyncio
from discord.ext import commands

# Unixタイムを取得する
def get_unix_time():
    unix_time = int(time.time())
    return unix_time

unix = get_unix_time()
print(unix)


# Discordのトークンを設定
DISCORD_TOKEN = "BOTTOKEN"

# 監視するホスト名またはIPアドレスとポート番号
host = "192.168.3.100"
port = 8250

# Discord Botを作成
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print("ログインしました")

@bot.event
async def on_disconnect():
    print("切断しました")

# 監視対象のポートの状態を監視するタスク
async def port_check_task():
    last_state = None

    while True:
        state = await check_port_state()
        if state != last_state:
            last_state = state
            await send_discord_message(state)
        await asyncio.sleep(1)

# ポートの状態をチェックする関数
async def check_port_state():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)

    try:
        sock.connect((host, port))
        return f"<t:{unix}:F> にサーバーが復旧しました。"
    except socket.error:
        return f"<t:{unix}:R> にサーバーがダウンしました。復旧までしばらくお待ち下さい。 @here"
    finally:
        sock.close()

# Discordにメッセージを送信する非同期関数
async def send_discord_message(msg):
    channel = bot.get_channel(channelid)  # DiscordのチャンネルIDを設定してください
    await channel.send(msg)

# ポートの状態を監視
@bot.event
async def on_ready():
    bot.loop.create_task(port_check_task())

# Discord Botを実行
bot.run(DISCORD_TOKEN)
