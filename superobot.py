import socket
import re
import random
import time
import colorama
from colorama import Fore, Style

# Always initialize colorama
colorama.init()

class TwitchChatBot:
    def __init__(self, user, oauth):
        self.user = user
        self.oauth = oauth
        self.workers = {}
        self.last_timer = time.time()

    def join(self, channel):
        self.workers[channel] = ChatWorker(self.user, self.oauth, channel,
        verbose=True)
        self.workers[channel].send_data('JOIN ' + channel)

    def listen(self):
        while True:
            for channel in self.workers:
                worker = self.workers[channel]
                try:
                    data = worker.recv()
                    if data:
                        print(f'{Fore.GREEN}SENT: ' + data.strip() + 
                        f'{Style.RESET_ALL}')
                        self.parse_message(data)
                except Exception as e:
                    print(f'{Fore.RED} Something went wrong: ' + str(e) + 
                    f'{Style.RESET_ALL}')

    def parse_message(self, message):
        if "PRIVMSG" in message:
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
            elif "meguHands" in user_message or "seal12MH" in user_message:
                checktime = time.time()
                if checktime - self.last_timer > 15:
                    self.send_msg("meguHands", channel)
                    self.last_timer = checktime
            elif user_message.startswith("!"):
                self.run_command(username, channel, user_message[1:])

    def run_command(self, username, channel, command):
        commands = ["!command", "!dice xdy + z"]
        if command.startswith("commands"):
            self.at_msg(username, "The following commands are available: " +
                        str(commands)[1:-1], channel)
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
        elif command == "spam":
            self.send_msg("test", channel)
            self.send_msg("test2", channel)
            self.send_msg("test3", channel)
            self.send_msg("test4", channel)
            self.send_msg("test5", channel)

    def at_msg(self, username, message, channel):
        self.send_msg("@" + username + " " + message, channel)

    def send_msg(self, message, channel):
        self.workers[channel].send_data('PRIVMSG ' + channel + ' :' + message)

    def encodeb(self, message):
        return bytes(message, 'utf-8')

class ChatWorker:
    def __init__(self, user, oauth, channel, verbose=False):
        self.user = user
        self.oauth = oauth
        self.channel = channel
        self.verbose = verbose
        self.socket = socket.socket()
        self.connect()

    def connect(self):
        self.socket.connect(('irc.chat.twitch.tv', 6667))
        self.send_data('PASS ' + self.oauth, silent=True)
        self.send_data('NICK ' + self.user, silent=True)
        self.send_data('JOIN ' + self.channel, silent=True)

    def recv(self):
        data = self.socket.recv(2048).decode('utf-8', 'ignore')
        if data.strip() == "PING :tmi.twitch.tv":
            self.pong()
            return None
        else:
            return data

    def pong(self):
        self.send_data("PONG :tmi.twitch.tv", silent=True)

    def send_data(self, message, silent=False):
        self.socket.send(self.encodeb(message + '\r\n'))
        if not silent and self.verbose:
            print(f'{Fore.YELLOW}SENT: ' + message + f'{Style.RESET_ALL}')

    def encodeb(self, message):
        return bytes(message, 'utf-8')