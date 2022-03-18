import email
import imaplib
class Read:
    def __init__(self,email,passwd):
        self.mail = imaplib.IMAP4_SSL("imap.gmail.com")
        self.email = email
        self.passwd = passwd
        self.mail.login(self.email, self.passwd)

    def main(self):
        self.mail.select("inbox")
        status, data = self.mail.search(None,"ALL")
        mail_ids = []
        for blocks in data:
            mail_ids += blocks.split()
        for elements in mail_ids:
            status, data = self.mail.fetch(elements,"(RFC822)")
            for response_part in data:
                if isinstance(response_part,tuple):
                    message = email.message_from_bytes(response_part[1])
                    mail_time = message["date"]
                    mail_from = message["from"]
                    mail_subject = message["subject"]
                if message.is_multipart():
                    mail_content = ''
                    for part in message.get_payload():
                        if part.get_content_type() == 'text/plain':
                            mail_content += part.get_payload()
                else:
                    mail_content = message.get_payload()
                print(f'Date:{mail_time}')
                print(f'From: {mail_from}')
                print(f'Subject: {mail_subject}')
                print(f'Content: {mail_content}')                        

read = Read("email","password")
read.main()
