from flask import Flask, render_template, request, redirect, url_for, flash, session
import uuid
import string

from generator import generate_password, generate_passphrase
from checker import display_strength
from history import save, load

app = Flask(__name__)
app.secret_key = 'changeme_please_use_secure_key'


def get_strength_color(level):
    mapping = {
        'Muito Fraca': '#ef4444',  # vermelho
        'Fraca': '#f97316',       # laranja
        'Média': '#facc15',       # amarelo
        'Boa': '#22c55e',         # verde claro
        'Forte': '#16a34a',       # verde escuro
        'Muito Forte': '#0284c7', # azul
    }
    return mapping.get(level, '#94a3b8')


def check_char_policy(password, uppercase, lowercase, numbers, symbols):
    """Verifica se a senha está de acordo com as opções selecionadas."""
    if uppercase and not any(c.isupper() for c in password):
        return False
    if lowercase and not any(c.islower() for c in password):
        return False
    if not numbers and any(c.isdigit() for c in password):
        return False
    if numbers and not any(c.isdigit() for c in password):
        return False
    if not symbols and any(c in string.punctuation for c in password):
        return False
    if symbols and not any(c in string.punctuation for c in password):
        return False
    return True


@app.route('/', methods=['GET', 'POST'])
def index():
    if 'user_id' not in session:
        session['user_id'] = str(uuid.uuid4())

    user_id = session['user_id']
    results = []
    history = [h for h in load() if h.get('user_id') == user_id]

    # Padrões das preferências do formulário (guardado por session/browser)
    default_prefs = {
        'comprimento': 16,
        'quantidade': 1,
        'uppercase': True,
        'lowercase': True,
        'numbers': True,
        'symbols': True,
        'exclude_ambiguous': False,
        'include_word_enabled': False,
        'include_word': '',
        'include_shuffle': False,
    }

    prefs = session.get('prefs', default_prefs.copy())

    if request.method == 'POST':
        include_word_enabled = request.form.get('include_word_enabled') == 'on'
        include_word = request.form.get('include_word', '').strip() if include_word_enabled else ''
        include_shuffle = request.form.get('include_shuffle') == 'on'
        quantidade = int(request.form.get('quantidade', 1))
        comprimento = int(request.form.get('comprimento', 16))
        uppercase = request.form.get('uppercase') == 'on'
        lowercase = request.form.get('lowercase') == 'on'
        numbers = request.form.get('numbers') == 'on'
        symbols = request.form.get('symbols') == 'on'
        exclude_ambiguous = request.form.get('exclude_ambiguous') == 'on'

        prefs = {
            'comprimento': comprimento,
            'quantidade': quantidade,
            'uppercase': uppercase,
            'lowercase': lowercase,
            'numbers': numbers,
            'symbols': symbols,
            'exclude_ambiguous': exclude_ambiguous,
            'include_word_enabled': include_word_enabled,
            'include_word': include_word,
            'include_shuffle': include_shuffle,
        }

        session['prefs'] = prefs

        try:
            quantidade = int(request.form.get('quantidade', 1))
            if quantidade <= 0:
                raise ValueError('Quantidade deve ser positiva.')
        except ValueError:
            flash('Quantidade inválida. Informe um número inteiro positivo.', 'danger')
            return redirect(url_for('index'))

        try:
            comprimento = int(request.form.get('comprimento', 16))
            if comprimento <= 0:
                raise ValueError('Comprimento deve ser positivo.')
        except ValueError:
            flash('Comprimento inválido. Informe um número inteiro positivo.', 'danger')
            return redirect(url_for('index'))

        if include_word_enabled and not include_word:
            flash('Desative "Incluir palavra personalizada" ou escreva alguma palavra no campo acima.', 'danger')
            return redirect(url_for('index'))

        if include_word and len(include_word) > comprimento:
            flash('A palavra incluída não pode ser maior que comprimento total.', 'danger')
            return redirect(url_for('index'))

        if not any([uppercase, lowercase, numbers, symbols]):
            flash('Selecione pelo menos um tipo de caractere.', 'danger')
            return redirect(url_for('index'))

        if not any([uppercase, lowercase, numbers, symbols]):
            flash('Selecione pelo menos um tipo de caractere.', 'danger')
            return redirect(url_for('index'))

        for _ in range(quantidade):
            if include_word:
                restante = comprimento - len(include_word)
                if restante < 0:
                    flash('A palavra incluída não pode ser maior que comprimento total.', 'danger')
                    return redirect(url_for('index'))
                if restante == 0:
                    senha = include_word
                else:
                    complemento = generate_password(
                        length=restante,
                        uppercase=uppercase,
                        lowercase=lowercase,
                        numbers=numbers,
                        symbols=symbols,
                        exclude_ambiguous=exclude_ambiguous,
                    )
                    senha = include_word + complemento
            else:
                senha = generate_password(
                    length=comprimento,
                    uppercase=uppercase,
                    lowercase=lowercase,
                    numbers=numbers,
                    symbols=symbols,
                    exclude_ambiguous=exclude_ambiguous,
                )

            # Embaralha senha resultante para aumentar aleatoriedade, mantendo palavra inclusa em qualquer posição
            if include_shuffle and include_word:
                chars = list(senha)
                # Preserve presença da palavra por contagem, não necessariamente por bloco contíguo
                import secrets as _secrets
                _secrets.SystemRandom().shuffle(chars)
                senha = ''.join(chars)

            # Verificação adicional: não deve conter dígitos ou símbolos se não selecionados.
            if not check_char_policy(senha, uppercase, lowercase, numbers, symbols):
                # Regerar se encontrar elementos fora da política selecionada.
                for i in range(10):
                    if include_word:
                        restante = comprimento - len(include_word)
                        if restante <= 0:
                            senha = include_word
                        else:
                            complemento = generate_password(
                                length=restante,
                                uppercase=uppercase,
                                lowercase=lowercase,
                                numbers=numbers,
                                symbols=symbols,
                                exclude_ambiguous=exclude_ambiguous,
                            )
                            senha = include_word + complemento
                        if include_shuffle:
                            chars = list(senha)
                            import secrets as _secrets
                            _secrets.SystemRandom().shuffle(chars)
                            senha = ''.join(chars)
                    else:
                        senha = generate_password(
                            length=comprimento,
                            uppercase=uppercase,
                            lowercase=lowercase,
                            numbers=numbers,
                            symbols=symbols,
                            exclude_ambiguous=exclude_ambiguous,
                        )
                    if check_char_policy(senha, uppercase, lowercase, numbers, symbols):
                        break

            forca = display_strength(senha)
            results.append({'value': senha, 'strength': forca, 'color': get_strength_color(forca)})
            save(senha, {
                'mode': 'senha',
                'comprimento': comprimento,
                'uppercase': uppercase,
                'lowercase': lowercase,
                'numbers': numbers,
                'symbols': symbols,
                'exclude_ambiguous': exclude_ambiguous,
                'include_word': include_word if include_word_enabled else '',
                'include_shuffle': include_shuffle,
            }, user_id=user_id)

        history = [h for h in load() if h.get('user_id') == user_id]

    return render_template('index.html', results=results, history=history, prefs=prefs)


if __name__ == '__main__':
    app.run(debug=True)
