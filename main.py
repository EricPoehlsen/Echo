from irc_socket import IRC


def main():

    channel = "#HPGR"
    server = "irc.euirc.net"
    nickname = "EchoPapa"
    realname = ":ein Echo Bot"
    password = ""

    user_data = [
        nickname,

    ]
    irc = IRC()
    irc.connect(server, channel, nickname, realname)

    while 1:
        text = irc.recv()

        if "PING" in text:
            irc.pong(text)

        if "VERSION" in text:
            irc.version()

        if "402" in text:
            irc.join(channel)
            irc.identify(nickname, password)

        if "433" in text and text.startswith(":services"):
            irc.identify(nickname, password)

        if text.startswith(":Eric!"):
            if "!shutdown" in text:
                irc.quit()
                return

        if "PRIVMSG" in text and channel in text and "hello" in text:
            irc.privmsg(channel, "Hello!")

if __name__ == '__main__':
    main()