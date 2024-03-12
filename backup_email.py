import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os
import tarfile

# info for the Email
subject = "System Backup"
body = "Backup for Kali machine."
to_email = "example@example.com"
from_email = "example@example.com"
password = "Password for from_email"

def create_backup():
    # Create a temporary directory for backup
    backup_dir = "/tmp/backup"
    try:
        os.makedirs(backup_dir, exist_ok=True)

        # Create a backup for any directory add into files_to_backup
        files_to_backup = ["/etc/", "/var/"]
        backup_file = "/tmp/system_backup.tar.gz"
        with tarfile.open(backup_file, "w:gz") as tar:
            for file in files_to_backup:
                tar.add(file, arcname=os.path.basename(file))

        return backup_file
    except Exception as e:
       print("Error creating backup:", e)
       return None


def send_email(subject, body, to_email, from_email, password, attachment=None):
    server = None
    try:
        msg = MIMEMultipart()
        msg['From'] = from_email
        msg['To'] = to_email
        msg['Subject'] = subject

        msg.attach(MIMEText(body, 'plain'))

        if attachment:
            with open(attachment, 'rb') as f:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(f.read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', f'attachment; filename="{os.path.basename(attachment)}"')
                msg.attach(part)

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(from_email, password)
        text = msg.as_string()
        server.sendmail(from_email, to_email, text)
        print("Email sent successfully!")
    except Exception as e:
        print("Error:", e)
    finally:
        if server:
            server.quit()

# Create backup
backup_file = create_backup()

# Send email with attachment
if backup_file:
   send_email(subject, body, to_email, from_email, password, attachment=backup_file)
   os.remove(backup_file)
else:
   print("Didn't create backup. Email terminated.")
