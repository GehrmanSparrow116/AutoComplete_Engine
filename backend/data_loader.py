"""Data Loader with fallback to embedded word list"""
import csv
import os
from typing import List, Tuple, Optional


FALLBACK_WORDS = [
    ("the", 10000), ("of", 9500), ("to", 9000), ("and", 8800), ("a", 8500),
    ("in", 8200), ("is", 8000), ("it", 7800), ("you", 7600), ("that", 7400),
    ("he", 7200), ("was", 7000), ("for", 6800), ("on", 6600), ("are", 6400),
    ("with", 6200), ("as", 6000), ("his", 5800), ("they", 5600), ("i", 5400),
    ("at", 5200), ("be", 5000), ("this", 4800), ("have", 4600), ("from", 4400),
    ("or", 4200), ("one", 4000), ("had", 3800), ("by", 3600), ("word", 3500),
    ("but", 3400), ("not", 3300), ("what", 3200), ("all", 3100), ("were", 3000),
    ("we", 2900), ("when", 2800), ("your", 2700), ("can", 2600), ("said", 2500),
    ("there", 2400), ("use", 2350), ("an", 2300), ("each", 2250), ("which", 2200),
    ("she", 2150), ("do", 2100), ("how", 2050), ("their", 2000), ("if", 1950),
    ("will", 1900), ("up", 1850), ("other", 1800), ("about", 1750), ("out", 1700),
    ("many", 1650), ("then", 1600), ("them", 1550), ("these", 1500), ("so", 1450),
    ("some", 1400), ("her", 1350), ("would", 1300), ("make", 1250), ("like", 1200),
    ("into", 1150), ("him", 1100), ("has", 1050), ("two", 1000), ("more", 950),
    ("very", 900), ("after", 880), ("words", 860), ("just", 840), ("where", 820),
    ("most", 800), ("get", 780), ("through", 760), ("back", 740), ("much", 720),
    ("before", 700), ("go", 680), ("good", 660), ("new", 640), ("write", 620),
    ("our", 600), ("me", 580), ("man", 560), ("too", 540), ("any", 520),
    ("day", 500), ("same", 490), ("right", 480), ("look", 470), ("think", 460),
    ("also", 450), ("around", 440), ("another", 430), ("came", 420), ("come", 410),
    ("work", 400), ("three", 390), ("must", 380), ("because", 370), ("does", 360),
    ("part", 350), ("even", 340), ("place", 330), ("well", 320), ("such", 310),
    ("here", 300), ("take", 295), ("why", 290), ("things", 285), ("help", 280),
    ("put", 275), ("years", 270), ("different", 265), ("away", 260), ("again", 255),
    ("off", 250), ("went", 245), ("old", 240), ("number", 235), ("great", 230),
    ("tell", 225), ("men", 220), ("say", 215), ("small", 210), ("every", 205),
    ("found", 200), ("still", 195), ("between", 190), ("name", 185), ("should", 180),
    ("home", 175), ("big", 170), ("give", 165), ("air", 160), ("line", 155),
    ("set", 150), ("own", 145), ("under", 140), ("read", 135), ("last", 130),
    ("never", 125), ("us", 120), ("left", 115), ("end", 110), ("along", 105),
    ("while", 100), ("might", 98), ("next", 96), ("sound", 94), ("below", 92),
    ("saw", 90), ("something", 88), ("thought", 86), ("both", 84), ("few", 82),
    ("those", 80), ("always", 78), ("looked", 76), ("show", 74), ("large", 72),
    ("often", 70), ("together", 68), ("asked", 66), ("house", 64), ("don't", 62),
    ("world", 60), ("going", 58), ("want", 56), ("school", 54), ("important", 52),
    ("until", 50), ("form", 49), ("food", 48), ("keep", 47), ("children", 46),
    ("feet", 45), ("land", 44), ("side", 43), ("without", 42), ("boy", 41),
    ("once", 40), ("animal", 39), ("life", 38), ("enough", 37), ("took", 36),
    ("four", 35), ("head", 34), ("above", 33), ("kind", 32), ("begin", 31),
    ("almost", 30), ("live", 29), ("page", 28), ("got", 27), ("began", 26),
    ("grow", 25), ("cut", 24), ("knew", 23), ("earth", 22), ("father", 21),
    ("stand", 19), ("country", 15), ("answer", 13), ("study", 10), ("learn", 8),
    ("plant", 7), ("cover", 6), ("sun", 4), ("let", 1), ("eye", 99), ("door", 96),
    ("city", 94), ("tree", 93), ("cross", 92), ("since", 91), ("hard", 90),
    ("start", 89), ("story", 87), ("far", 85), ("sea", 84), ("draw", 83),
    ("late", 81), ("run", 80), ("press", 77), ("close", 76), ("night", 75),
    ("real", 74), ("north", 71), ("open", 70), ("seem", 69), ("white", 66),
    ("walk", 62), ("example", 61), ("ease", 60), ("paper", 59), ("group", 58),
    ("music", 56), ("mark", 53), ("letter", 51), ("mile", 49), ("river", 48),
    ("car", 47), ("care", 45), ("second", 44), ("book", 43), ("carry", 42),
    ("science", 40), ("eat", 39), ("room", 38), ("friend", 37), ("idea", 35),
    ("fish", 34), ("mountain", 33), ("stop", 32), ("base", 30), ("hear", 29),
    ("horse", 28), ("sure", 26), ("watch", 25), ("color", 24), ("face", 23),
    ("wood", 22), ("main", 21), ("plain", 19), ("girl", 18), ("usual", 17),
    ("young", 16), ("ready", 15), ("ever", 13), ("red", 12), ("list", 11),
    ("though", 10), ("feel", 9), ("talk", 8), ("bird", 7), ("soon", 6),
    ("body", 5), ("dog", 4), ("family", 3), ("direct", 2), ("pose", 1),
    ("leave", 100), ("song", 99), ("measure", 98), ("product", 96), ("black", 95),
    ("short", 94), ("numeral", 93), ("class", 92), ("wind", 91), ("question", 90),
    ("happen", 89), ("complete", 88), ("ship", 87), ("area", 86), ("half", 85),
    ("rock", 84), ("order", 83), ("fire", 82), ("south", 81), ("problem", 80),
    ("piece", 79), ("told", 78), ("pass", 76), ("top", 74), ("whole", 73),
    ("king", 72), ("space", 71), ("heard", 70), ("best", 69), ("hour", 68),
    ("better", 67), ("during", 66), ("hundred", 65), ("five", 64), ("remember", 63),
    ("step", 62), ("early", 61), ("hold", 60), ("west", 59), ("ground", 58),
    ("interest", 57), ("reach", 56), ("fast", 55), ("verb", 54), ("sing", 53),
    ("listen", 52), ("six", 51), ("table", 50), ("travel", 49), ("less", 48),
    ("morning", 47), ("ten", 46), ("simple", 45), ("several", 44), ("vowel", 43),
    ("toward", 42), ("war", 41), ("lay", 40), ("against", 39), ("pattern", 38),
    ("slow", 37), ("center", 36), ("love", 35), ("person", 34), ("money", 33),
    ("serve", 32), ("appear", 31), ("road", 30), ("map", 29), ("rain", 28),
    ("rule", 27), ("govern", 26), ("pull", 25), ("cold", 24), ("notice", 23),
    ("voice", 22), ("unit", 21), ("power", 20), ("town", 19), ("fine", 18),
    ("certain", 17), ("fly", 16), ("fall", 15), ("lead", 14), ("cry", 13),
    ("dark", 12), ("machine", 11), ("note", 10), ("wait", 9), ("plan", 8),
    ("figure", 7), ("star", 6), ("box", 5), ("noun", 4), ("field", 3),
    ("rest", 2), ("correct", 1), ("able", 100), ("pound", 99), ("done", 98),
    ("beauty", 97), ("drive", 96), ("stood", 95), ("contain", 94), ("front", 93),
    ("teach", 92), ("week", 91), ("final", 90), ("gave", 89), ("green", 88),
    ("oh", 87), ("quick", 86), ("develop", 85), ("ocean", 84), ("warm", 83),
    ("free", 82), ("minute", 81), ("strong", 80), ("special", 79), ("mind", 78),
    ("behind", 77), ("clear", 76), ("tail", 75), ("produce", 74), ("fact", 73),
    ("street", 72), ("inch", 71), ("multiply", 70), ("nothing", 69), ("course", 68),
    ("stay", 67), ("wheel", 66), ("full", 65), ("force", 64), ("blue", 63),
    ("object", 62), ("decide", 61), ("surface", 60), ("deep", 59), ("moon", 58),
    ("island", 57), ("foot", 56), ("system", 55), ("busy", 54), ("test", 53),
    ("record", 52), ("boat", 51), ("common", 50), ("gold", 49), ("possible", 48),
    ("plane", 47), ("stead", 46), ("dry", 45), ("wonder", 44), ("laugh", 43),
    ("thousand", 42), ("ago", 41), ("ran", 40), ("check", 39), ("game", 38),
    ("shape", 37), ("equate", 36), ("hot", 35), ("miss", 34), ("brought", 33),
    ("heat", 32), ("snow", 31), ("tire", 30), ("bring", 29), ("yes", 28),
    ("distant", 27), ("fill", 26), ("east", 25), ("paint", 24), ("language", 23),
    ("among", 22), ("grand", 21), ("ball", 20), ("yet", 19), ("wave", 18),
    ("drop", 17), ("heart", 16), ("am", 15), ("present", 14), ("heavy", 13),
    ("dance", 12), ("engine", 11), ("position", 10), ("arm", 9), ("wide", 8),
    ("sail", 7), ("material", 6), ("size", 5), ("vary", 4), ("settle", 3),
    ("speak", 2), ("weight", 1),
]


def load_words_from_csv(filepath: str) -> List[Tuple[str, int]]:
    """Load words from CSV."""
    words = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            first_row = next(reader, None)
            if first_row and len(first_row) == 2:
                try:
                    int(first_row[1])
                    words.append((first_row[0].lower().strip(), int(first_row[1])))
                except ValueError:
                    pass
            for row in reader:
                if len(row) >= 2:
                    try:
                        word = row[0].lower().strip()
                        frequency = int(row[1])
                        if word and frequency > 0:
                            words.append((word, frequency))
                    except (ValueError, IndexError):
                        continue
    except FileNotFoundError:
        return []
    except Exception:
        return []
    return words


def try_load_nltk() -> List[Tuple[str, int]]:
    """Try to load words from NLTK corpus."""
    try:
        import nltk
        from nltk.corpus import words as nltk_words
        try:
            nltk.data.find('corpora/words')
        except LookupError:
            nltk.download('words', quiet=True)
        word_list = nltk_words.words()
        return [(word.lower(), max(100, 10000 - i * 10)) for i, word in enumerate(word_list[:5000])]
    except ImportError:
        return []
    except Exception:
        return []


def load_words(filepath: Optional[str] = None) -> List[Tuple[str, int]]:
    """Load words with fallback: CSV -> NLTK -> Embedded."""
    if filepath:
        csv_words = load_words_from_csv(filepath)
        if csv_words:
            return csv_words
    nltk_words = try_load_nltk()
    if nltk_words:
        return nltk_words
    return FALLBACK_WORDS.copy()


def save_words_to_csv(words: List[Tuple[str, int]], filepath: str) -> bool:
    """Save words to CSV."""
    try:
        with open(filepath, 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['word', 'frequency'])
            for word, freq in words:
                writer.writerow([word, freq])
        return True
    except Exception:
        return False


def create_default_csv(filepath: str) -> bool:
    """Create default CSV with fallback words."""
    return save_words_to_csv(FALLBACK_WORDS, filepath)
