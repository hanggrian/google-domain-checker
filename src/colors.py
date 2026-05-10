from colorama import Fore, Style


def green(content: str) -> str:
    return f'{Fore.GREEN}{content}{Style.RESET_ALL}'


def red(content: str) -> str:
    return f'{Fore.RED}{content}{Style.RESET_ALL}'


def yellow(content: str) -> str:
    return f'{Fore.YELLOW}{content}{Style.RESET_ALL}'


def b(content: str) -> str:
    return f'{Style.BRIGHT}{content}{Style.RESET_ALL}'
