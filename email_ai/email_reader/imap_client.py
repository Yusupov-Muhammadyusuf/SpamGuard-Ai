import imaplib
import email

from email.header import decode_header

EMAIL = "muhammadyusuf.yusupov201@gmail.com"
PASSWORD = "App Password"

def connect_email():
    imap = imaplib.IMAP4_SSL("imap.gmail.com")
    imap.login(EMAIL, PASSWORD)

    return imap

def fetch_emails(imap, limit=5):
    imap.select("inbox")
    status, messages = imap.search(None, "ALL")
    email_ids = messages[0].split()

    return email_ids[-limit:]

def read_email(imap, email_id):
    status, msg_data = imap.fetch(email_id, "(RFC822)")
    raw_email = msg_data[0][1]
    msg = email.message_from_bytes(raw_email)

    return msg

def parse_email(msg):
    subject, encoding = decode_header(msg["Subject"])[0]

    if isinstance(subject, bytes):
        subject = subject.decode(encoding if encoding else "utf-8", errors="ignore")

    body = ""

    if msg.is_multipart():
        for part in msg.walk():

            if part.get_content_type() == "text/plain":
                body = part.get_payload(decode=True).decode(errors="ignore")
                break
    else:
        body = msg.get_payload(decode=True).decode(errors="ignore")

    return subject, body