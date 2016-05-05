# bot.py
# The code for our bot

import cfg
import utils
import socket
import re
import time, thread
from time import sleep

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

    while True:
        response = s.recv(1024).decode("utf-8")
        if response == "PING :tmi.twitch.tv\r\n":
            s.send("PONG :tmi.twitch.tv\r\n".encode("utf-8"))
        else:
            username = re.search(r"\w+", response).group(0)
            message = CHAT_MSG.sub("", response)
            print(response)

            # Custom commands
            if message.strip() == "!time":
                utils.chat(s, "It is currently " + time.strftime("%I:%M %p %Z on %A, %B %d, %Y."))
            if message.strip() == "!messages" and utils.isOp(username):
                utils.chat(s, "Please give Limeoats a follow at twitter.com/limeoats! All follows are greatly appreciated!!")
                utils.chat(s, "Go to patreon.com/limeoats to support me! :)")
        sleep(1)

if __name__ == "__main__":
    main()