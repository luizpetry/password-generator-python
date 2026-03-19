import secrets
import string

AMBIGUOUS_CHARS = "0O1Il"


def generate_password(length=12, uppercase=True, lowercase=True, numbers=True, symbols=True, exclude_ambiguous=False):
    """Gera uma senha criptograficamente segura.

    Args:
        length (int): comprimento da senha (pelo menos 1).
        uppercase (bool): incluir letras maiúsculas.
        lowercase (bool): incluir letras minúsculas.
        numbers (bool): incluir dígitos.
        symbols (bool): incluir símbolos.
        exclude_ambiguous (bool): remover caracteres ambíguos.

    Returns:
        str: senha gerada.

    Raises:
        ValueError: se nenhum tipo de caractere for selecionado ou length inválido.
    """
    if length <= 0:
        raise ValueError("O comprimento da senha deve ser um número inteiro positivo.")

    charset = ""
    if uppercase:
        charset += string.ascii_uppercase
    if lowercase:
        charset += string.ascii_lowercase
    if numbers:
        charset += string.digits
    if symbols:
        charset += string.punctuation

    if not charset:
        raise ValueError("Ao menos um tipo de caractere deve ser selecionado para gerar a senha.")

    if exclude_ambiguous:
        charset = ''.join(c for c in charset if c not in AMBIGUOUS_CHARS)

    if not charset:
        raise ValueError("Não há caracteres disponíveis após a exclusão de ambíguos.")

    # Garantir pelo menos um caractere de cada categoria selecionada para melhor segurança
    caracteres_escolhidos = []
    if uppercase:
        allowed = string.ascii_uppercase
        if exclude_ambiguous:
            allowed = ''.join(c for c in allowed if c not in AMBIGUOUS_CHARS)
        caracteres_escolhidos.append(secrets.choice(allowed))
    if lowercase:
        allowed = string.ascii_lowercase
        if exclude_ambiguous:
            allowed = ''.join(c for c in allowed if c not in AMBIGUOUS_CHARS)
        caracteres_escolhidos.append(secrets.choice(allowed))
    if numbers:
        allowed = string.digits
        if exclude_ambiguous:
            allowed = ''.join(c for c in allowed if c not in AMBIGUOUS_CHARS)
        caracteres_escolhidos.append(secrets.choice(allowed))
    if symbols:
        allowed = string.punctuation
        if exclude_ambiguous:
            allowed = ''.join(c for c in allowed if c not in AMBIGUOUS_CHARS)
        caracteres_escolhidos.append(secrets.choice(allowed))

    # Se o comprimento for menor que o número de categorias exigidas, reduzir reforço mínimo
    if len(caracteres_escolhidos) > length:
        caracteres_escolhidos = caracteres_escolhidos[:length]

    # Completa com caracteres aleatórios do conjunto principal
    while len(caracteres_escolhidos) < length:
        caracteres_escolhidos.append(secrets.choice(charset))

    # Embaralha para evitar padrões previsíveis
    secrets.SystemRandom().shuffle(caracteres_escolhidos)
    return ''.join(caracteres_escolhidos)


def generate_passphrase(num_words=4):
    """Gera uma frase-senha estilo palavra-palavra, usando lista de palavras em português."""
    if num_words <= 0:
        raise ValueError("O número de palavras deve ser inteiro positivo.")

    palavras = [
        "sol", "lua", "estrela", "vento", "mar", "terra", "fogo", "verde", "rio", "casa",
        "tempo", "sonho", "vida", "flor", "paz", "sombra", "luz", "caminho", "amigo", "sorriso",
        "alegria", "trabalho", "cidade", "vortex", "rua", "praia", "harpa", "safira", "gemida", "historia"
    ]

    frase = [secrets.choice(palavras) for _ in range(num_words)]
    return '-'.join(frase)
