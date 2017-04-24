from irc_socket import IRC


class EchoBot(object):
    def __init__(self):
        self.irc = IRC()

        self.server = ""
        self.channel = ""
        self.nickname = ""
        self.password = ""
        self.realname = ""

    def getConfig(self):
        with open(file="config", mode="r", encoding="utf-8") as file:
            for line in file:
                if ":" not in line:
                    continue
                setting, value = line.split(":")
                settings = ["nick", "name", "pass", "server", "channels"]
                if setting not in settings:
                    continue

                value = value.strip()
                if setting == "nick": self.nickname = value
                if setting == "name": self.realname = value
                if setting == "pass": self.password = value
                if setting == "server": self.server = value
                if setting == "channels": self.channel = value

    def run(self):

        self.irc.connect(
            self.server,
            self.channel,
            self.nickname,
            self.realname
        )

        while 1:
            raw = self.irc.recv()

            # sometimes messages come in bulk!
            raw = raw.split("\n")
            for msg in raw:
                self.parser(msg)
 
    def parser(self, raw):
        """ this parses the raw irc messages 
        
        Args: 
            raw (str): an irc message
        """

        # remove junk
        if len(raw.split(" ")) < 2:
            return

        # cleanup carriage returns!
        raw = raw.replace(chr(13), "")

        # add a sender to 'senderless' commands
        if not raw.startswith(":"):
            raw = ":server " + raw

        print("IN:", raw)

        # split the irc string into components
        sender, command, rawmessage = raw.split(" ", maxsplit=2)
        if " :" in rawmessage:
            receiver, msg = rawmessage.split(" :", maxsplit=1)
        else:
            receiver, msg = None, rawmessage

        sender_nick = None
        sender_user = None
        sender_host = None

        if "@" in sender:
            name, sender_host = sender.split("@")
            sender_nick, sender_name = name[1:].split("!")

        if command.upper() == "PING":
            self.irc.pong(msg)

        if command.upper() == "NOTICE":
            pass

        if command.upper() == "PRIVMSG":
            pass

        if command == "376":
            # handle after the end of MOTD
            self.irc.join(self.channel)
            self.irc.identify(self.password)
            self.irc.mode(self.nickname, "B")

        if "test" in msg:
            for letter in msg:
                print(ord(letter))

        # handle CTCP messages ...
        if msg.startswith(chr(1)) and command != "NOTICE":
            self.ctcpHandler(sender_nick, msg)

        if msg.startswith("!") and command != "NOTICE":
            self.commandHandler(sender_nick, msg)

        if command == "PRIVMSG" and self.channel == receiver and "hello" in msg:
            self.irc.privmsg(self.channel, "Hello!")

    def commandHandler(self, nick, msg):
        if nick in self.admins
        if sender.startswith(":Eric!"):
            if "!shutdown" in msg:
                self.irc.quit()
                return
            if "!command" in msg:
                msg = msg.replace("!command ", "")
                self.irc.send(msg)
            if "!ctcp" in msg:
                msg = msg.replace("!ctcp ", "")
                receiver = msg.split(" ")[0]
                msg = msg.split(" ", maxsplit=1)[1]
                self.irc.ctcp_send(receiver, msg)


    def ctcpHandler(self, sender_nick, msg):
        if msg.upper().startswith(chr(1)+"VERSION"):
            self.irc.ctcp_version(sender_nick)
        elif msg.upper().startswith(chr(1)+"SOURCE"):
            self.irc.ctcp_source(sender_nick)
        elif msg.upper().startswith(chr(1)+"FINGER"):
            self.irc.ctcp_finger(sender_nick)
        elif msg.upper().startswith(chr(1)+"TIME"):
            self.irc.ctcp_time(sender_nick)
        elif msg.upper().startswith(chr(1)+"PING"):
            self.irc.ctcp_ping(sender_nick, msg)

        elif msg.upper().startswith(chr(1)+"LAG"):
            pass
        elif msg.upper().startswith(chr(1)+"ACTION"):
            pass

        else:
            self.irc.ctcp_error(sender_nick, msg, self.nickname)


def main():
    echo = EchoBot()
    echo.getConfig()
    echo.run()

if __name__ == '__main__':
    main()