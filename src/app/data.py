"""Erfundene Beispieldaten: Urlaubstage je Person (Schlüssel ist `user.sub`)."""

from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class Urlaubstag:
    datum: date
    grund: str


_URLAUBSTAGE: dict[str, list[Urlaubstag]] = {
    "student-test": [
        Urlaubstag(date(2026, 12, 23), "Weihnachtsurlaub"),
        Urlaubstag(date(2026, 12, 28), "Weihnachtsurlaub"),
        Urlaubstag(date(2026, 12, 29), "Weihnachtsurlaub"),
        Urlaubstag(date(2027, 2, 15), "Erholungsurlaub"),
        Urlaubstag(date(2027, 2, 16), "Erholungsurlaub"),
        Urlaubstag(date(2027, 4, 6), "Osterferien"),
        Urlaubstag(date(2027, 7, 12), "Sommerurlaub"),
    ],
    "student-empty": [
        Urlaubstag(date(2027, 3, 1), "Umzug"),
    ],
}


def urlaubstage_von(sub: str) -> list[Urlaubstag]:
    """Nur die Urlaubstage der angemeldeten Person, nach Datum sortiert."""
    return sorted(_URLAUBSTAGE.get(sub, []), key=lambda tag: tag.datum)
