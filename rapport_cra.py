import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime

def get_latest_md_file(directory):
    files = [f for f in os.listdir(directory) if f.endswith('.md')]

    # Sort files by descending name
    files.sort(reverse=True)
    return files[0] if files else None

def send_email(subject, body, to_email, attachment_path):
    from_email = os.getenv('EMAIL_USER')
    from_password = os.getenv('EMAIL_PASS')

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    if attachment_path:
        attachment = open(attachment_path, 'rb')
        part = MIMEBase('application', 'octet-stream')
        part.set_payload((attachment).read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename= {os.path.basename(attachment_path)}')
        msg.attach(part)

    server = smtplib.SMTP('smtp-cdaw.alwaysdata.net', 587)
    server.starttls()
    server.login(from_email, from_password)
    text = msg.as_string()
    server.sendmail(from_email, to_email, text)
    server.quit()

if __name__ == "__main__":
    subject = "Weekly Report"
    body = f"""
Bonjour madame,

Vous trouverez ci-joint le rapport hebdomadaire de mon alternance de la semaine {datetime.now().strftime("%W")}.

Cordialement,

Daw Charles

(Ce mail est généré automatiquement)
"""
    to_email = os.getenv('EMAIL_PROF')

    # Directory = current year
    repo_directory = f'{os.getcwd()}/{datetime.now().year}'
    latest_md_file = get_latest_md_file(repo_directory)

    if latest_md_file:
        attachment_path = os.path.join(repo_directory, latest_md_file)
        send_email(subject, body, to_email, attachment_path)
        print("Email sent successfully.")
    else:
        print("No markdown files found.")