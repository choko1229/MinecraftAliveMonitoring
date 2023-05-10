from mcstatus import JavaServer

# MinecraftサーバーのIPアドレスとポート番号を指定
server_ip = "192.168.3.100"
server_port = 8250  # デフォルトのポート番号は25565ですが、サーバーが異なるポートを使用している場合は変更してください

# Minecraftサーバーオブジェクトを作成
server = JavaServer.lookup(f"{server_ip}:{server_port}")

try:
    # サーバーのステータスを取得
    status = server.status()

    # 接続中のプレイヤー数を表示
    print(f"接続中のプレイヤー数: {status.players.online}")

except ConnectionRefusedError:
    print("サーバーに接続できませんでした。")
