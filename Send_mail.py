import mimetypes
import smtplib, ssl

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

from datetime import date

def send_mail_csv(file_path):
    context = ssl.create_default_context()

    msg = MIMEMultipart('alternative')
    msg['Subject'] = "NBA injuries report"
    msg['From'] = "nba.injuries.report@gmail.com"
    msg['To'] = "your_mail_here@hotmail.com" # the mail you want to send the report to

    # Plain-text version of content
    plain_text = """\
        Hi there,
        This is your NBA injuries report for today."""
    # html version of content
    html_content = """\
        <html>
        <head></head>
        <body>
            <p>Hi there,</p>
            <p>This is your NBA injuries report for today</p>
            <p>GitHub repository : https://github.com/Seb943/NBA_injuries_report</p>
        </body>
    </html>"""

    text_part = MIMEText(plain_text, 'plain')
    html_part = MIMEText(html_content, 'html')

    msg.attach(text_part)
    msg.attach(html_part)

    # Define MIMEImage part
    ctype, encoding = mimetypes.guess_type(file_path)
    maintype, subtype = ctype.split('/', 1)
    with open(file_path, 'rb') as fp:
        img_part = MIMEImage(fp.read(), _subtype=subtype)
        # Set the filename for the attachment
        img_part.add_header('Content-Disposition', 'attachment', filename='NBA_injuries_{}.csv'.format(date.today()))
        msg.attach(img_part)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login("nba.injuries.report@gmail.com", 'nba_injuries_report') # email adress and password
        server.send_message(msg)
