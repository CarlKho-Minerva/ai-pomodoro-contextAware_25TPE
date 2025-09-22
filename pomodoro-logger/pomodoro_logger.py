#!/usr/bin/env python3
"""
Pomodoro Work Journal Logger
A 25-minute session logger that captures keystrokes, clipboard changes, and window activity.
"""

import time
import os
import threading
from datetime import datetime
from urllib.parse import quote_plus
import pyperclip
import pygetwindow as gw
from pynput import keyboard

# Configuration constants
SESSION_DURATION_SECONDS = 1500  # 25 minutes
LOG_FILE_PATH = os.path.expanduser('/Users/cvk/Downloads/CODELocalProjects/ai-pomodoro_25TPE/PomodoroLogs/')
POLL_INTERVAL_SECONDS = 2

class PomodoroLogger:
    def __init__(self):
        self.events = []
        self.running = False
        self.last_clipboard_content = ""
        self.last_window_title = ""
        self.keyboard_listener = None

        # Thread-safe lock for events list
        self.events_lock = threading.Lock()

        # Ensure log directory exists
        os.makedirs(LOG_FILE_PATH, exist_ok=True)

    def add_event(self, event_type, data):
        """Thread-safe method to add events to the log."""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        with self.events_lock:
            self.events.append((timestamp, event_type, data))

    def on_key_press(self, key):
        """Callback for keyboard events."""
        if not self.running:
            return False

        try:
            # Handle normal characters
            if hasattr(key, 'char') and key.char is not None:
                self.add_event('KEYSTROKE', key.char)
            else:
                # Handle special keys
                self.add_event('KEYSTROKE', str(key))
        except Exception as e:
            # Handle any key processing errors
            self.add_event('KEYSTROKE', f'[ERROR: {str(e)}]')

    def monitor_clipboard_and_window(self):
        """Monitor clipboard content and active window changes."""
        while self.running:
            try:
                # Check clipboard
                current_clipboard = pyperclip.paste()
                if current_clipboard != self.last_clipboard_content and current_clipboard.strip():
                    self.add_event('CLIPBOARD_COPY', current_clipboard[:100] + '...' if len(current_clipboard) > 100 else current_clipboard)
                    self.last_clipboard_content = current_clipboard

                # Check active window
                try:
                    active_window = gw.getActiveWindow()
                    if active_window:
                        current_window_title = str(active_window)
                        if (current_window_title != self.last_window_title and
                            current_window_title.strip()):
                            self.add_event('WINDOW_CHANGE', current_window_title)
                            self.last_window_title = current_window_title
                except Exception:
                    # Handle cases where no window is active or getActiveWindow fails
                    pass

            except Exception as e:
                self.add_event('SYSTEM_ERROR', f'Monitoring error: {str(e)}')

            time.sleep(POLL_INTERVAL_SECONDS)

    def format_events_for_export(self):
        """Format the captured events into a human-readable string."""
        with self.events_lock:
            formatted_lines = []
            for timestamp, event_type, data in self.events:
                formatted_lines.append(f'[{timestamp}] :: {event_type} :: {data}')
            return '\n'.join(formatted_lines)

    def generate_ai_studio_url(self, log_content):
        """Generate the pre-prompted AI Studio URL with the log content."""
        prompt = """Please analyze this Pomodoro work session log and create a concise work journal entry.

Based on the captured keystrokes, clipboard activities, and window changes, please:

1. Identify the main work focus/project
2. Summarize key activities and progress made
3. Note any tools, websites, or applications used
4. Highlight any interesting patterns or insights

Format your response as a Markdown file with:
- H1 title describing the work session
- 3-bullet summary of main activities
- <details> section containing the raw log for reference

Raw log data:
""" + log_content

        encoded_prompt = quote_plus(prompt)
        return f"https://aistudio.google.com/app/prompts/new?q={encoded_prompt}"

    def save_log_file(self):
        """Save the formatted events to a timestamped file."""
        timestamp = datetime.now().strftime('%Y-%m-%d_%H%M%S')
        filename = f'raw_log_{timestamp}.txt'
        filepath = os.path.join(LOG_FILE_PATH, filename)

        formatted_content = self.format_events_for_export()

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(formatted_content)

        return filepath, formatted_content

    def start_session(self, duration_seconds=None):
        """Start a Pomodoro logging session."""
        if duration_seconds is None:
            duration_seconds = SESSION_DURATION_SECONDS

        print("Starting 25-minute Pomodoro session... Press Ctrl+C to stop early.")

        self.running = True

        # Start keyboard listener
        self.keyboard_listener = keyboard.Listener(on_press=self.on_key_press)
        self.keyboard_listener.start()

        # Start clipboard and window monitoring in a separate thread
        monitor_thread = threading.Thread(target=self.monitor_clipboard_and_window)
        monitor_thread.daemon = True
        monitor_thread.start()

        try:
            # Wait for the session duration
            time.sleep(duration_seconds)
        except KeyboardInterrupt:
            print("\nSession stopped early by user.")

        # Stop logging
        self.running = False

        # Stop keyboard listener
        if self.keyboard_listener:
            self.keyboard_listener.stop()

        # Save the log file
        filepath, log_content = self.save_log_file()

        print(f"Session complete. Log saved to {filepath}")

        # Generate and display AI Studio URL
        ai_url = self.generate_ai_studio_url(log_content)
        print(f"\nAI Studio URL (click to analyze your session):")
        print(ai_url)

        return filepath

def main():
    """Main entry point for the Pomodoro logger."""
    logger = PomodoroLogger()
    logger.start_session()

if __name__ == "__main__":
    main()