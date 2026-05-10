from functools import lru_cache

from dns.exception import DNSException
from dns.resolver import resolve

CONSUMER_DOMAINS: frozenset[str] = frozenset(['gmail.com', 'googlemail.com'])
GOOGLE_INDICATORS: frozenset[str] = frozenset(['google.com', 'googlemail.com'])


@lru_cache(maxsize=1024)
def _is_google_domain_domain(domain: str) -> bool:
    if domain in CONSUMER_DOMAINS:
        return True
    try:
        return any(
            any(indicator in exchange for indicator in GOOGLE_INDICATORS)
            for exchange in [str(rdata.exchange).lower() for rdata in resolve(domain, 'MX')]
        )
    except DNSException:
        return False


def is_google_domain(email: str) -> bool:
    return _is_google_domain_domain(email.split('@')[-1].lower())
