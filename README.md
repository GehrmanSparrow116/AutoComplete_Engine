# Trie-based Autocomplete Search Engine

A complete autocomplete search system built with a Trie data structure, Flask backend, and vanilla JavaScript frontend.

## Features

- **Fast Prefix Search**: O(m) lookup where m = prefix length
- **Top-K Suggestions**: DFS + min-heap for efficient ranking
- **Contextual Bigrams**: Multi-word phrase completion with bigram frequency boosting
- **Frequency-based Ranking**: Popular words and bigrams rank higher
- **Learning System**: Search frequency dynamically increases word/bigram priority
- **Real-time Stats**: Live trie statistics visualization

## Project Structure

```
autocomplete-engine/
├── backend/
│   ├── trie.py           # TrieNode and Trie classes
│   ├── data_loader.py    # Data loading with NLTK fallback
│   ├── app.py            # Flask REST API
│   └── words.csv         # Default word dataset
├── frontend/
│   └── index.html        # Single-file HTML/CSS/JS UI
└── README.md
```

## Quick Start

### 1. Install Dependencies

```bash
cd backend
pip install flask flask-cors
```

Optional for NLTK fallback:
```bash
pip install nltk
```

### 2. Run the Application

```bash
cd backend
python app.py
```

Server runs on `http://localhost:5000`

### 3. Open the UI

Simply visit `http://localhost:5000` in your web browser. The Flask backend automatically serves the frontend static files!

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/autocomplete` | Get suggestions for prefix (accepts optional `context`) |
| POST | `/insert` | Add a new word (accepts optional `context`) |
| DELETE | `/delete` | Remove a word |
| GET | `/stats` | Get trie statistics |
| POST | `/search` | Search word to increment freq (accepts optional `context`) |
| GET | `/words` | List all words |

### Example Requests

```bash
# Get suggestions with context
curl -X POST http://localhost:5000/autocomplete \
  -H "Content-Type: application/json" \
  -d '{"prefix": "le", "context": "machine", "top_k": 5}'

# Insert word with context
curl -X POST http://localhost:5000/insert \
  -H "Content-Type: application/json" \
  -d '{"word": "learning", "context": "machine", "frequency": 100}'

# Delete word
curl -X DELETE http://localhost:5000/delete \
  -H "Content-Type: application/json" \
  -d '{"word": "test"}'

# Get stats
curl http://localhost:5000/stats
```

## Trie Implementation

### TrieNode
- `children`: Dict of char → TrieNode
- `is_end`: Boolean marking word completion
- `frequency`: Integer for ranking

### Key Methods

| Method | Time | Description |
|--------|------|-------------|
| `insert(word, freq)` | O(n) | n = word length |
| `search(word)` | O(n) | Returns frequency or None |
| `delete(word)` | O(n) | With node pruning |
| `autocomplete(prefix, k)` | O(N log k) | N = nodes under prefix |
| `stats()` | O(N) | Words, nodes, depth |

## Frontend Features

- **Live Search**: Debounced 150ms input handling
- **Keyboard Navigation**: ↑↓ arrows + Enter selection
- **Visual Highlighting**: Bold prefix match in suggestions
- **Loading States**: Spinner during fetch
- **Empty State**: "No suggestions found" message
- **Stats Panel**: Real-time trie metrics
- **Add Word**: Insert new words directly from UI

## Data Sources

1. **Primary**: `words.csv` - ~5,000 most common English words (derived from NLTK)
2. **Fallback**: NLTK words corpus (if installed)
3. **Embedded**: Top 500 words hardcoded in `data_loader.py`

## Learning Algorithm

When a word is selected/searched or a new word is typed:
1. Client calls `POST /search` or `POST /insert` with the word and the preceding `context` word.
2. Server increments the word's absolute frequency.
3. Server also stores/increments the bigram `(context, word)` frequency.
4. Future `/autocomplete` requests with that context will multiply the suggestion's score by 2 if the bigram is known.
5. Stats refresh automatically.

## License

MIT
