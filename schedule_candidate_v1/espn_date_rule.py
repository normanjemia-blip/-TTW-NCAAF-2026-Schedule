#!/usr/bin/env python3
"""CANONICAL DATE SEMANTICS for the TTW schedule — the permanent ingestion rule.

This module is the single source of truth for how an ESPN event becomes a
`start_date`. Import it from any extractor or refresh job. It is pure: no I/O,
no network, no globals.

    CANONICAL DEFINITION
    --------------------
    `start_date` is the calendar date on which the game is played IN THE
    TIME ZONE OF ITS VENUE.

    It is NOT the UTC date, and NOT the US/Eastern date.

Why this matters: ESPN publishes the kickoff as an instant in UTC. Taking
`.date()` off that instant stores the UTC day, which rolls forward for any
kickoff after roughly 20:00 US/Eastern. That defect put 133 of 888 games one
day late and invented 67 Sunday games that are really Saturday games.

    THE TWO CASES
    -------------
    timeValid = True   the kickoff instant is real.
                       start_date = kickoff.astimezone(venue_zone).date()

    timeValid = False  ESPN has no announced kickoff and encodes the row as
                       MIDNIGHT US/EASTERN. That instant is a placeholder, not
                       a kickoff. Converting it into a western venue zone would
                       fabricate a 23:00 game on the PREVIOUS day.
                       start_date = kickoff.astimezone(US/Eastern).date()

                       Such a row MUST be re-derived once a real kickoff time is
                       published. `needs_rederivation()` marks them.
"""
from zoneinfo import ZoneInfo

EASTERN = ZoneInfo("America/New_York")

STATE_TZ = {
    "AL": "America/Chicago", "AR": "America/Chicago", "AZ": "America/Phoenix",
    "CA": "America/Los_Angeles", "CO": "America/Denver", "CT": "America/New_York",
    "DE": "America/New_York", "FL": "America/New_York", "GA": "America/New_York",
    "HI": "Pacific/Honolulu", "IA": "America/Chicago", "ID": "America/Boise",
    "IL": "America/Chicago", "IN": "America/Indiana/Indianapolis",
    "KS": "America/Chicago", "KY": "America/New_York", "LA": "America/Chicago",
    "MA": "America/New_York", "MD": "America/New_York", "ME": "America/New_York",
    "MI": "America/Detroit", "MN": "America/Chicago", "MO": "America/Chicago",
    "MS": "America/Chicago", "MT": "America/Denver", "NC": "America/New_York",
    "ND": "America/Chicago", "NE": "America/Chicago", "NH": "America/New_York",
    "NJ": "America/New_York", "NM": "America/Denver", "NV": "America/Los_Angeles",
    "NY": "America/New_York", "OH": "America/New_York", "OK": "America/Chicago",
    "OR": "America/Los_Angeles", "PA": "America/New_York", "RI": "America/New_York",
    "SC": "America/New_York", "SD": "America/Chicago", "TN": "America/New_York",
    "TX": "America/Chicago", "UT": "America/Denver", "VA": "America/New_York",
    "VT": "America/New_York", "WA": "America/Los_Angeles", "WI": "America/Chicago",
    "WV": "America/New_York", "WY": "America/Denver", "DC": "America/New_York",
    "AK": "America/Anchorage",
}

# Split-zone states: the venue's CITY decides. Keep this list exhaustive for any
# venue the schedule can reach, not merely the ones present today.
CITY_TZ = {
    ("TN", "Memphis"): "America/Chicago",
    ("TN", "Nashville"): "America/Chicago",
    ("TN", "Murfreesboro"): "America/Chicago",
    ("TN", "Martin"): "America/Chicago",
    ("TN", "Clarksville"): "America/Chicago",
    ("KY", "Bowling Green"): "America/Chicago",
    ("KY", "Murray"): "America/Chicago",
    ("TX", "El Paso"): "America/Denver",
    ("FL", "Pensacola"): "America/Chicago",
    ("FL", "Tallahassee"): "America/New_York",   # Leon County is Eastern
    ("IN", "Evansville"): "America/Chicago",
    ("ND", "Dickinson"): "America/Denver",
    ("NE", "Scottsbluff"): "America/Denver",
    ("KS", "Goodland"): "America/Denver",
    ("OR", "Ontario"): "America/Boise",
    ("ID", "Moscow"): "America/Los_Angeles",
    ("ID", "Coeur d'Alene"): "America/Los_Angeles",
    ("MI", "Iron Mountain"): "America/Menominee",
}

COUNTRY_TZ = {
    "Ireland": "Europe/Dublin", "England": "Europe/London",
    "Scotland": "Europe/London", "Wales": "Europe/London",
    "Puerto Rico": "America/Puerto_Rico", "Mexico": "America/Mexico_City",
    "Canada": "America/Toronto", "Bahamas": "America/Nassau",
    "Germany": "Europe/Berlin", "Australia": "Australia/Sydney",
    "Japan": "Asia/Tokyo",
}


class UnresolvedVenueZone(Exception):
    """Raised when a venue cannot be mapped. NEVER fall back to UTC."""


def venue_zone(address):
    """ESPN venue address dict -> ZoneInfo. Raises rather than guessing."""
    if not address:
        raise UnresolvedVenueZone("venue address missing")
    country = address.get("country")
    if country and country != "USA":
        z = COUNTRY_TZ.get(country)
        if not z:
            raise UnresolvedVenueZone(f"no zone mapped for country {country!r}")
        return ZoneInfo(z)
    state, city = address.get("state"), address.get("city")
    z = CITY_TZ.get((state, city)) or STATE_TZ.get(state)
    if not z:
        raise UnresolvedVenueZone(f"no zone mapped for state {state!r} (city {city!r})")
    return ZoneInfo(z)


def start_date(kickoff_utc, address, time_valid):
    """THE RULE. kickoff_utc must be timezone-aware UTC.

    Returns a datetime.date. Raises UnresolvedVenueZone rather than silently
    falling back to the UTC date -- that fallback is the original defect.
    """
    if kickoff_utc.tzinfo is None:
        raise ValueError("kickoff_utc must be timezone-aware")
    if time_valid:
        return kickoff_utc.astimezone(venue_zone(address)).date()
    return kickoff_utc.astimezone(EASTERN).date()


def needs_rederivation(time_valid):
    """True while ESPN still has no announced kickoff for the row."""
    return not time_valid


def assert_not_utc_dates(records):
    """REFRESH GUARD -- run after every ingestion.

    `records` is an iterable of dicts with keys:
        id, stored_date (date), kickoff_utc (aware), address (dict), time_valid (bool)

    Raises AssertionError listing every row whose stored date is not what the
    canonical rule produces. A refresh that reintroduces UTC dates cannot pass.
    """
    bad = []
    for r in records:
        want = start_date(r["kickoff_utc"], r["address"], r["time_valid"])
        if r["stored_date"] != want:
            bad.append((r["id"], r["stored_date"].isoformat(), want.isoformat()))
    if bad:
        raise AssertionError(
            f"{len(bad)} row(s) violate the canonical date rule "
            f"(stored -> expected): {bad[:20]}"
            + (f" ... and {len(bad)-20} more" if len(bad) > 20 else ""))
    return len(list(records)) if isinstance(records, list) else True
