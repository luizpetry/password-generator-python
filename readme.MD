# Password Generator (Gerador de Senhas)

Projeto Python completo com:
- gerador de senhas aleatórias e passphrases
- verificador de força de senha
- histórico local por usuário (session + arquivo JSON)
- interface web elegante com Flask
- suporte a opções avançadas (caracteres, exclusão de ambiguidades, palavra personalizada, shuffle)
- botão copiar com fallback confiável

## Arquivos principais

- `generator.py`: lógica de geração de senha e passphrase usando `secrets`.
- `checker.py`: avalia força com regra customizada e retorna etiqueta + cor.
- `history.py`: lê/grava histórico JSON em `history.json` por `user_id` de sessão.
- `main.py`: modo de linha de comando interativo + args para uso CLI.
- `app.py`: servidor Flask com rota `/`, validação de formulário, controle de política e persistência em `session`.
- `templates/index.html`: UI com formulário, resultados, histórico e JS para copiar senha.
- `static/style.css`: estilo visual separado
- `requirements.txt`: dependências (`Flask`, `rich`, `pyperclip` se precisar)

## Como usar localmente

1. Crie e ative um ambiente virtual:
   - Windows (PowerShell):
     ```powershell
     python -m venv .venv
     .\.venv\Scripts\Activate.ps1
     ```
2. Instale dependências:
   ```bash
   pip install -r requirements.txt
   ```
3. Execute o servidor:
   ```bash
   python app.py
   ```
4. Abra `http://127.0.0.1:5000` no navegador.

## Funcionalidades da interface

- `Comprimento`: tamanho da senha (mínimo 4, padrão 16).
- `Quantidade`: número de senhas a gerar.
- `Maiúsculas`, `Minúsculas`, `Números`, `Símbolos`, `Excluir ambíguos`.
- `Incluir palavra personalizada`: anexa texto e pode embaralhar.
- `Embaralhar senha final` (recomendada para melhor aleatoriedade).
- Resultado mostra força e cor (Muito Fraca/Muito Forte etc).
- Botão `Copiar` copia senha para a área de transferência (ou prompt fallback).
- Histórico com última geração de senha salvo por navegador/usuário.

## Heurísticas de segurança

- Senhas geradas com `secrets.choice` (cryptographic randomness).
- `exclude_ambiguous` removes characters like `l`, `1`, `O`, `0`.
- `check_char_policy` garante consistência desejada (sem números/símbolos indesejados).

## Pontos de melhoria futura

- autenticação de usuário e histórico multi-digit
- endpoints API JSON para geração remota
- testes unitários automatizados (`pytest`)
- suporte a temas escuro/claro persistentes

## Licença

- MIT Luiz Petry.
