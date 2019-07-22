import socket
import re
import random
import time

class TwitchChatBot:
    def __init__(self, user, oauth, channel):
        self.user = user
        self.oauth = oauth
        self.channel = channel
        self.socket = socket.socket()
        self.connect()
        self.last_timer = time.time()

    def connect(self):
        self.socket.connect(('irc.chat.twitch.tv', 6667))
        self.send_data('PASS ' + self.oauth)
        self.send_data('NICK ' + self.user)
        self.send_data('JOIN ' + self.channel)

    def join(self, channel):
        self.send_data('JOIN ' + channel)

    def listen(self):
        while True:
            try:
                inp = self.socket.recv(2048).decode('utf-8', 'ignore')
                if len(inp) > 1:
                    print(repr(inp))
                    self.parse_message(inp)
            except Exception as e:
                print("Something went wrong")
                print(e)

    def parse_message(self, message):
        if message.strip() == "PING :tmi.twitch.tv":
            self.pong()
        elif "PRIVMSG" in message:
            chunks = message[1:].split(":")
            head = chunks[0]
            tail = chunks[1]
            
            username = head.split("!")[0]
            channel = head.split(" ")[2]
            user_message = tail.strip()
            
            # do the things here
            if "supero_bot" in user_message.lower():
                self.at_msg(username, ":)", channel)
            elif "anime" in user_message.lower() and channel == "#sym_okami":
                self.send_msg("/timeout " + username + " 60", channel)
                self.at_msg(username, "The proper term is Japanimation.", channel)
            elif ("meguHands" in user_message or "seal12MH" in user_message) and channel == "#seal1234":
                checktime = time.time()
                if checktime - self.last_timer > 60:
                    self.send_msg("meguHands", channel)
                    self.last_timer = checktime
            elif user_message.startswith("!"):
                self.run_command(username, channel, user_message[1:])

    def run_command(self, username, channel, command):
        commands = ["!command", "!dice xdy + z"]
        if command.startswith("commands"):
            self.at_msg(username, "The following commands are available: " +
                        str(commands)[1:-1])
        elif command.startswith("dice"):
            print("IN DICE")
            pattern = r"(\d+)\s*d\s*(\d+)\s*\+?\s*(\d+)?"
            print(command[5:])
            match = re.search(pattern, command[5:])
            if match:
                numdice = match.group(1)
                die = match.group(2)
                modifier = match.group(3)
                total = int(numdice) * random.randint(1, int(die))
                if modifier != None:
                    total += int(modifier)
                self.at_msg(username, "You roll: " + str(total), channel)
            else:
                self.at_msg(username, "Please use the form: !dice xdy + z", channel)

    def pong(self):
        self.send_data("PONG :pingis")

    def send_data(self, message):
        self.socket.send(self.encodeb(message + '\r\n'))
        print("!!! SENT: " + message)

    def at_msg(self, username, message, channel):
        self.send_msg("@" + username + " " + message, channel)

    def send_msg(self, message, channel):
        self.send_data('PRIVMSG ' + channel + ' :' + message)

    def encodeb(self, message):
        return bytes(message, 'utf-8')
