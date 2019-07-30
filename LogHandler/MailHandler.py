import smtplib
from LogHandler.LogHandler import LogHandler
from email.mime.text import MIMEText
from email.header import Header


class MailHandler(LogHandler):
    def __init__(self):
        LogHandler.__init__(self)
        self.mail_host = self.get_config_value("mail", "host")
        self.mail_user = self.get_config_value("mail", "user")
        self.mail_password = self.get_config_value("mail", "password")
        self.mail_port = self.get_config_value("mail", "port")
        self.sender = self.get_config_value("mail", "sender")
        self.receivers = self.get_config_value("mail", "receivers")

    def send_mail(self, subject: str, content: str) -> None:
        message = MIMEText(content, 'plain', 'utf-8')
        message['Subject'] = Header(subject, 'utf-8')
        try:
            smtp_obj = smtplib.SMTP_SSL(self.mail_host, self.mail_port)
            smtp_obj.login(self.mail_user, self.mail_password)
            smtp_obj.sendmail(self.sender, self.receivers, message.as_string())
            smtp_obj.quit()
            self.logger.info(f"邮件发送成功: {message.as_string()}")
        except smtplib.SMTPException as e:
            self.logger.error(e)


if __name__ == '__main__':
    mail_handler = MailHandler()
    mail_handler.send_mail("subject", "content")
