import discord


async def on_ready(self, *, init_channels):
    print(f"[INFO ] {self.user} でログインしました。")
    channels = {}
    channels["vxww50"] = self.get_channel(self.channels_id["vxww50"])

    print(f"[INFO ] 設定されたチャンネルIDの送信権限を検証しています...")

    for code, channel in channels.items():
        try:
            sent_message = await channel.send("これは設定されたチャンネルIDの送信権限を検証するテストメッセージです。")
            await sent_message.delete()

        except discord.errors.Forbidden as e:
            print(
                f"[ERROR] {code} 用に設定されたチャンネルID {self.channels_id[code]} にメッセージを送信できません:\nチャンネルへの送信権限がありません。\n{e}"
            )

        except Exception as e:
            print(
                f"[ERROR] {code} 用に設定されたチャンネルID {self.channels_id[code]} にメッセージを送信できません:\nチャンネルIDが正しいか、送信するサーバーにBOTが参加しているかを確認してください。\n{e}"
            )

    print(f"[INFO ] 設定されたチャンネルIDの送信権限の検証が完了しました。")

    init_channels(channels)
