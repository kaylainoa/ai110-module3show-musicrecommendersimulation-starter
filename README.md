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

Top recommendations:

1. Sunrise City - Score: 4.48
   Because: genre match (+2.0), mood match (+1.0), energy closeness (+0.98), acoustic preference match (+0.5)

2. Gym Hero - Score: 3.37
   Because: genre match (+2.0), energy closeness (+0.87), acoustic preference match (+0.5)

3. Rooftop Lights - Score: 2.46
   Because: mood match (+1.0), energy closeness (+0.96), acoustic preference match (+0.5)

4. Night Drive Loop - Score: 1.45
   Because: energy closeness (+0.95), acoustic preference match (+0.5)

5. Neon Tide - Score: 1.42
   Because: energy closeness (+0.92), acoustic preference match (+0.5)
```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

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

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this



