import re
from collections.abc import Sequence

from humps import camelize, decamelize


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


class Decamelizer:
    """
    >>> decamelizer = Decamelizer(["URL", "IP"])
    >>> decamelizer("redirectURL")
    'redirect_url'
    >>> decamelizer("serverIP")
    'server_ip'
    >>> decamelizer("pyHumpsIsGreat")
    'py_humps_is_great'
    >>> decamelizer("IPFirst")
    'ip_first'
    >>> decamelizer("theGirlFromIpanema")
    'the_girl_from_ipanema'
    """

    def __init__(self, initialisms: Sequence[str]):
        self._initialisms = [re.compile(rf'{i}(?:[^a-zA-Z0-9]|$)', re.IGNORECASE) for i in initialisms]

    def __call__(self, v: str) -> str:
        v = decamelize(v)
        for i in self._initialisms:
            for m in i.finditer(v):
                v = f'{v[:m.start()]}{v[m.start():m.end()].lower()}{v[m.end():]}'
        return v


initialisms = ["url", "ip", "id"]
camelizer = Camelizer(initialisms=initialisms)
decamelizer = Decamelizer(initialisms=initialisms)
