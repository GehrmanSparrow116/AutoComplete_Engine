"""Flask Backend for Trie Autocomplete"""
import time
import os
from flask import Flask, request, jsonify
from flask_cors import CORS

from trie import Trie
from data_loader import load_words, save_words_to_csv, create_default_csv

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), '../frontend'), static_url_path='/')
CORS(app, resources={r"/*": {"origins": "*"}})

trie = Trie()
bigram_freq = {}
DATA_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_FILE = os.path.join(DATA_DIR, 'words.csv')


def initialize_trie():
    """Initialize trie with words from data source."""
    global trie
    trie = Trie()
    if not os.path.exists(CSV_FILE):
        create_default_csv(CSV_FILE)
    words = load_words(CSV_FILE)
    for word, frequency in words:
        trie.insert(word, frequency)
    stats = trie.stats()
    print(f"Trie: {stats['total_words']} words, {stats['total_nodes']} nodes, depth {stats['trie_depth']}")


@app.route('/')
def index():
    return app.send_static_file('index.html')


@app.route('/autocomplete', methods=['POST'])
def autocomplete():
    start_time = time.perf_counter()
    data = request.get_json() or {}
    prefix = data.get('prefix', '')
    context = data.get('context', '')
    top_k = data.get('top_k', 10)
    
    if not isinstance(prefix, str):
        return jsonify({"error": "prefix must be a string"}), 400
    if not isinstance(top_k, int) or top_k < 1 or top_k > 100:
        top_k = 10
    
    suggestions = trie.autocomplete(prefix, top_k)
    if context and isinstance(context, str):
        context = context.lower().strip()
        def get_score(sugg):
            bg_freq = bigram_freq.get((context, sugg['word']), 0)
            return sugg['frequency'] * 2 if bg_freq > 0 else sugg['frequency']
        suggestions.sort(key=get_score, reverse=True)
        
    elapsed_ms = (time.perf_counter() - start_time) * 1000
    
    return jsonify({
        "suggestions": suggestions,
        "time_ms": round(elapsed_ms, 3),
        "prefix": prefix,
        "count": len(suggestions)
    })


@app.route('/insert', methods=['POST'])
def insert_word():
    data = request.get_json() or {}
    word = data.get('word', '')
    context = data.get('context', '')
    frequency = data.get('frequency', 1)
    
    if not isinstance(word, str) or not word.strip():
        return jsonify({"error": "word must be a non-empty string"}), 400
    if not isinstance(frequency, int) or frequency < 1:
        frequency = 1
    
    word = word.lower().strip()
    if context and isinstance(context, str):
        context = context.lower().strip()
        bg_key = (context, word)
        bigram_freq[bg_key] = bigram_freq.get(bg_key, 0) + 1
        
    existing_freq = trie.search(word)
    is_new = existing_freq is None
    
    trie.insert(word, frequency)
    new_freq = trie.search(word)
    
    if is_new:
        all_words = trie.get_all_words()
        save_words_to_csv(all_words, CSV_FILE)
    
    return jsonify({
        "success": True,
        "word": word,
        "is_new": is_new,
        "previous_frequency": existing_freq,
        "new_frequency": new_freq,
        "added_frequency": frequency
    })


@app.route('/delete', methods=['DELETE'])
def delete_word():
    data = request.get_json() or {}
    word = data.get('word', '')
    
    if not isinstance(word, str) or not word.strip():
        return jsonify({"error": "word must be a non-empty string"}), 400
    
    word = word.lower().strip()
    existed = trie.search(word) is not None
    deleted = trie.delete(word)
    
    if deleted:
        all_words = trie.get_all_words()
        save_words_to_csv(all_words, CSV_FILE)
    
    return jsonify({
        "success": deleted,
        "word": word,
        "existed": existed,
        "deleted": deleted
    })


@app.route('/stats', methods=['GET'])
def get_stats():
    return jsonify(trie.stats())


@app.route('/search', methods=['POST'])
def search_word():
    data = request.get_json() or {}
    word = data.get('word', '')
    context = data.get('context', '')
    
    if not isinstance(word, str) or not word.strip():
        return jsonify({"error": "word must be a non-empty string"}), 400
    
    word = word.lower().strip()
    if context and isinstance(context, str):
        context = context.lower().strip()
        bg_key = (context, word)
        bigram_freq[bg_key] = bigram_freq.get(bg_key, 0) + 1
        
    frequency = trie.search(word)
    found = frequency is not None
    
    if found:
        trie.insert(word, 1)
        new_frequency = trie.search(word)
        return jsonify({
            "found": True,
            "word": word,
            "frequency": new_frequency,
            "previous_frequency": frequency
        })
    
    return jsonify({"found": False, "word": word, "frequency": None})


@app.route('/words', methods=['GET'])
def get_all_words():
    limit = request.args.get('limit', 1000, type=int)
    if limit < 1 or limit > 10000:
        limit = 1000
    
    words = trie.get_all_words()
    words_data = [{"word": w, "frequency": f} for w, f in words[:limit]]
    
    return jsonify({
        "words": words_data,
        "total": len(words),
        "returned": len(words_data)
    })


@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint not found"}), 404


@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500


if __name__ == '__main__':
    initialize_trie()
    app.run(host='0.0.0.0', port=5000, debug=True)
