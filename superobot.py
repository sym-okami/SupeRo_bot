import socket
import re
import random
import time
import traceback
import colorama
from colorama import Fore, Style

# Always initialize colorama
colorama.init()

### Utility functions go here :)
def parse_tags(tags):
    tag_dict = {}
    for tag_pair in tags.split(";"):
        tag,content = tag_pair.split("=")
        tag_dict[tag] = content
    return tag_dict

def encodeb(message):
    return bytes(message, 'utf-8')

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
                        print(f'{Fore.GREEN}RECV: ' + data.strip() + 
                        f'{Style.RESET_ALL}')
                        self.parse_message(data)
                except Exception:
                    print(f'{Fore.RED}Something went wrong: ' + 
                    traceback.format_exc() + f'{Style.RESET_ALL}')

    def parse_message(self, message):
        if "PRIVMSG" in message:
            chunks = message.split(":")
            # tags = parse_tags(chunks[0])
            head = chunks[1]
            user_message = chunks[2].strip()

            username = head.split("!")[0]
            channel = head.split(" ")[2]
            
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
            self.workers[channel].queue_data('PRIVMSG ' + channel + ' :test')
            self.workers[channel].queue_data('PRIVMSG ' + channel + ' :test2')
            self.workers[channel].queue_data('PRIVMSG ' + channel + ' :test3')
            self.workers[channel].queue_data('PRIVMSG ' + channel + ' :test4')
            self.workers[channel].queue_data('PRIVMSG ' + channel + ' :test5')
            self.workers[channel].send_queued_data()

    def at_msg(self, username, message, channel):
        self.send_msg("@" + username + " " + message, channel)

    def send_msg(self, message, channel):
        self.workers[channel].queue_data('PRIVMSG ' + channel + ' :' + message)
        self.workers[channel].send_queued_data()

class ChatWorker:
    def __init__(self, user, oauth, channel, verbose=False):
        self.user = user
        self.oauth = oauth
        self.channel = channel
        self.is_mod = False
        self.msg_q = []
        self.timestamps = []
        self.last_sent = time.time() - 10
        self.verbose = verbose
        self.socket = socket.socket()
        self.connect()

    def connect(self):
        self.socket.connect(('irc.chat.twitch.tv', 6667))
        self.send_data('PASS ' + self.oauth, silent=True)
        self.send_data('NICK ' + self.user, silent=True)
        self.send_data('JOIN ' + self.channel, silent=True)
        self.send_data('CAP REQ :twitch.tv/membership', silent=True)
        self.send_data('CAP REQ :twitch.tv/tags', silent=True)
        self.send_data('CAP REQ :twitch.tv/commands', silent=True)

    def recv(self):
        data = self.socket.recv(2048).decode('utf-8', 'ignore')
        if data.strip() == "PING :tmi.twitch.tv":
            self.pong()
            return None
        elif "USERSTATE" in data:
            self.check_mod(data)
        else:
            return data

    def pong(self):
        self.send_data("PONG :tmi.twitch.tv", silent=True)

    def check_mod(self, data):
        chunks = data.split(" ")
        tags = parse_tags(chunks[0])
        if tags["mod"] == "1":
            self.is_mod = True
        else:
            self.is_mod = False

    def get_rate_limit(self):
        if self.is_mod:
            return 0.1
        else:
            return 1.1

    def get_msg_limit(self):
        if self.is_mod:
            return 100
        else:
            return 20

    def queue_data(self, message):
        self.msg_q.append(message)

    def send_queued_data(self, silent=False):
        if len(self.timestamps) > 0:
            while self.timestamps[0] - time.time() > 30:
                self.timestamps.pop()
        while len(self.msg_q) > 0:
            if len(self.timestamps) < self.get_msg_limit():
                time_since_last = time.time() - self.last_sent
                if time_since_last < self.get_rate_limit():
                    time.sleep(self.get_rate_limit() - time_since_last)
                self.send_data(self.msg_q[0], silent)               
                self.timestamps.append(time.time())
                self.last_sent = time.time()
                self.msg_q = self.msg_q[1:]
            else:
                break

    def send_data(self, message, silent=False):
        self.socket.send(encodeb(message + '\r\n'))
        if not silent and self.verbose:
            print(f'{Fore.YELLOW}SENT: ' + message + f'{Style.RESET_ALL}')