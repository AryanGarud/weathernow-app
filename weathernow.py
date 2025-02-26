import os
import threading
import requests
import smtplib
import schedule
import time
import logging
from email.mime.text import MIMEText
import tkinter as tk
from tkinter import ttk, messagebox

# --- Logging Configuration ---
LOG_FILE_PATH = os.path.join(os.getcwd(), 'weather_notifier.log')
logging.basicConfig(level=logging.INFO,
                    filename=LOG_FILE_PATH,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# --- Weather Fetching Function ---
def fetch_weather(api_key, location, units='metric'):
    """
    Fetch weather data from the dummy API server.
    The API key is not used in this dummy setup.
    """
    # Use the local API server URL instead of the real OpenWeatherMap endpoint.
    url = f"http://localhost:5000/data/2.5/weather?q={location}&appid={api_key}&units={units}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        weather_report = (
            f"Weather Update for {data['name']}:\n"
            f"Temperature: {data['main']['temp']}°{'C' if units == 'metric' else 'F'}\n"
            f"Humidity: {data['main']['humidity']}%\n"
            f"Conditions: {data['weather'][0]['description'].capitalize()}\n"
        )
        logging.info("Weather data fetched successfully.")
        return weather_report
    except requests.RequestException as e:
        logging.error(f"Error fetching weather data: {e}")
        return None

# --- Email Notification Function ---
def send_email(smtp_server, port, username, password, to_email, subject, message):
    msg = MIMEText(message)
    msg['Subject'] = subject
    msg['From'] = username
    msg['To'] = to_email
    try:
        with smtplib.SMTP(smtp_server, port) as server:
            server.starttls()
            server.login(username, password)
            server.sendmail(username, to_email, msg.as_string())
        logging.info("Email sent successfully.")
    except Exception as e:
        logging.error(f"Failed to send email: {e}")

# --- SMS Notification Function using Twilio ---
def send_sms(account_sid, auth_token, from_number, to_number, message):
    try:
        from twilio.rest import Client
    except ImportError:
        logging.error("Twilio library not installed. Run 'pip install twilio'")
        return
    try:
        client = Client(account_sid, auth_token)
        sms = client.messages.create(
            body=message,
            from_=from_number,
            to=to_number
        )
        logging.info(f"SMS sent successfully. SID: {sms.sid}")
    except Exception as e:
        logging.error(f"Failed to send SMS: {e}")

# --- Notification Function ---
def send_notification(message, use_sms, email_settings, sms_settings):
    subject = "Daily Weather Update"
    if use_sms:
        send_sms(sms_settings['account_sid'], sms_settings['auth_token'],
                 sms_settings['from_number'], sms_settings['to_number'], message)
    else:
        send_email(email_settings['smtp_server'], email_settings['port'],
                   email_settings['username'], email_settings['password'],
                   email_settings['to_email'], subject, message)

# --- Job Function ---
def job(config):
    logging.info("Job started.")
    weather_report = fetch_weather(config['weather_api_key'], config['location'], config['units'])
    if weather_report:
        send_notification(weather_report, config['use_sms'], config['email_settings'], config['sms_settings'])
    else:
        logging.error("No weather report available to send.")
    logging.info("Job completed.")

# --- Background Scheduler Thread ---
def scheduler_thread(config, schedule_time):
    schedule.every().day.at(schedule_time).do(job, config)
    logging.info(f"Job scheduled daily at {schedule_time}.")
    while True:
        schedule.run_pending()
        time.sleep(60)

# --- Tkinter GUI Application ---
class WeatherNotifierApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Weather Notifier Setup")
        self.geometry("500x600")
        self.create_widgets()
        self.scheduler = None

    def create_widgets(self):
        # Weather settings frame
        weather_frame = ttk.LabelFrame(self, text="Weather API Settings")
        weather_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(weather_frame, text="API Key:").grid(row=0, column=0, sticky="e", padx=5, pady=2)
        self.api_key_entry = ttk.Entry(weather_frame, width=40)
        # For the dummy API, the API key is not actually used.
        self.api_key_entry.insert(0, "API_KEY")
        self.api_key_entry.grid(row=0, column=1, padx=5, pady=2)

        ttk.Label(weather_frame, text="Location:").grid(row=1, column=0, sticky="e", padx=5, pady=2)
        self.location_entry = ttk.Entry(weather_frame, width=40)
        self.location_entry.insert(0, "Mumbai")
        self.location_entry.grid(row=1, column=1, padx=5, pady=2)

        ttk.Label(weather_frame, text="Units:").grid(row=2, column=0, sticky="e", padx=5, pady=2)
        self.units_var = tk.StringVar(value="metric")
        units_combo = ttk.Combobox(weather_frame, textvariable=self.units_var, values=["metric", "imperial"], state="readonly")
        units_combo.grid(row=2, column=1, padx=5, pady=2)

        # Email settings frame
        email_frame = ttk.LabelFrame(self, text="Email Settings")
        email_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(email_frame, text="SMTP Server:").grid(row=0, column=0, sticky="e", padx=5, pady=2)
        self.smtp_server_entry = ttk.Entry(email_frame, width=40)
        self.smtp_server_entry.insert(0, "smtp.example.com")
        self.smtp_server_entry.grid(row=0, column=1, padx=5, pady=2)

        ttk.Label(email_frame, text="Port:").grid(row=1, column=0, sticky="e", padx=5, pady=2)
        self.port_entry = ttk.Entry(email_frame, width=40)
        self.port_entry.insert(0, "587")
        self.port_entry.grid(row=1, column=1, padx=5, pady=2)

        ttk.Label(email_frame, text="Username:").grid(row=2, column=0, sticky="e", padx=5, pady=2)
        self.email_username_entry = ttk.Entry(email_frame, width=40)
        self.email_username_entry.insert(0, "your_email@example.com")
        self.email_username_entry.grid(row=2, column=1, padx=5, pady=2)

        ttk.Label(email_frame, text="Password:").grid(row=3, column=0, sticky="e", padx=5, pady=2)
        self.email_password_entry = ttk.Entry(email_frame, width=40, show="*")
        self.email_password_entry.grid(row=3, column=1, padx=5, pady=2)

        ttk.Label(email_frame, text="Recipient Email:").grid(row=4, column=0, sticky="e", padx=5, pady=2)
        self.recipient_email_entry = ttk.Entry(email_frame, width=40)
        self.recipient_email_entry.insert(0, "recipient@example.com")
        self.recipient_email_entry.grid(row=4, column=1, padx=5, pady=2)

        # SMS settings frame
        sms_frame = ttk.LabelFrame(self, text="SMS Settings (Twilio)")
        sms_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(sms_frame, text="Account SID:").grid(row=0, column=0, sticky="e", padx=5, pady=2)
        self.twilio_sid_entry = ttk.Entry(sms_frame, width=40)
        self.twilio_sid_entry.insert(0, "YOUR_TWILIO_ACCOUNT_SID")
        self.twilio_sid_entry.grid(row=0, column=1, padx=5, pady=2)

        ttk.Label(sms_frame, text="Auth Token:").grid(row=1, column=0, sticky="e", padx=5, pady=2)
        self.twilio_token_entry = ttk.Entry(sms_frame, width=40, show="*")
        self.twilio_token_entry.insert(0, "YOUR_TWILIO_AUTH_TOKEN")
        self.twilio_token_entry.grid(row=1, column=1, padx=5, pady=2)

        ttk.Label(sms_frame, text="From Number:").grid(row=2, column=0, sticky="e", padx=5, pady=2)
        self.twilio_from_entry = ttk.Entry(sms_frame, width=40)
        self.twilio_from_entry.insert(0, "+91234567890")
        self.twilio_from_entry.grid(row=2, column=1, padx=5, pady=2)

        ttk.Label(sms_frame, text="To Number:").grid(row=3, column=0, sticky="e", padx=5, pady=2)
        self.twilio_to_entry = ttk.Entry(sms_frame, width=40)
        self.twilio_to_entry.insert(0, "+910987654321")
        self.twilio_to_entry.grid(row=3, column=1, padx=5, pady=2)

        # Notifier options
        options_frame = ttk.LabelFrame(self, text="Notification Options")
        options_frame.pack(fill="x", padx=10, pady=5)

        self.use_sms_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(options_frame, text="Use SMS (Twilio) instead of Email", variable=self.use_sms_var).pack(padx=5, pady=5)

        ttk.Label(options_frame, text="Schedule Time (HH:MM 24h):").pack(padx=5, pady=2)
        self.schedule_time_entry = ttk.Entry(options_frame, width=20)
        self.schedule_time_entry.insert(0, "08:00")
        self.schedule_time_entry.pack(padx=5, pady=2)

        # Start button
        start_button = ttk.Button(self, text="Start Weather Notifier", command=self.start_notifier)
        start_button.pack(pady=15)

        # Status label
        self.status_label = ttk.Label(self, text="Status: Not running", foreground="red")
        self.status_label.pack(pady=5)

    def start_notifier(self):
        # Gather configuration data from the GUI
        config = {
            'weather_api_key': self.api_key_entry.get(),
            'location': self.location_entry.get(),
            'units': self.units_var.get(),
            'use_sms': self.use_sms_var.get(),
            'email_settings': {
                'smtp_server': self.smtp_server_entry.get(),
                'port': int(self.port_entry.get()),
                'username': self.email_username_entry.get(),
                'password': self.email_password_entry.get(),
                'to_email': self.recipient_email_entry.get()
            },
            'sms_settings': {
                'account_sid': self.twilio_sid_entry.get(),
                'auth_token': self.twilio_token_entry.get(),
                'from_number': self.twilio_from_entry.get(),
                'to_number': self.twilio_to_entry.get()
            }
        }
        schedule_time = self.schedule_time_entry.get()

        # Validate basic configuration
        if not config['weather_api_key'] or not config['location']:
            messagebox.showerror("Error", "Please enter both the Weather API key and location.")
            return

        # Start the scheduler in a background thread
        thread = threading.Thread(target=scheduler_thread, args=(config, schedule_time), daemon=True)
        thread.start()
        logging.info("Scheduler thread started.")
        self.status_label.config(text="Status: Running", foreground="green")
        messagebox.showinfo("Started", "Weather Notifier is now running.\nCheck log file for details.")

if __name__ == '__main__':
    app = WeatherNotifierApp()
    app.mainloop()
