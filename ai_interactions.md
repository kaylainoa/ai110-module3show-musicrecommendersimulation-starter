# AI Interactions Log

> **Stretch features only.** Only fill in the sections that apply to stretch features you attempted. If you did not attempt a stretch feature, leave its section blank or delete it. This file is not required for the core project.

---

## Agentic Workflow (SF8)

> Document your experience using an AI agent (e.g., Cursor Agent, Claude, Copilot) to make multi-step changes autonomously.

**What task did you give the agent?**

Challenge 1 from the optional stretch round: add 5+ new song attributes not in the baseline data, update the CSV, and update the scoring logic so it actually accounts for the new attributes instead of just sitting there unused.

**Prompts used:**

"Add 5 new attributes to data/songs.csv that go beyond genre/mood/energy, something like popularity, release decade, or detailed mood tags. Fill in believable values for all 18 existing songs, keep it backward compatible so the current tests and scoring don't break, and update score_song so it actually uses at least some of the new attributes instead of just adding dead columns."

**What did the agent generate or change?**

- `data/songs.csv`: added `popularity` (0-100), `release_decade`, `mood_tags` (semicolon-separated so it doesn't collide with the CSV's comma delimiter), `language`, and `explicit`, filled in for all 18 rows.
- `src/recommender.py`: gave the `Song` dataclass default values for the 5 new fields (so the existing test file's `Song(...)` calls, which don't pass them, still work), updated `load_songs` to parse `popularity` as an int, split `mood_tags` on `;`, and parse `explicit` as a real bool instead of the string `"True"`/`"False"`.
- Folded the new attributes into scoring as a new `discovery` weight preset (decade match, mood-tag overlap, and a small popularity-based bonus), rather than adding them to the default recipe, so the original documented scores wouldn't silently change.

**What did you verify or fix manually?**

I reran `pytest` and `python -m src.main` after the change to confirm the original 5 stress-test profiles still produced the exact same scores as before (they did, since the new attributes only affect the `discovery` mode). I also manually checked that `explicit` was being read as an actual boolean and not the literal string `"False"` (which is truthy in Python), since that's an easy mistake for a CSV loader to make.

---

## Design Pattern (SF10)

> Document how AI helped you choose or implement a design pattern.

**Which design pattern did you use?**

Strategy pattern: interchangeable scoring algorithms that all share the same interface (`(user_prefs, song) -> (score, reasons)`), swapped at runtime instead of hardcoded into `recommend_songs`.

**How did AI help you brainstorm or implement it?**

I asked for a way to support multiple ranking modes ("Genre-First," "Mood-First," "Energy-Focused") without copy-pasting the scoring function four times. The suggestion was to keep one generic scorer that takes a weight configuration, and treat each named mode as a thin wrapper around it, that's the Strategy pattern: same interface, different behavior, chosen at call time. I considered a full class hierarchy (a `ScoringStrategy` base class with subclasses for each mode) but that felt like overkill for something that's really just "the same formula with different numbers," so I went with a simpler factory function instead of separate classes.

**How does the pattern appear in your final code?**

In `src/recommender.py`: `WEIGHT_PRESETS` holds the numbers for each mode (`balanced`, `genre_first`, `mood_first`, `energy_focused`, `discovery`), `_score_with_weights` is the one real scoring implementation, and `make_scorer(weights)` is the factory that closes over a weight preset and returns a ready-to-use scoring function. `SCORING_STRATEGIES` is a dict of all five, built from `WEIGHT_PRESETS` in one line. `recommend_songs(..., scorer=SCORING_STRATEGIES["mood_first"])` is where the strategy actually gets swapped in, and `src/main.py`'s stretch demo loops over all five strategies on the same profile to show the ranking change.
