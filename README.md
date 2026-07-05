# BuddyOS 🤖

A real-time voice AI that can hear, see, understand, and control your computer — on any OS. Supporting Windows, macOS, and Linux. Built with Gemini integration for maximum stability and performance, delivering zero subscriptions and total digital autonomy.

## ✨ Features

- **Real-Time Voice AI:** Natural, low-latency conversations with your computer.
- **Computer Control:** Can open apps, control settings, and manage your desktop environment.
- **Advanced Multi-Modal Search:** Comprehensive web search featuring specific modes (`news`, `research`, `price`, `compare`, `search`) that prioritize Gemini Grounded Search with an automatic DuckDuckGo fallback.
- **Morning Briefing Mode:** Automatically triggers once on first boot to read the time, pull local/global news, and check memory for your city to deliver a personalized weather update.
- **Audio-Visual System Monitor:** Background telemetry checks CPU, RAM, GPU, and temps every 10 seconds, delivering localized voice warnings with a 5-minute cooldown when thresholds are breached.
- **Zero Subscriptions:** Bring your own API key and enjoy complete digital autonomy.

## 🚀 Getting Started

### Prerequisites
- Python 3.10 or higher
- A free Google Gemini API Key

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Sanskar9081/BuddyOS.git
   cd BuddyOS
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure your API Key:**
   - Navigate to the `config` folder.
   - Copy `api_keys.example.json` and rename it to `api_keys.json`.
   - Open `api_keys.json` and paste your Gemini API key inside:
     ```json
     {
         "gemini_api_key": "YOUR_GEMINI_API_KEY_HERE",
         "os_system": "windows"
     }
     ```
   *(Note: The `api_keys.json` file is ignored by Git, so your keys will never be accidentally uploaded).*

4. **Run BuddyOS:**
   ```bash
   python main.py
   ```

## 🔒 Security & Privacy
BuddyOS is designed for complete digital autonomy. All processing logic respects your local environment, and your private certificates and configuration files are heavily safeguarded.

---
**Version:** v1.0.0
