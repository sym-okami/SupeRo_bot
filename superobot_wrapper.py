import superobot as sr
import json

if __name__ == "__main__":
    auth = None
    with open("./bot_auth.json") as f:
        auth = json.load(f)

    superobot = sr.TwitchChatBot(auth["user"], auth["oauth"])
    superobot.join("#sym_okami")
    # superobot.join("#seal1234")
    superobot.listen()
