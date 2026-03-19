import argparse
import sys

from rich import box
from rich.console import Console
from rich.table import Table

from generator import generate_password, generate_passphrase
from checker import display_strength
from history import save, load, display_history

try:
    import pyperclip
    has_pyperclip = True
except ImportError:
    has_pyperclip = False


def main():
    parser = argparse.ArgumentParser(description='Gerador de Senhas Configurável')
    parser.add_argument('-c', '--comprimento', type=int, default=16, help='Comprimento da senha (padrão 16)')
    parser.add_argument('--sem-maiusculas', action='store_true', help='Não incluir letras maiúsculas')
    parser.add_argument('--sem-minusculas', action='store_true', help='Não incluir letras minúsculas')
    parser.add_argument('--sem-numeros', action='store_true', help='Não incluir números')
    parser.add_argument('--sem-simbolos', action='store_true', help='Não incluir símbolos')
    parser.add_argument('--excluir-ambiguos', action='store_true', help='Excluir caracteres ambíguos')
    parser.add_argument('-q', '--quantidade', type=int, default=1, help='Quantidade de senhas a gerar')
    parser.add_argument('--frase', action='store_true', help='Gerar frase-senha em vez de senha aleatória')
    parser.add_argument('--historico', action='store_true', help='Exibir histórico de senhas geradas')
    parser.add_argument('--clipboard', action='store_true', help='Copiar última senha gerada para o clipboard')

    args = parser.parse_args()
    console = Console()

    if args.historico:
        display_history(limit=20)
        return

    if args.frase:
        passwords = [generate_passphrase(args.quantidade)]
    else:
        if args.quantidade <= 0:
            console.print('[red]A quantidade deve ser um número inteiro positivo.[/red]')
            sys.exit(1)

        passwords = []
        for _ in range(args.quantidade):
            try:
                pwd = generate_password(
                    length=args.comprimento,
                    uppercase=not args.sem_maiusculas,
                    lowercase=not args.sem_minusculas,
                    numbers=not args.sem_numeros,
                    symbols=not args.sem_simbolos,
                    exclude_ambiguous=args.excluir_ambiguos,
                )
                passwords.append(pwd)
            except ValueError as e:
                console.print(f'[red]Erro: {str(e)}[/red]')
                sys.exit(1)

    table = Table(title='Senhas Geradas', box=box.ROUNDED)
    table.add_column('#', justify='right')
    table.add_column('Senha', style='cyan')
    table.add_column('Força', style='magenta')

    for i, pwd in enumerate(passwords, 1):
        strength = display_strength(pwd)
        table.add_row(str(i), pwd, strength)

        criteria = {
            'comprimento': args.comprimento,
            'uppercase': not args.sem_maiusculas,
            'lowercase': not args.sem_minusculas,
            'numbers': not args.sem_numeros,
            'symbols': not args.sem_simbolos,
            'exclude_ambiguous': args.excluir_ambiguos,
            'frase': args.frase,
        }

        try:
            save(pwd, criteria)
        except Exception as e:
            console.print(f'[yellow]Aviso: não foi possível salvar histórico ({e}).[/yellow]')

    console.print(table)

    if args.clipboard:
        if not has_pyperclip:
            console.print('[red]pyperclip não está instalado. Instale com pip install pyperclip.[/red]')
        else:
            try:
                pyperclip.copy(passwords[-1])
                console.print('[green]Última senha copiada para o clipboard.[/green]')
            except Exception as e:
                console.print(f'[red]Erro ao copiar para clipboard: {e}[/red]')


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('\nOperação cancelada pelo usuário.')
        sys.exit(0)
