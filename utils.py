# utils.py
# A bunch of utility functions

import cfg
import urllib2, json
import time, thread
from time import sleep

# Function: chat
# Send a chat message to the server.
#    Parameters:
#      sock -- the socket over which to send the message
#      msg  -- the message to send
def chat(sock, msg):
    sock.send("PRIVMSG #{} :{}\r\n".format(cfg.CHAN, msg))

# Function: ban
# Ban a user from the channel
#   Parameters:
#       sock -- the socket over which to send the ban command
#       user -- the user to be banned
def ban(sock, user):
    chat(sock, ".ban {}".format(user))

# Function: timeout
# Timeout a user for a set period of time
#   Parameters:
#       sock -- the socket over which to send the timeout command
#       user -- the user to be timed out
#       seconds -- the length of the timeout in seconds (default 600)
def timeout(sock, user, seconds=600):
    chat(sock, ".timeout {}".format(user, seconds))

# Function: threadFillOpList
# In a separate thread, fill up the op list
def threadFillOpList():
    while True:
        try:
            url = "http://tmi.twitch.tv/group/user/limeoats/chatters"
            req = urllib2.Request(url, headers={"accept": "*/*"})
            response = urllib2.urlopen(req).read()
            if response.find("502 Bad Gateway") == -1:
                cfg.oplist.clear()
                data = json.loads(response)
                for p in data["chatters"]["moderators"]:
                    cfg.oplist[p] = "mod"
                for p in data["chatters"]["global_mods"]:
                    cfg.oplist[p] = "global_mod"
                for p in data["chatters"]["admins"]:
                    cfg.oplist[p] = "admin"
                for p in data["chatters"]["staff"]:
                    cfg.oplist[p] = "staff"
        except:
            'do nothing'
        sleep(5)

def isOp(user):
    return user in cfg.oplist