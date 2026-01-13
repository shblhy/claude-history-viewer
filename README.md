# Claude History Viewer

A web-based viewer for Claude Code (CLI) conversation history. Browse, search, and explore your AI coding sessions with a beautiful dark-themed interface.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-2.0+-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## Features

- **Browse Sessions**: View all your Claude Code conversation history
- **Full-text Search**: Search across all conversations
- **File Path Detection**: Automatically highlights file paths in messages
- **Click to Open**: Click any file path to open it in your file explorer (WeChat-style)
- **Multi-source Support**: Supports both CLI sessions and web export data
- **Pagination**: Efficiently handles large conversation histories
- **Dark Theme**: Easy on the eyes for long coding sessions

## Screenshots

```
+------------------+------------------------+
|  Session List    |   Conversation View    |
|                  |                        |
|  > Project A     |  [user] How do I...    |
|    01-13 22:30   |                        |
|                  |  [assistant] You can   |
|  > Project B     |  use D:\path\file.cs   |  <- Clickable!
|    01-12 18:45   |                        |
+------------------+------------------------+
```

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Quick Start

```bash
# Clone the repository
git clone https://github.com/yangzealliator-yz/claude-history-viewer.git
cd claude-history-viewer

# Install dependencies
pip install -r requirements.txt

# Run the server
python app.py
```

Open your browser and navigate to `http://localhost:5000`

## Usage

### Basic Usage

1. Run `python app.py`
2. Open `http://localhost:5000` in your browser
3. Browse your Claude Code sessions on the left panel
4. Click a session to view the conversation
5. Click any highlighted file path to open it in your file explorer

### Keyboard Shortcuts

| Action | Shortcut |
|--------|----------|
| Open file in folder | Click on file path |
| View file content | Ctrl + Click on file path |

### Search

Use the search box to find conversations containing specific keywords. The search covers:
- Message content
- File paths
- Tool calls

## Data Sources

The viewer automatically detects and loads conversations from:

### 1. Claude Code CLI (Local)

Default location: `~/.claude/projects/`

```
~/.claude/
└── projects/
    └── {project-name}/
        ├── {session-id}.jsonl
        └── ...
```

### 2. Web Export (Optional)

Export your conversations from Claude.ai and place them in:

```
~/.claude/
└── web_export/
    └── conversations.json
```

## Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `PORT` | `5000` | Server port |
| `HOST` | `0.0.0.0` | Server host |

### Custom Data Path

Modify the `CLAUDE_PROJECTS` variable in `app.py` to point to your custom data location.

## Supported File Types

The viewer recognizes and highlights paths for these file types:

| Category | Extensions |
|----------|------------|
| Code | `.cs`, `.py`, `.js`, `.ts`, `.go`, `.rs`, `.java`, `.cpp`, `.c`, `.h` |
| Config | `.json`, `.yaml`, `.yml`, `.xml`, `.toml`, `.ini`, `.cfg` |
| Documents | `.md`, `.txt`, `.log`, `.csv` |
| Unity | `.unity`, `.prefab`, `.asset`, `.mat`, `.anim`, `.controller` |
| Images | `.png`, `.jpg`, `.jpeg`, `.gif`, `.webp`, `.svg` |
| And more... | `.bat`, `.sh`, `.sql`, `.html`, `.css`, etc. |

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Main web interface |
| `/api/sessions` | GET | List all sessions |
| `/api/conversation` | GET | Get conversation by session ID |
| `/api/search` | GET | Search conversations |
| `/api/file` | GET | Read local file content |
| `/api/open-folder` | GET | Open file in system explorer |

## Troubleshooting

### "File not found" when clicking a path

This means the file existed when the conversation was recorded but has since been moved or deleted. You can click "Copy Path" to copy the path to your clipboard.

### Server won't start

Make sure port 5000 is not in use:
```bash
# Windows
netstat -ano | findstr :5000

# Linux/Mac
lsof -i :5000
```

### Chinese characters not displaying correctly

Ensure your terminal and browser support UTF-8 encoding.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built for use with [Claude Code](https://claude.ai/claude-code) by Anthropic
- Inspired by the need to review and archive AI coding sessions

## Changelog

### v1.0.0 (2026-01-13)
- Initial release
- Session browsing and search
- File path detection and click-to-open
- Support for CLI and web export data
- Dark theme UI

---

**Made with Claude Code**
