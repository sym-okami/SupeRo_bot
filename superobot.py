import re
import random
import sys
import time
sys.path.append('../GetterCore')
import gettercore

class SupeRo_Bot(gettercore.GetterCore):
    def __init__(self, user, oauth):
        gettercore.GetterCore.__init__(self, user, oauth)
        self.megu_timer = time.time() - 50

    def on_mention(self, user_message, username, channel):
        if "meguHands" in user_message or "seal12MH" in user_message:
            self.send_msg("@{} meguHands".format(username), channel)
        else:
            self.send_msg("@{} :)".format(username), channel)

    def run_command(self, user_message, username, channel):
        # list of commands
        commands = ["!command", "!dice {x}d{y} + {z}", "!roll {n}",
        "!8ball {question}", "!birdgirl", "!bttv", "!% {question}"]
        command = user_message[1:] # remove !
        
        if command.startswith("commands"):
            self.send_msg("@{} Here are my functionalities: {}".format(
                username, str(commands)[1:-1]
            ), channel)
        
        elif command.startswith("dice"):
            pattern = r"(\d+)\s*d\s*(\d+)\s*\+?\s*(\d+)?"
            match = re.search(pattern, command[5:])
            if match:
                numdice = match.group(1)
                die = match.group(2)
                modifier = match.group(3)
                total = int(numdice) * random.randint(1, int(die))
                if modifier != None:
                    total += int(modifier)
                self.send_msg("@{} You roll: {}".format(username, total), 
                channel)
            else:
                self.send_msg("@{} Please use this format: !dice 2d10 + 3", 
                channel)

        elif command.startswith("roll"):
            pattern = r"roll\s+(\d+)"
            match = re.search(pattern, command)
            if match:
                n = int(match.group(1))
                self.send_msg("@{} {}".format(username, random.randint(1, n)),
                channel)
            else:
                self.send_msg("@{} Please use this format: !roll 10", channel)

        elif command.startswith("8ball"):
            results = ['All signs point to yes...', 'Yes!', 
            'My sources say nope.', 'You may rely on it.', 
            'Concentrate and ask again...', 'Outlook not so good...', 
            'It is decidedly so!', 'Better not tell you.', 'Very doubtful.', 
            'Yes - Definitely!', 'It is certain!', 'Most likely.', 
            'Ask again later.', 'No!', 'Outlook good.', 'Don\'t count on it.']
            self.send_msg("@{} :8ball: {}".format(username, 
            random.choice(results)), channel)

        elif command.startswith("birdgirl"):
            bg = ["https://imgur.com/SesEqKJ", " https://imgur.com/UDvEAyA", 
            "https://imgur.com/nkRwkQh", "https://imgur.com/4D8u2LD"]
            self.send_msg(random.choice(bg), channel)

        elif command.startswith("bttv"):
            emotes = self.fetch_url(
                "https://twitch.center/customapi/bttvemotes?channel={}".
                format(channel[1:]))
            self.send_msg(emotes, channel)

        elif command.startswith("%"):
            self.send_msg("@{} {}%".format(username, random.randint(0, 100)),
            channel)

    def handle_message(self, user_message, username, channel):
        if "anime" in user_message.lower():
            self.send_msg("@{} the proper term is Japanimation.".
            format(username), channel)
        elif "meguHands" in user_message or "seal12MH" in user_message:
            checktime = time.time()
            if checktime - self.megu_timer > 15:
                self.send_msg("meguHands", channel)
                self.megu_timer = checktime