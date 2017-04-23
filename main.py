from irc_socket import IRC


class EchoBot(object):
    def __init__(self):
        self.irc = IRC()

        self.server = None
        self.channel = None
        self.nickname = None
        self.password = None
        self.realname = None

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
            
            for msg in raw:
                self.parser(msg)
 
    def parser(self, raw):
        if len(raw.split(" ")) < 2:
            return

        if not raw.startswith(":"):
            raw = ":server " + raw

        sender, command, rawmessage = raw.split(" ", maxsplit=2)
        if " :" in rawmessage:
            receiver, msg = rawmessage.split(" :", maxsplit=1)
        else:
            receiver, msg = None, rawmessage

        print(
            "IN - ",
            "S:", sender,
            "C:", command,
            "R:", receiver,
            "M:", msg
        )

        if command == "PING":
            self.irc.pong(msg)

        if command == "VERSION":
            self.irc.version()

        if command == "376":
            # handle after the end of MOTD
            self.irc.join(self.channel)
            self.irc.identify(self.nickname, self.password)
            self.irc.mode(self.nickname, "B")

        if "433" in msg and msg.startswith(":services"):
            self.irc.identify(self.nickname, self.password)

        if sender.startswith(":Eric!"):
            if "!shutdown" in msg:
                self.irc.quit()
                return
            if "!command" in msg:
                msg = msg.replace("!command ", "")
                self.irc.send(msg)

        if command == "PRIVMSG" and self.channel == receiver and "hello" in msg:
            self.irc.privmsg(self.channel, "Hello!")


def main():
    echo = EchoBot()
    echo.getConfig()
    echo.run()

if __name__ == '__main__':
    main()