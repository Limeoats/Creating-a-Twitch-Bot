# bot.py
# The code for our bot

import cfg
import utils
import sql
import socket
import re
import time, thread
from time import sleep

class Command(object):
    cmd = ""
    response = ""
    description = ""
    op = 0
    def __init__(self, cmd, response, description, op):
        self.cmd = cmd
        self.response = response
        self.description = description
        self.op = op

def parse(c, s):
    if c.response.find("~") > -1:
        list = c.response.split("~")
        for item in list:
            if item.find("{") > -1:
                code = item.split("{")[1].split("}")[0]
                utils.chat(s, item.split("{")[0] + eval(code))
            else:
                utils.chat(s, item)
    else:

        if c.response.find("{") > -1:
            code = c.response.split("{")[1].split("}")[0]
            utils.chat(s, c.response.split("{")[0] + eval(code))
        else:
            utils.chat(s, c.response)

def main():
    # Networking functions
    s = socket.socket()
    s.connect((cfg.HOST, cfg.PORT))
    s.send("PASS {}\r\n".format(cfg.PASS).encode("utf-8"))
    s.send("NICK {}\r\n".format(cfg.NICK).encode("utf-8"))
    s.send("JOIN #{}\r\n".format(cfg.CHAN).encode("utf-8"))

    CHAT_MSG = re.compile(r"^:\w+!\w+@\w+\.tmi\.twitch\.tv PRIVMSG #\w+ :")
    utils.chat(s, "Hi everyone!")

    thread.start_new_thread(utils.threadFillOpList, ())

    commands = sql.getCommands()

    cmd = []
    for c in commands:
        cmd.append(Command(c["Command"], c["Response"], c["Description"], c["Op"]))

    while True:
        response = s.recv(1024).decode("utf-8")
        if response == "PING :tmi.twitch.tv\r\n":
            s.send("PONG :tmi.twitch.tv\r\n".encode("utf-8"))
        else:
            username = re.search(r"\w+", response).group(0)
            message = CHAT_MSG.sub("", response)
            print(response)

            for c in cmd:
                if message.strip() == c.cmd:
                    if c.op == 0:
                        parse(c, s)
                    else:
                        if utils.isOp(username):
                            parse(c, s)
        sleep(1)
    utils.chat(s, "Bye everyone :)");
if __name__ == "__main__":
    main()