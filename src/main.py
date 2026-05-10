from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import as_completed
from csv import DictReader, DictWriter
from os import cpu_count
from pathlib import Path
from re import Pattern, compile as re
from sys import argv, exit as exit2

from checker import is_google_domain
from colors import green, red, yellow

EMAIL_REGEX: Pattern = re('^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$')


def check() -> None:
    input_args: list[str] = argv[1:]
    if not input_args:
        print(red('No input.'))
        exit2(1)
    for arg in input_args:
        if not EMAIL_REGEX.match(arg):
            print(f"{arg}: {red('bad format')}")
            exit2(1)
        print(f'{arg}: {green('yes') if is_google_domain(arg) else yellow('no')}')


def convert() -> None:
    input_args: list[str] = argv[1:]
    if len(input_args) != 1:
        print(red('Expect one argument.'))
        exit2(1)
    input_path: Path = Path(input_args[0])
    print(f'Loading {input_path.name}.')
    with input_path.open(newline='', encoding='UTF-8') as input_file:
        reader: DictReader[str] = DictReader(input_file)
        if not reader.fieldnames:
            return
        fieldnames: list[str] = [fieldname.upper() for fieldname in reader.fieldnames]
        if 'EMAIL' not in fieldnames:
            print(red('Missing EMAIL column.'))
            exit2(1)
        rows: list[dict[str, str]] = [
            {fieldname.upper(): value for fieldname, value in row.items()}
            for row in reader
        ]
    unique_domains: list[str] = \
        sorted({row.get('EMAIL', '').split('@')[-1].lower() for row in rows})
    worker_count: int = min(len(unique_domains), cpu_count() or 1)
    print(f'Processing {len(rows)} row(s) across {worker_count} worker(s).')
    domain_results: dict[str, bool] = {}
    if unique_domains:
        with ThreadPoolExecutor(max_workers=worker_count) as executor:
            futures = {
                executor.submit(is_google_domain, domain): domain
                for domain in unique_domains
            }
            resolved_count: int = 0
            for future in as_completed(futures):
                domain_results[futures[future]] = future.result()
                resolved_count += 1
                print(f'Resolved {resolved_count}/{len(unique_domains)} unique domain(s).')
    with input_path.open('w', newline='', encoding='UTF-8') as output_file:
        writer: DictWriter[str] = DictWriter(output_file, fieldnames=[*fieldnames, 'GOOGLE'])
        writer.writeheader()
        for row_number, row in enumerate(rows, start=1):
            email_domain: str = row.get('EMAIL', '').split('@')[-1].lower()
            writer.writerow({
                **row,
                'GOOGLE': 'Yes' if domain_results.get(email_domain, False) else 'No',
            })
            print(f'Processed {row_number}/{len(rows)} row(s).')
    print(green('Done.'))
