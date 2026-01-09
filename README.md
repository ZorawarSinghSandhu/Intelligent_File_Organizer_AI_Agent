📂 Intelligent File Organizer Agent
An automated background service that monitors file system activity and organizes incoming files in real-time. Unlike standard scripts, this agent uses a Hybrid Architecture:

Rule-Based Engine: Instantly moves known file types (PDFs, JPGs, EXEs) to save compute costs.

AI-Powered Brain: Uses Google Gemini 2.0 Flash to analyze and classify unknown or ambiguous files based on their filename context.

🚀 Key Features
Real-Time Monitoring: Uses watchdog to detect files the moment they are downloaded.

Intelligent Classification: Distinguishes between "Personal", "Work", and "School" documents using LLM analysis.

Resilient Architecture: Implements a "Wait-and-Retry" loop to handle API rate limits (HTTP 429) gracefully.

Secure: API keys are managed via environment variables (.env), ensuring no sensitive data is hardcoded.

🛠️ Tech Stack
Language: Python 3.12+

AI Model: Google Gemini 2.0 Flash (via google-generativeai)

Automation: watchdog (Observer Pattern)

File Ops: shutil, os

Security: python-dotenv

⚙️ How It Works
The script runs a background thread to watch C:/Users/Downloads.

When a file arrives, it checks the extension against a hash map.

If Known: It moves the file immediately (O(1) complexity).

If Unknown: It sends the filename to Gemini with a prompt: "Classify this file into [Finance, School, Work, Personal]..."

If the API hits a Rate Limit, the script pauses and retries automatically.
