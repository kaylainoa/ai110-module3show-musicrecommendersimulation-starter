"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from src.recommender import load_songs, recommend_songs, SCORING_STRATEGIES


# Stress-test profiles: three everyday personas plus two adversarial/edge
# cases designed to try to trip up the scoring logic (conflicting signals,
# or a genre that doesn't exist anywhere in the catalog).
USER_PROFILES = {
    "Happy Pop": {"genre": "pop", "mood": "happy", "energy": 0.8, "likes_acoustic": False},
    "Chill Lofi": {"genre": "lofi", "mood": "chill", "energy": 0.35, "likes_acoustic": True},
    "Deep Intense Rock": {"genre": "rock", "mood": "intense", "energy": 0.85, "likes_acoustic": False},
    "Adversarial: Conflicting (sad + high energy metal, but acoustic)": {
        "genre": "metal", "mood": "sad", "energy": 0.9, "likes_acoustic": True,
    },
    "Adversarial: Genre Not In Catalog (edm)": {
        "genre": "edm", "mood": "happy", "energy": 0.8, "likes_acoustic": False,
    },
}


def format_table(recommendations) -> str:
    """Formats (song, score, reasons) tuples as a simple ASCII table."""
    headers = ["#", "Title", "Artist", "Score", "Reasons"]
    rows = [
        [str(rank), song["title"], song["artist"], f"{score:.2f}", reasons]
        for rank, (song, score, reasons) in enumerate(recommendations, start=1)
    ]
    widths = [max(len(h), *(len(row[i]) for row in rows)) if rows else len(h) for i, h in enumerate(headers)]

    def format_row(cells):
        return " | ".join(cell.ljust(widths[i]) for i, cell in enumerate(cells))

    separator = "-+-".join("-" * w for w in widths)
    lines = [format_row(headers), separator]
    lines.extend(format_row(row) for row in rows)
    return "\n".join(lines)


def print_recommendations(profile_name: str, user_prefs: dict, songs: list, **kwargs) -> None:
    recommendations = recommend_songs(user_prefs, songs, k=5, **kwargs)
    print(f"\n=== {profile_name} — {user_prefs} ===\n")
    print(format_table(recommendations))
    print()


def main() -> None:
    songs = load_songs("data/songs.csv")

    for profile_name, user_prefs in USER_PROFILES.items():
        print_recommendations(profile_name, user_prefs, songs)

    # --- Stretch feature demos ---

    # Challenge 2: same profile, different scoring strategies (Strategy pattern).
    lofi_profile = USER_PROFILES["Chill Lofi"]
    print("\n########## Stretch Demo: Scoring Modes (Chill Lofi profile) ##########")
    for mode_name in ["balanced", "genre_first", "mood_first", "energy_focused", "discovery"]:
        print_recommendations(f"Mode: {mode_name}", lofi_profile, songs, scorer=SCORING_STRATEGIES[mode_name])

    # Challenge 3: diversity penalty so one artist can't dominate the top 5.
    print("\n########## Stretch Demo: Diversity Penalty (Chill Lofi profile) ##########")
    print_recommendations("Chill Lofi (diversify=True)", lofi_profile, songs, diversify=True)


if __name__ == "__main__":
    main()
