# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.

---

## How The System Works

Honestly, I think real recommenders like Spotify aren't doing anything magical. They just know a bunch of facts about a song and a bunch of facts about what you like, then check how well those two lists line up. The song that matches the most, and matches the important stuff, wins and gets shown to you first. My version does the same thing on a much smaller scale, using the features that actually matter when I'm picking music, not just the ones with numbers attached.

To me, "vibe" is mostly genre and mood first, and energy second. If I say I want pop and I'm in a happy mood, I don't really want a sad rock song even if the tempo lines up, so genre and mood are the main things that need to match. Energy is a little different. I don't want the "most energetic" song necessarily, I want one close to the energy level I'm actually in the mood for. Whether a song is acoustic or not is more of a small nice-to-have on top, not a dealbreaker.

Here's what I'm using on each side:

**Song features:** genre, mood, energy, and acousticness.

**UserProfile info:** favorite_genre, favorite_mood, target_energy, and likes_acoustic (whether they're into acoustic-sounding songs).

Here's my actual recipe:
- +2.0 points if genre matches
- +1.0 point if mood matches
- points for energy based on how close it is to the target (so 1 minus the difference), not just "higher is better"
- +0.5 bonus if the acoustic-ness lines up with what they like

Once every song in the CSV has a score like that, the recommender sorts them highest to lowest and hands back the top few. The scoring part figures out how good one song is for someone, and the ranking part is what actually turns a pile of scores into a real "here are your top 5" list.

One bias I'm expecting: since genre is worth double what mood is, this system will probably over-favor genre matches and pass up songs that are actually a great mood match but in a slightly different genre (like an indie pop song that would've been perfect for a "happy" request, just because the user typed "pop" instead). It also can't tell two songs apart if they tie on genre, mood, and energy, since it has no way to break that tie yet.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

Output of `python -m src.main` for the default profile (`genre=pop, mood=happy, energy=0.8, likes_acoustic=False`):

```
Loaded songs: 18

=== Happy Pop — {'genre': 'pop', 'mood': 'happy', 'energy': 0.8, 'likes_acoustic': False} ===

# | Title            | Artist        | Score | Reasons
--+------------------+---------------+-------+--------------------------------------------------------------------------------------------------
1 | Sunrise City     | Neon Echo     | 4.48  | genre match (+2.0), mood match (+1.0), energy closeness (+0.98), acoustic preference match (+0.5)
2 | Gym Hero         | Max Pulse     | 3.37  | genre match (+2.0), energy closeness (+0.87), acoustic preference match (+0.5)
3 | Rooftop Lights   | Indigo Parade | 2.46  | mood match (+1.0), energy closeness (+0.96), acoustic preference match (+0.5)
4 | Night Drive Loop | Neon Echo     | 1.45  | energy closeness (+0.95), acoustic preference match (+0.5)
5 | Neon Tide        | Pulse Theory  | 1.42  | energy closeness (+0.92), acoustic preference match (+0.5)
```

The full run also loops through the other stress-test profiles and prints stretch-feature demos (scoring modes and the diversity penalty), see [Stretch Features](#stretch-features-optional) below.

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

I tried halving the genre weight (2.0 to 1.0) and doubling the energy weight (1x to 2x) to see what would happen if energy mattered more than genre.

For the "Happy Pop" profile, the top pick stayed the same (Sunrise City), but #2 and #3 swapped: Gym Hero (genre match, but energy a bit further from target) dropped below Rooftop Lights (no genre match, but a closer energy match), because energy now had more pull than a genre match. It also squeezed everything else closer together, since a lot of songs sit in a similar energy range, so more of the list started looking like a coin flip instead of a clear ranking. My takeaway: it made the results *different*, not obviously *better*. Genre still felt like the more meaningful signal for "does this match what I asked for," so I reverted back to the original weights (2.0 genre, 1.0 mood, 1x energy, 0.5 acoustic).

---

## Stretch Features (Optional)

I tried all four optional challenges:

**1. Advanced song features.** Added 5 new columns to `data/songs.csv`: `popularity` (0-100), `release_decade`, `mood_tags` (detailed tags like "nostalgic;euphoric"), `language`, and `explicit`. These feed into a new `discovery` scoring mode (see below) that adds small bonuses for a matching decade, overlapping mood tags, and popularity, without changing the original recipe's scores.

**2. Multiple scoring modes (Strategy pattern).** `recommender.py` now has a `WEIGHT_PRESETS` dict and a `make_scorer(weights)` factory that builds an interchangeable scoring function for each preset: `balanced` (the original recipe), `genre_first`, `mood_first`, `energy_focused`, and `discovery`. `recommend_songs()` takes an optional `scorer=` argument, so swapping the ranking strategy is a one-line change in `main.py` instead of rewriting the scoring logic. Running the Chill Lofi profile through all five modes shows the ranking genuinely shift: under `mood_first`, Spacewalk Thoughts (a mood match with no genre match) jumps to #3, ahead of Focus Flow (a genre match with no mood match), the exact opposite of what happens under `genre_first`.

**3. Diversity penalty.** `recommend_songs(..., diversify=True)` greedily builds the top-k list and subtracts `artist_penalty` (default 1.0) points from a song's score for every prior pick already made by the same artist. On the Chill Lofi profile, LoRoom has two songs in the catalog (Midnight Coding and Focus Flow); with `diversify=True`, Focus Flow's score drops from 3.45 to 2.45 once Midnight Coding has already been picked, and the reason list shows exactly why ("diversity penalty (-1.0, artist already picked)").

**4. Visual summary table.** `main.py` has a small `format_table()` helper that lays out rank, title, artist, score, and reasons as an aligned ASCII table (no external dependency needed), instead of the original multi-line "Because: ..." print block.

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Building this made it click for me that a recommender isn't predicting anything magical, it's just turning a taste profile and a catalog of numbers into a comparison, then sorting the results. Every "because" in the output traces back to a rule I wrote myself (genre match, mood match, how close the energy is), so the "prediction" is really just arithmetic wearing a friendly explanation. That's reassuring and a little unsettling at the same time: it means a system can sound confident about a recommendation for reasons that have nothing to do with actually understanding music.

Bias showed up faster than I expected, and mostly through the data, not the math. Lofi has three songs in my catalog while almost every other genre only has one, so lofi fans get more chances to land a genre match just because of how I built the dataset, not because the system understands lofi better. Genre and mood only match on exact spelling too, so a mood that isn't in my dataset at all (like "sad") just silently disappears from someone's score instead of telling them it didn't count. And since I weighted genre heavier than mood, the system will happily recommend a technically-right-genre song over one that actually matches how someone said they feel. None of that is intentional unfairness, it's just what happens when a small, hand-typed dataset and a handful of weight numbers stand in for something as messy as real taste.



