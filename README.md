# Pomodoro Work Journal System

⚠️ New version with audio and snapshot every 5 minutes approach (for a 25 min sesh coming soon). Email kho@uni.minerva.edu with an ANGRY EMAIL if you want it now.  

A lightweight, local data-capture tool that integrates AI-summarized output into a portfolio website, displaying a granular feed of work sessions alongside published blog posts.

<div>
    <a href="https://www.loom.com/share/58088b77c6b94579a44261fde967a1ae">
      <p>AI Pomodoro!! - Watch Video</p>
    </a>
    <a href="https://www.loom.com/share/58088b77c6b94579a44261fde967a1ae">
      <img style="max-width:300px;" src="https://cdn.loom.com/sessions/thumbnails/58088b77c6b94579a44261fde967a1ae-33feea8c2cb161a6-full-play.gif">
    </a>
  </div>

## Project Overview

This system consists of three main components:

1. **The Capture Engine** - Local Python script that logs 25-minute work sessions
2. **The Content Pipeline** - Build script that processes content into HTML
3. **The Presentation Layer** - Responsive website displaying both blogs and work sessions

## Quick Start

### Phase 1: Capture Work Sessions

1. Install Python dependencies:

   ```bash
   cd pomodoro-logger
   pip3 install -r requirements.txt
   ```

2. Start a 25-minute logging session:

   ```bash
   ./start_pomodoro.sh
   ```

3. The script will capture:
   - Every keystroke
   - Clipboard changes
   - Active window changes

4. After 25 minutes (or Ctrl+C), a log file is saved to `~/Desktop/PomodoroLogs/`

5. An AI Studio URL is provided to generate a work journal entry

### Phase 2: Process AI Summary

1. Copy the AI-generated Markdown content
2. Save it as a `.md` file in `content/pomodoros/`
3. Use the format: `YYYY-MM-DD_session-name.md`

### Phase 3: Build Website

1. Run the build script:

   ```bash
   npm run build
   # or
   node build.js
   ```

2. Open the generated website:

   ```bash
   open dist/index.html
   ```

## File Structure

```
ai-pomodoro_25TPE/
├── pomodoro-logger/
│   ├── pomodoro_logger.py      # Main logging script
│   ├── start_pomodoro.sh       # Shell wrapper
│   ├── requirements.txt        # Python dependencies
│   └── test_pomodoro_logger.py # 60-second test version
├── content/
│   ├── blogs/                  # Blog post markdown files
│   └── pomodoros/              # Work session markdown files
├── src/
│   ├── index-template.html     # HTML template
│   └── css/
│       ├── main.css           # Layout and responsive styles
│       └── blog-post.css      # Content styling
├── dist/                       # Generated website
└── build.js                    # Build script
```

## AI Prompt Template

When processing logs, the AI receives this prompt:

> Please analyze this Pomodoro work session log and create a concise work journal entry.
>
> Based on the captured keystrokes, clipboard activities, and window changes, please:
>
> 1. Identify the main work focus/project
> 2. Summarize key activities and progress made
> 3. Note any tools, websites, or applications used
> 4. Highlight any interesting patterns or insights
>
> Format your response as a Markdown file with:
>
> - H1 title describing the work session
> - 3-bullet summary of main activities
> - `<details>` section containing the raw log for reference

## Expected AI Output Format

```markdown
# Session Title Here

- First key activity or achievement
- Second key activity or achievement
- Third key activity or achievement

<details>
<summary>Raw Session Log</summary>

[raw log data here...]

</details>
```

## Website Features

- **Responsive Design**: Two-column layout on desktop, stacked on mobile
- **Live Content**: Automatically processes new markdown files
- **Interactive Elements**: Expandable raw logs using HTML details tags
- **Dark Theme**: Optimized for developer workflows

## Testing

Test the capture engine with a 60-second session:

```bash
cd pomodoro-logger
python3 test_pomodoro_logger.py
```

## Core Principles

- **Simplicity**: No complex UI, just command-line tools
- **Separation of Concerns**: Capture and display are completely separate
- **Automation**: Only manual step is copy-paste of AI summaries

## Requirements

- Python 3.6+
- Node.js (for build script)
- macOS (for window/clipboard monitoring)

## License

MIT License - Feel free to adapt for your own productivity workflows.
