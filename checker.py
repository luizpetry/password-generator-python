import re


def check_strength(password):
    """Verifica a força da senha e retorna texto descritivo."""
    if not isinstance(password, str):
        raise ValueError("A senha deve ser uma string.")

    score = 0
    if len(password) >= 8:
        score += 1
    if len(password) >= 16:
        score += 1
    if re.search(r'[A-Z]', password):
        score += 1
    if re.search(r'[a-z]', password):
        score += 1
    if re.search(r'[0-9]', password):
        score += 1
    if re.search(r'[!"#\$%&\'\(\)\*\+,\-\./:;<=>\?@\[\\\]\^_`\{\|\}~]', password):
        score += 1

    if score <= 1:
        return 'Muito Fraca'
    if score == 2:
        return 'Fraca'
    if score == 3:
        return 'Média'
    if score == 4:
        return 'Boa'
    if score == 5:
        return 'Forte'
    return 'Muito Forte'


def display_strength(password):
    """Retorna uma representação de força com barra em texto e nível."""
    score = 0
    if len(password) >= 8:
        score += 1
    if len(password) >= 16:
        score += 1
    if re.search(r'[A-Z]', password):
        score += 1
    if re.search(r'[a-z]', password):
        score += 1
    if re.search(r'[0-9]', password):
        score += 1
    if re.search(r'[!"#\$%&\'\(\)\*\+,\-\./:;<=>\?@\[\\\]\^_`\{\|\}~]', password):
        score += 1

    level = check_strength(password)
    total = 6
    filled = '#' * score
    empty = ' ' * (total - score)
    bar = f'[{filled}{empty}]'
    return f"{bar} {level}"
