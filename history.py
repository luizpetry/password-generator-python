import json
from datetime import datetime

HISTORY_FILE = 'history.json'


def save(password, criteria, user_id=None):
    """Salva entrada de senha e critérios no histórico."""
    try:
        data = load()
    except Exception:
        data = []

    item = {
        'timestamp': datetime.now().isoformat(),
        'password': password,
        'criteria': criteria,
        'user_id': user_id,
    }
    data.append(item)

    with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def load():
    """Carrega histórico do arquivo ou retorna lista vazia se não existir."""
    try:
        with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []


def display_history(limit=10):
    """Imprime últimas N entradas do histórico."""
    data = load()
    if not data:
        print("Nenhum histórico encontrado.")
        return

    subset = data[-limit:]
    for idx, item in enumerate(reversed(subset), 1):
        print(f"{idx}. {item['timestamp']} - {item['password']} - {item['criteria']}")
