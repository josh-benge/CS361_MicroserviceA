import json
from flask import Flask, request, jsonify
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os
load_dotenv()

# references: https://dev.to/khaledhosseini/play-microservices-email-service-1kmc
# references: https://www.ory.sh/docs/kratos/self-hosted/email-http
# references: https://medium.com/the-andela-way/create-a-simple-microservice-with-celery-python-flask-redis-to-send-emails-with-gmail-api-224cc74ac7b3

# documentation: https://www.w3schools.com/python/ref_requests_post.asp
# documentation: https://pypi.org/project/requests/
# documentation: https://sentry.io/answers/flask-configure-dev-server-visibility/
# documentation: https://docs.python.org/3/library/email.mime.html
# documentation: https://docs.python.org/3/library/smtplib.html
# documentation: https://www.mailgun.com/blog/email/which-smtp-port-understanding-ports-25-465-587/

app = Flask(__name__)

# smtp server configuration 
SMTP_PORT = 587
SMTP_SERVER = 'smtp.gmail.com'
SENDER_EMAIL = os.getenv('SENDER_EMAIL')
SENDER_PASSWORD = os.getenv('SENDER_PASSWORD')

# endpoint to request data from and to receieve data also
@app.route('/send-email', methods=['POST'])
def emailService():
  try:
    # according to partner, JSON contains 'email' and 'message' parameters
    recipient_email = request.get_json().get('email')
    message = request.get_json().get('message')

    if not recipient_email or not message:
      return jsonify({"error": "Missing input"}), 400 # user/input error

    new_email = createEmail(recipient_email, message)
    sendEmail(recipient_email, new_email)

    return jsonify({"status": "success", "message": "Email sent"}), 200 # success

  except Exception:
    return jsonify({"error": str(Exception)}), 500 # server error

def createEmail(recipient_email, message):
  msg = MIMEMultipart()
  msg['To'] = recipient_email
  msg['From'] = SENDER_EMAIL
  msg['Subject'] = 'New message'
  msg.attach(MIMEText(message, 'plain'))
  return msg


def sendEmail(message, recipient):
  with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
    server.starttls()
    server.login(SENDER_EMAIL, SENDER_PASSWORD) 
    text = message.as_string()
    server.sendmail(SENDER_EMAIL, recipient, text)


if __name__ == '__main__':
  app.run(debug=True, port=5000, host='0.0.0.0')
