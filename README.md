 🌦️ WeatherNow

A Python-based Weather Notifier application that fetches weather updates from a local API server and sends notifications via email or SMS. The application features a Tkinter-based GUI for easy configuration and scheduling.

 🚀 Features
- 🌍 Fetches weather updates from a local API server.
- 📧 Sends notifications via email using SMTP.
- 📱 Sends SMS notifications using Twilio.
- 🖥️ Provides a Tkinter-based GUI for easy setup.
- ⏰ Allows users to schedule daily notifications.
- 📝 Logs events and errors to a log file.

 🛠️ Requirements
- 🐍 Python 3.x
- 📦 Required Python libraries:
  - `requests`
  - `schedule`
  - `smtplib` (built-in)
  - `tkinter` (built-in)
  - `twilio` (for SMS notifications)
  - `logging` (built-in)

Install dependencies using:
```sh
pip install requests schedule twilio
```

 🔧 Installation
1. 📥 Clone the repository:
   ```sh
   git clone https://github.com/your-username/weathernow.git
   cd weathernow
   ```
2. ▶️ Run the script:
   ```sh
   python weathernow.py
   ```

 ⚙️ Configuration
- 🌐 **Weather API**: The application fetches weather data from a local API server running at `http://localhost:5000`.
- ✉️ **Email Settings**: Configure SMTP settings, including server, port, and credentials.
- 📲 **SMS Settings**: Set up Twilio account credentials for SMS notifications.
- ⏳ **Scheduling**: Users can specify a daily schedule (HH:MM in 24-hour format).

 📌 Usage
1. 🔑 Enter your API key and location.
2. ⚙️ Configure email or SMS settings.
3. ⏰ Set the desired notification time.
4. ✅ Click "Start Weather Notifier" to begin receiving updates.

 📜 Logging
- 📝 Logs are saved in `weathernow.log`.
- 📊 Provides information about fetched weather data, notification status, and errors.

 📄 License
This project is licensed under the MIT License.

 🤝 Contributions
Contributions, issues, and feature requests are welcome! Feel free to open an issue or submit a pull request.

Enjoy staying updated with the weather! 🌦️☀️🌍

