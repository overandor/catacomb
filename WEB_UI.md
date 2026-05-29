# Catacomb Web UI

A modern web interface for the Catacomb Deterministic Agent Stack.

## Features

- **Search by Topic**: Find high-value intervention opportunities by GitHub topic
- **Search by User**: Analyze repositories from a specific GitHub user
- **Single Repo Analysis**: Deep dive into a specific repository
- **Real-time Scoring**: View intervention scores, effort estimates, and success probabilities
- **Modern UI**: Built with React, TailwindCSS, and Flask

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set GitHub token (optional, for higher rate limits):
```bash
export GITHUB_TOKEN=your_token
```

## Running the Web UI

Start the Flask server:
```bash
python app.py
```

The UI will be available at `http://localhost:5000`

## API Endpoints

- `GET /` - Serve the React UI
- `GET /api/analyze/repo/<owner>/<repo>` - Analyze a single repository
- `POST /api/analyze/topic` - Analyze repositories by topic
  - Body: `{"topic": "machine-learning", "limit": 10}`
- `POST /api/analyze/user` - Analyze repositories by user
  - Body: `{"username": "username", "limit": 10}`
- `GET /api/health` - Health check

## Environment Variables

- `GITHUB_TOKEN` - GitHub API token for higher rate limits
- `PORT` - Server port (default: 5000)
- `DEBUG` - Enable debug mode (default: false)

## Usage

1. Open the web UI in your browser
2. Select search mode (Topic, User, or Repo)
3. Enter your search query
4. Adjust the limit (number of repos to analyze)
5. Click "Analyze" to see results

## Understanding Results

Each result shows:
- **Intervention Score**: Overall potential (0-100)
- **Best Intervention**: Recommended action with effort, probability, and upside
- **Repo Stats**: Stars, forks, language
- **Hash**: Deterministic proof of analysis

## CLI Usage

The CLI interface is still available:
```bash
python catacomb.py topic "machine-learning"
python catacomb.py user "username"
python catacomb.py repo "owner/repo"
```
