import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float
    popularity: int = 50
    release_decade: str = ""
    mood_tags: str = ""
    language: str = "english"
    explicit: bool = False

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        # TODO: Implement explanation logic
        return "Explanation placeholder"

def load_songs(csv_path: str) -> List[Dict]:
    """Loads songs from a CSV file, converting numeric/boolean columns and splitting mood_tags."""
    songs = []
    with open(csv_path, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            row["id"] = int(row["id"])
            row["energy"] = float(row["energy"])
            row["tempo_bpm"] = float(row["tempo_bpm"])
            row["valence"] = float(row["valence"])
            row["danceability"] = float(row["danceability"])
            row["acousticness"] = float(row["acousticness"])
            row["popularity"] = int(row["popularity"])
            row["mood_tags"] = row["mood_tags"].split(";") if row["mood_tags"] else []
            row["explicit"] = row["explicit"].strip().lower() == "true"
            songs.append(row)
    print(f"Loaded songs: {len(songs)}")
    return songs

# Weight presets used by the named scoring strategies below (Challenge 2: Strategy
# pattern). "balanced" reproduces the original finalized Algorithm Recipe exactly;
# the decade/mood_tags/popularity weights only kick in for "discovery" so the
# documented default output doesn't shift just because new attributes exist.
WEIGHT_PRESETS: Dict[str, Dict[str, float]] = {
    "balanced": {"genre": 2.0, "mood": 1.0, "energy": 1.0, "acoustic": 0.5, "decade": 0.0, "mood_tags": 0.0, "popularity": 0.0},
    "genre_first": {"genre": 3.0, "mood": 0.5, "energy": 0.5, "acoustic": 0.5, "decade": 0.0, "mood_tags": 0.0, "popularity": 0.0},
    "mood_first": {"genre": 0.5, "mood": 3.0, "energy": 0.5, "acoustic": 0.5, "decade": 0.0, "mood_tags": 0.0, "popularity": 0.0},
    "energy_focused": {"genre": 0.5, "mood": 0.5, "energy": 3.0, "acoustic": 0.5, "decade": 0.0, "mood_tags": 0.0, "popularity": 0.0},
    "discovery": {"genre": 1.0, "mood": 1.0, "energy": 1.0, "acoustic": 0.5, "decade": 0.5, "mood_tags": 0.5, "popularity": 0.5},
}

def _score_with_weights(user_prefs: Dict, song: Dict, weights: Dict[str, float]) -> Tuple[float, List[str]]:
    """Scores one song against user_prefs using the given weight configuration."""
    score = 0.0
    reasons = []

    if weights["genre"] and user_prefs.get("genre") == song["genre"]:
        score += weights["genre"]
        reasons.append(f"genre match (+{weights['genre']:.1f})")

    if weights["mood"] and user_prefs.get("mood") == song["mood"]:
        score += weights["mood"]
        reasons.append(f"mood match (+{weights['mood']:.1f})")

    target_energy = user_prefs.get("energy")
    if weights["energy"] and target_energy is not None:
        energy_points = weights["energy"] * (1.0 - abs(song["energy"] - target_energy))
        score += energy_points
        reasons.append(f"energy closeness (+{energy_points:.2f})")

    likes_acoustic = user_prefs.get("likes_acoustic")
    if weights["acoustic"] and likes_acoustic is not None:
        is_acoustic_song = song["acousticness"] > 0.5
        if likes_acoustic == is_acoustic_song:
            score += weights["acoustic"]
            reasons.append(f"acoustic preference match (+{weights['acoustic']:.1f})")

    favorite_decade = user_prefs.get("favorite_decade")
    if weights["decade"] and favorite_decade and favorite_decade == song.get("release_decade"):
        score += weights["decade"]
        reasons.append(f"decade match (+{weights['decade']:.1f})")

    extra_moods = set(user_prefs.get("extra_moods", []))
    song_tags = set(song.get("mood_tags", []))
    if weights["mood_tags"] and extra_moods:
        overlap = extra_moods & song_tags
        if overlap:
            tag_bonus = weights["mood_tags"] * len(overlap)
            score += tag_bonus
            reasons.append(f"mood tag match ({', '.join(sorted(overlap))}) (+{tag_bonus:.2f})")

    if weights["popularity"]:
        popularity_bonus = weights["popularity"] * (song.get("popularity", 50) / 100)
        score += popularity_bonus
        reasons.append(f"popularity boost (+{popularity_bonus:.2f})")

    return score, reasons

def make_scorer(weights: Dict[str, float]):
    """Strategy factory: returns a score_song-compatible function bound to a weight preset."""
    def scorer(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
        return _score_with_weights(user_prefs, song, weights)
    return scorer

# Named scoring strategies (Challenge 2). Pass SCORING_STRATEGIES["mood_first"], etc.
# as the `scorer` argument to recommend_songs() to switch ranking behavior.
SCORING_STRATEGIES = {name: make_scorer(weights) for name, weights in WEIGHT_PRESETS.items()}

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Scores one song against user_prefs using the default "balanced" Algorithm Recipe."""
    return SCORING_STRATEGIES["balanced"](user_prefs, song)

def recommend_songs(
    user_prefs: Dict,
    songs: List[Dict],
    k: int = 5,
    scorer=None,
    diversify: bool = False,
    artist_penalty: float = 1.0,
) -> List[Tuple[Dict, float, str]]:
    """
    Scores every song against user_prefs and returns the top k, highest score first.
    If diversify=True, songs by an artist already picked lose artist_penalty
    points per prior pick (Challenge 3), so one artist can't dominate the list.
    """
    scorer = scorer or score_song
    scored = [(song, *scorer(user_prefs, song)) for song in songs]

    if not diversify:
        scored.sort(key=lambda item: item[1], reverse=True)
        top = scored[:k]
    else:
        remaining = list(scored)
        top = []
        artist_counts: Dict[str, int] = {}
        for _ in range(min(k, len(remaining))):
            remaining.sort(
                key=lambda item: item[1] - artist_counts.get(item[0]["artist"], 0) * artist_penalty,
                reverse=True,
            )
            song, score, reasons = remaining.pop(0)
            repeats = artist_counts.get(song["artist"], 0)
            if repeats:
                penalty = repeats * artist_penalty
                score -= penalty
                reasons = reasons + [f"diversity penalty (-{penalty:.1f}, artist already picked)"]
            artist_counts[song["artist"]] = repeats + 1
            top.append((song, score, reasons))

    return [
        (song, score, ", ".join(reasons) if reasons else "no strong matches")
        for song, score, reasons in top
    ]
