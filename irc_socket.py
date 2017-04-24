import socket
import datetime
import platform
import os


class IRC:
    irc = socket.socket()

    def __init__(self):
        self.irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def send(self, msg):
        """ sends a raw message to the server
        
        Note:
            Commands are implemented as separate methods and will
            call the send method.
        
        Args:
            msg (str): the raw message to send
        """

        self.irc.send(bytes(msg + "\n", "utf-8"))
        print("OUT: ", msg)

    def recv(self):
        """ This is the socket listener 
        
        Returns str 
        """
        msg = str(self.irc.recv(2040), "utf-8")  # receive the text
        return msg

    def privmsg(self, reciever, msg):
        self.send("PRIVMSG " + reciever + " " + msg)

    def mode(self, receiver, mode):
        self.send("MODE " + receiver + " " + mode)

    def connect(self, server, channel, nick, real):
        # defines the socket
        print("connecting to:" + server)
        self.irc.connect((server, 6667))  # connects to the server
        user_msg = " ".join(["USER", nick, nick, nick, real])
        self.send(user_msg)
        nick_msg = "NICK " + nick
        self.send(nick_msg)

    def join(self, channel):
        self.send("JOIN " + channel)

    def pong(self, msg):
        self.send("PONG " + msg)

    def quit(self):
        self.send("QUIT :shutting down ...")

    def identify(self, password):
        self.send("IDENTIFY " + password)

    # ctcp handlers
    def ctcp_send(self, receiver, msg):
        privmsg = "PRIVMSG " + receiver + " :"
        msg = chr(1)+msg+chr(1)
        self.send(privmsg + msg)

    def ctcp_version(self, sender):
        notice = "NOTICE " + sender + " :"
        name = "Echo Bot"
        version = "0.0a"
        os_info = " ".join([
            platform.system(),
            platform.version(),
            platform.machine()
        ])
        info = [name, version, os_info]
        msg = chr(1) + "VERSION " + " : ".join(info) + chr(1)
        self.send(notice + msg)

    def ctcp_finger(self, sender):
        notice = "NOTICE " + sender + " :"
        info = "This Echo Bot is run by Eric Poehlsen - "\
               "https://www.eric-poehlsen.de"

        msg = chr(1) + "FINGER :" + info + chr(1)
        self.send(notice + msg)

    def ctcp_source(self, sender):
        notice = "NOTICE " + sender + " :"
        info = "The source code of Echo Bot is available at "\
               "https://github.com/EricPoehlsen/Echo"
        msg = chr(1) + "SOURCE :" + info + chr(1)
        self.send(notice + msg)

    def ctcp_time(self, sender):
        notice = "NOTICE " + sender + " :"
        time = str(datetime.datetime.now())
        msg = chr(1) + "TIME :" + time + chr(1)
        self.send(notice + msg)

    def ctcp_ping(self, sender, msg):
        notice = "NOTICE " + sender + " :"
        self.send(notice + msg)

    def ctcp_clientinfo(self, sender, msg):
        notice = "NOTICE " + sender + " :"
        info = "EchoBot 0.0a Supported tags: "
        implemented = [
            "PING",
            "VERSION",
            "CLIENTINFO",
            "USERINFO",
            "FINGER",
            "SOURCE",
            "TIME",
            "ACTION",
        ]
        not_implemented = [
            "AVATAR",
            "DCC",
            "PAGE"
        ]

        msg = chr(1) + "TIME :" + info + chr(1)
        self.send(notice + msg)

    def ctcp_error(self, sender, msg, nickname):
        print("trying to send error")
        notice = "NOTICE " + sender + " :"

        command = msg.replace(chr(1), "")
        if command.startswith("ERRMSG"):
            info = "You have successfully queried my error message ..."
        else:
            info = "{cmd} : unknown request. Try /CTCP {nick} CLIENTINFO".format(
                cmd=command,
                nick=nickname
            )
        out_msg = chr(1) + "ERRMSG :" + info + chr(1)
        print(notice + out_msg)

        # self.send(notice + out_msg)

    """
    USERINFO	- A string set by the user (never the client coder)
    CLIENTINFO	- Dynamic master index of what a client knows.
    PING		- Used to measure the delay of the IRC network
              between clients.
    TIME		- Gets the local date and time from other clients.
    """