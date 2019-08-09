import os


class WeChatRobot:

    @staticmethod
    def send_message(message: str) -> None:
        command: str = ""
        command += "curl 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=292e1dd7-d1ef-491c-88b3-a49e6333f810'"
        command += " -H 'Content-Type: application/json' -d '"
        command += "{\"msgtype\": \"text\", \"text\": {\"content\": \""
        command += message
        command += "\"}}'"
        os.system(command=command)
