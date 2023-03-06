import re
from collections.abc import Sequence

from humps import camelize


class Camelizer:
    """
    >>> camelizer = Camelizer(["url", "ip"])
    >>> camelizer("redirect_url")
    'redirectURL'
    >>> camelizer("server_ip")
    'serverIP'
    >>> camelizer("py_humps_is_great")
    'pyHumpsIsGreat'
    >>> camelizer("ip_first")
    'ipFirst'
    >>> camelizer("the_girl_from_ipanema")
    'theGirlFromIpanema'
    """

    def __init__(self, initialisms: Sequence[str]):
        self._initialisms = [re.compile(rf'_{i}(?:[^a-zA-Z0-9]|$)') for i in initialisms]

    def __call__(self, v: str) -> str:
        for i in self._initialisms:
            for m in i.finditer(v):
                v = f'{v[:m.start()]}{v[m.start():m.end()].upper()}{v[m.end():]}'
        return camelize(v)
