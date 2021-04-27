import logging
import os
import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE


class Email:

    def __init__(self):
        self._logger = logging.getLogger(__name__)
        self._subject = None
        self._from_addr = 'from_addr@example.com'  # Actual sender
        self._from_display_name = 'Display Name <DoNotReply@example.com>'  # Masked display name of sender
        self._to_addr = []
        self._cc_addr = []
        self._body = None
        self._body_type = 'plain'
        self._attachments = []
        self._smtp_server = 'smtp.example.com'
        self._port = 25

    @property
    def smtp_server(self):
        return self._smtp_server

    @smtp_server.setter
    def smtp_server(self, val):
        self._smtp_server = val

    @property
    def from_display_name(self):
        return self._from_display_name

    @from_display_name.setter
    def from_display_name(self, val):
        self._from_display_name = val

    @property
    def from_addr(self):
        return self._from_addr

    @from_addr.setter
    def from_addr(self, val):
        self._from_addr = val

    @property
    def to_addr(self):
        return self._to_addr

    @to_addr.setter
    def to_addr(self, val):
        if isinstance(val, str):
            if COMMASPACE in val:
                self._to_addr = val.split(COMMASPACE)
            else:
                self._to_addr = val.split(',')
        else:
            self._to_addr = val

    @property
    def cc_addr(self):
        return self._cc_addr

    @cc_addr.setter
    def cc_addr(self, val):
        if isinstance(val, str):
            if COMMASPACE in val:
                self._cc_addr = val.split(COMMASPACE)
            else:
                self._cc_addr = val.split(',')
        else:
            self._cc_addr = val

    @property
    def subject(self):
        return self._subject

    @subject.setter
    def subject(self, val):
        self._subject = val

    def set_body(self, body, body_type='plain'):
        self._body = body
        self._body_type = body_type

    def add_attachment(self, filepath):
        self._attachments.append((os.path.basename(filepath), open(filepath, "rb").read()))

    def send(self):
        if self._to_addr is None and self._cc_addr is None:
            self._logger.error("No mail recipient. Assign value to at least one of follow fields: to_addr or cc_addr.")

        if self._body_type == 'plain' and len(self._attachments) == 0:
            msg = MIMEText(self._body)
        else:
            msg = MIMEMultipart()
            msg.attach(MIMEText(self._body, self._body_type))

        msg['From'] = self._from_display_name
        msg['To'] = COMMASPACE.join(self._to_addr)
        msg['Cc'] = COMMASPACE.join(self._cc_addr)
        msg['Subject'] = self._subject

        self._logger.info(f"EMAIL FROM shown as:{msg['From']}")
        self._logger.info(f"EMAIL FROM:{self._from_addr}")
        self._logger.info(f"EMAIL To:{msg['To']}")
        self._logger.info(f"EMAIL Cc:{msg['Cc']}")
        self._logger.info(f"EMAIL Subject:{msg['Subject']}")

        for filename, content in self._attachments:
            self._logger.info(f"Adding attachment: {filename}")
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(content)
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f'attachment; filename={filename}')
            msg.attach(part)

        self._logger.info(f"EMAIL SMTP Server:{self._smtp_server}")
        self._logger.info(f"EMAIL SMTP Port:{self._port}")
        server = smtplib.SMTP(self._smtp_server, self._port)
        server.sendmail(self._from_addr, self._to_addr + self._cc_addr, msg.as_string())
        server.quit()


if __name__ == "__main__":
    mail = Email()
    mail.from_display_name = 'Display Name <DoNotReply@example.com>'
    mail.to_addr = 'to_addr@example.com'
    mail.subject = 'Test Subject'
    mail.set_body(body='<html><body>test mail</body><html>', body_type='html')
    # mail.add_attachment('C:\\tmp\\test.txt')
    mail.send()
