import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import datetime

import time
import GUI_time_entry

date_format = "%H:%M:%S"
# reference time
ref_time_converted = GUI_time_entry.total_time

# Email configuration
sender_email = "utilisation.tracker@gmail.com"
receiver_email = "utilisation.tracker@gmail.com"
app_password = "mgighaphvlbipsit"  # Use the App Password here
subject = "Daily Utilisation email"
if GUI_time_entry.total_time > ref_time_converted:
    message = "This is your daily utilisation email sent from utilisation tracker. \n" \
          "CONGRATULATION you reached your daily goal \n" \
              "Today you worked {}".format(GUI_time_entry.time_to_send)
else:
    message = "This is your daily utilisation email sent from utilisation tracker. \n" \
          "UNFORTUNATELY you could not reached your daily goal :( \n" \
              "Today you worked {}".format(GUI_time_entry.time_to_send)

# Function to send the email
def send_email():
    # Create the email message
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.attach(MIMEText(message, 'plain'))

    # Establish a connection to the SMTP server
    smtp_server = smtplib.SMTP('smtp.gmail.com', 587)
    smtp_server.starttls()

    # Log in to your email account using the App Password
    smtp_server.login(sender_email, app_password)

    # Send the email
    smtp_server.sendmail(sender_email, receiver_email, msg.as_string())

    # Close the SMTP server connection
    smtp_server.quit()

    print("Email sent successfully.")

# Calculate the delay until 20:01 (8:01 PM)
now = datetime.datetime.now()
target_time = datetime.datetime(now.year, now.month, now.day, 20, 51, 0)
time_difference = target_time - now
if time_difference.total_seconds() < 0:
    # If it's already past 20:01 today, schedule it for the same time tomorrow
    target_time += datetime.timedelta(days=1)

# Sleep until the target time
time.sleep(time_difference.total_seconds())

# Send the email at the target time
send_email()


