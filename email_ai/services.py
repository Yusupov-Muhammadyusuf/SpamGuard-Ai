import imaplib
import email

from bs4 import BeautifulSoup
 
from email.header import decode_header
from email.utils import parseaddr
from email_ai.ml.predict import load_model, load_tokenizer, predict

model = load_model(vocab_size=5001)
tokenizer = load_tokenizer()

def get_emails_with_prediction(user_email, app_password, limit=10):
    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    mail.login(user_email, app_password)
    mail.select("inbox")

    status, messages = mail.search(None, "ALL")
    email_ids = messages[0].split()

    results = []

    for eid in email_ids[-limit:]:
        status, msg_data = mail.fetch(eid, "(RFC822)")
        raw_email = msg_data[0][1]
        msg = email.message_from_bytes(raw_email)

        # Take a Message-ID
        message_id = msg.get("Message-ID")
        clean_id = message_id.strip("<> ") if message_id else ""

        # Decoding subject
        raw_subject = msg["subject"] or ""
        decoded_parts = decode_header(raw_subject)
        subject_parts = []
        for content, charset in decoded_parts:
            if isinstance(content, bytes):
                subject_parts.append(content.decode(charset or "utf-8", errors="ignore"))
            else:
                subject_parts.append(str(content))
        subject = "".join(subject_parts)

        # Sender
        raw_from = msg["from"] or ""
        decoded_from_parts = decode_header(raw_from)
        from_parts = []

        for content, charset in decoded_from_parts:
            if isinstance(content, bytes):
                from_parts.append(content.decode(charset or "utf-8", errors="ignore"))
            else:
                from_parts.append(str(content))
        sender = "".join(from_parts)
                
        full_sender = "".join(from_parts)
        sender_name, sender_email = parseaddr(full_sender)
        sender = sender_name if sender_name else sender_email

        # Take a body section   
        body = ""
        if msg.is_multipart():
            for part in msg.walk():
                content_type = part.get_content_type()
                if content_type == "text/plain":
                    body = part.get_payload(decode=True).decode(errors="ignore")
                    break
                elif content_type == "text/html":
                    # If text/plain not found, we will change html into text
                    html_content = part.get_payload(decode=True).decode(errors="ignore")
                    soup = BeautifulSoup(html_content, "html.parser")
                    body = soup.get_text(separator=' ')
        else:
            content_type = msg.get_content_type()
            if content_type == "text/html":
                html_content = msg.get_payload(decode=True).decode(errors="ignore")
                soup = BeautifulSoup(html_content, "html.parser")
                body = soup.get_text(separator=' ')
            else:
                body = msg.get_payload(decode=True).decode(errors="ignore")

        body = " ".join(body.split())

        # Spam or Ham
        text = subject + " " + body
        prediction = predict(text, model, tokenizer)

        results.append({
            "sender": sender,
            "subject": subject,
            "body": body[:200].replace('\n', ' ').strip(),
            "label": "SPAM" if prediction == 1 else "HAM",
            "message_id": clean_id,
        })

    mail.logout()
    return results