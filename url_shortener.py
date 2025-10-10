#!/usr/bin/env python3
"""
A simple script that accepts a long URL from the user and attempts to
create a shortened URL that forwards to the same destination.  It uses
several free shortening services via the `pyshorteners` library.  The
script will try each service in turn until a shortened URL not exceeding
50 characters is produced.  If none of the services return a URL within
this length, the script raises an error.  For services requiring API
keys (such as Bitly), you can extend the `services` list with the
appropriate initialisation and API key.

Usage::

    python3 url_shortener.py

You'll be prompted to enter the long URL.  The resulting short URL
(50 characters or fewer) will be printed on success.
"""
from __future__ import annotations

import sys

try:
    import pyshorteners  # type: ignore
except ImportError:  # pragma: no cover - guidance for the user, not testable here.
    sys.stderr.write(
        "The pyshorteners library is required. Install it with 'pip install pyshorteners'.\n"
    )
    raise


def shorten_url(long_url: str, max_length: int = 50) -> str:
    """Attempt to shorten ``long_url`` to within ``max_length`` characters.

    Tries multiple shortening services provided by the ``pyshorteners``
    library.  Returns the first shortened URL whose length is at most
    ``max_length``.  Raises ``ValueError`` if no such URL can be
    produced.

    :param long_url: The URL to shorten.
    :param max_length: Maximum allowed length of the resulting URL.
    :return: A shortened URL forwarding to ``long_url``.
    :raises ValueError: If none of the services return a short enough URL.
    """
    # Normalise scheme – some services require a scheme to be present
    if not long_url.startswith(("http://", "https://")):
        long_url = "http://" + long_url

    shortener = pyshorteners.Shortener()

    # Define a list of (service_name, callable) pairs.  Each callable
    # must accept the long URL and return a shortened URL string.
    services = [
        ("TinyURL", shortener.tinyurl.short),
        ("Is.gd", shortener.isgd.short),
        ("Da.gd", shortener.dagd.short),
        ("Clck.ru", shortener.clckru.short),
        ("Chilpit", shortener.chilpit.short),
    ]

    attempted_services = []

    for name, shortener_fn in services:
        attempted_services.append(name)
        try:
            shortened = shortener_fn(long_url)
        except Exception:
            # Skip this service if an exception occurs (e.g., network error or
            # service-specific limitation).  Continue to the next one.
            continue
        if len(shortened) <= max_length:
            return shortened

    raise ValueError(
        f"None of the shortening services returned a URL within {max_length} characters"
        f" after trying: {', '.join(attempted_services)}."
    )



def main() -> None:
    """Prompt the user for a URL and print the shortened version."""
    long_url = input("Enter the URL to shorten: ").strip()
    try:
        short_url = shorten_url(long_url)
        print(f"Shortened URL: {short_url}")
    except ValueError as exc:
        print(f"Failed to shorten URL: {exc}")


if __name__ == "__main__":
    main()
