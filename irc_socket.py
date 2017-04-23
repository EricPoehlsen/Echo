import socket


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

        self.irc.send(bytes(msg, "utf-8"))
        print("OUT: ", msg, end="")

    def recv(self):
        """ This is the socket listener 
        
        Returns str 
        """
        msg = str(self.irc.recv(2040), "utf-8")  # receive the text
        return msg

    def privmsg(self, reciever, msg):
        self.send("PRIVMSG " + reciever + " " + msg + "\n")

    def mode(self, receiver, mode):
        self.send("MODE " + receiver + " " + mode + "\n")

    def connect(self, server, channel, nick, real):
        # defines the socket
        print("connecting to:" + server)
        self.irc.connect((server, 6667))  # connects to the server
        user_msg = " ".join(["USER", nick, nick, nick, real, "\n"])
        self.send(user_msg)
        nick_msg = "NICK " + nick + "\n"
        self.send(nick_msg)
        join_msg = "JOIN " + channel + "\n"
        self.send(join_msg)

    def join(self, channel):
        self.send("JOIN " + channel + "\n")

    def pong(self, msg):
        request = msg.split("PING :")[-1]
        pong_msg = 'PONG ' + request + '\n'
        self.send(pong_msg)

    def version(self):
        self.send("VERSION Echo Bot 0.0\n")

    def quit(self):
        self.send("QUIT :shutting down ... \n")

    def identify(self, nickname, password):
        ident_msg = "IDENTIFY " + password + "\n"
        self.send(ident_msg)