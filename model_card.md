# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

**VibeMatch 1.0**

---

## 2. Intended Use  

VibeMatch takes a few things a listener says they like (a favorite genre, a favorite mood, an energy level, and whether they like acoustic songs) and picks the top 5 songs from a small catalog that match best. It's meant to show, in a simple and see-through way, how a recommender turns a taste profile into a ranked list. It assumes the user can describe their taste in a few basic words, and that those words match how the songs are labeled.

This is a classroom project, not a real product. It's not intended for real listeners, it's not connected to a real music library, and it shouldn't be used to make actual decisions about what people listen to, what gets promoted, or anything with real consequences. It's a small, transparent toy meant for learning how scoring and ranking work together.

---

## 3. How the Model Works  

Every song has a genre, a mood, an energy level, and how acoustic it sounds. The user says what genre they like, what mood they're in, how much energy they want, and whether they like acoustic songs. VibeMatch checks each song against those preferences one at a time and hands out points: 2 points if the genre matches, 1 point if the mood matches, some points based on how close the song's energy is to what the user wants (closer is better, being too high is just as bad as being too low), and half a point if the acoustic-ness lines up with what they said they like. Genre counts for the most because it felt like the strongest signal for "is this even the right kind of music." Once every song has a score, VibeMatch sorts them from highest to lowest and hands back the top 5, along with the reasons for each one so you can see why it picked what it picked.

---

## 4. Data  

The catalog is 18 songs stored in `data/songs.csv`. It started as 10 songs (pop, lofi, rock, ambient, jazz, synthwave, indie pop) and I added 8 more to cover genres and moods that weren't there yet: hip-hop, metal, classical, country, r&b, folk, house, and reggae, with moods like angry, melancholy, romantic, nostalgic, and euphoric. Each song has genre, mood, energy, tempo, valence, danceability, and acousticness, all as plain numbers or short text, no audio or lyrics involved. It's still a tiny, hand-made dataset, so it's not balanced (lofi has 3 songs, most other genres have just 1), and it's missing a lot of real musical taste: no sub-genres, no artist popularity, no listening history, and no way to tell two songs in the same genre/mood apart besides energy and acousticness.

---

## 5. Strengths  

VibeMatch does well with users who give a clear, specific profile that actually exists in the catalog. The Chill Lofi test is a good example: it asked for lofi, chill, low energy, and acoustic, and got back Library Rain and Midnight Coding first, both genuinely lofi, chill, and mellow. That matched my intuition exactly. The Deep Intense Rock vs. Happy Pop comparison also showed that mood is pulling real weight, not just energy, since two profiles with similar energy levels still landed on very different, mood-appropriate songs (Storm Runner for intense, Sunrise City for happy). So for users whose taste fits neatly into the labels the catalog already uses, the scoring and ranking hold up well.

---

## 6. Limitations and Bias 

The catalog isn't balanced: lofi has 3 songs while almost every other genre (metal, classical, country, r&b, folk, house, reggae, hip-hop, ambient, jazz, synthwave) only has 1. That means a lofi fan gets three shots at a genre match and a metal fan only gets one, so lofi profiles will tend to look "better served" even though that's really just a data gap, not the algorithm being smarter about lofi. The acoustic-preference bonus also uses a hard cutoff (acousticness above or below 0.5), so two songs that are basically the same, like 0.49 versus 0.51, get treated as totally different, which feels unfair to the song that just barely missed the line. Genre and mood only match on exact spelling too, so if a mood the user types (like "sad") doesn't exist anywhere in the dataset, that whole signal just silently disappears from the score instead of telling the user it couldn't be used. On top of that, when I tested a "metal fan who also likes acoustic songs," the system still recommended the one metal song even though it's the least acoustic song in the whole catalog, because genre and energy alone were enough to win, which shows the system doesn't require every part of a profile to line up before it's confident in a recommendation.

---

## 7. Evaluation  

I tested five profiles in `src/main.py`: three normal personas ("Happy Pop," "Chill Lofi," "Deep Intense Rock") and two adversarial ones designed to try to trip the system up: a "metal fan who is sad but likes acoustic songs" (conflicting signals, and "sad" isn't even a mood in the dataset), and an "edm fan" (a genre that doesn't exist anywhere in the catalog). Here's the actual terminal output for all five, using the finalized recipe (+2.0 genre, +1.0 mood, energy closeness, +0.5 acoustic):

```
Loaded songs: 18

=== Happy Pop — {'genre': 'pop', 'mood': 'happy', 'energy': 0.8, 'likes_acoustic': False} ===

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


=== Chill Lofi — {'genre': 'lofi', 'mood': 'chill', 'energy': 0.35, 'likes_acoustic': True} ===

1. Library Rain - Score: 4.50
   Because: genre match (+2.0), mood match (+1.0), energy closeness (+1.00), acoustic preference match (+0.5)

2. Midnight Coding - Score: 4.43
   Because: genre match (+2.0), mood match (+1.0), energy closeness (+0.93), acoustic preference match (+0.5)

3. Focus Flow - Score: 3.45
   Because: genre match (+2.0), energy closeness (+0.95), acoustic preference match (+0.5)

4. Spacewalk Thoughts - Score: 2.43
   Because: mood match (+1.0), energy closeness (+0.93), acoustic preference match (+0.5)

5. Coffee Shop Stories - Score: 1.48
   Because: energy closeness (+0.98), acoustic preference match (+0.5)


=== Deep Intense Rock — {'genre': 'rock', 'mood': 'intense', 'energy': 0.85, 'likes_acoustic': False} ===

1. Storm Runner - Score: 4.44
   Because: genre match (+2.0), mood match (+1.0), energy closeness (+0.94), acoustic preference match (+0.5)

2. Gym Hero - Score: 2.42
   Because: mood match (+1.0), energy closeness (+0.92), acoustic preference match (+0.5)

3. Sunrise City - Score: 1.47
   Because: energy closeness (+0.97), acoustic preference match (+0.5)

4. Neon Tide - Score: 1.47
   Because: energy closeness (+0.97), acoustic preference match (+0.5)

5. Rooftop Lights - Score: 1.41
   Because: energy closeness (+0.91), acoustic preference match (+0.5)


=== Adversarial: Conflicting (sad + high energy metal, but acoustic) — {'genre': 'metal', 'mood': 'sad', 'energy': 0.9, 'likes_acoustic': True} ===

1. Iron Fever - Score: 2.93
   Because: genre match (+2.0), energy closeness (+0.93)

2. Backroad Sunset - Score: 1.12
   Because: energy closeness (+0.62), acoustic preference match (+0.5)

3. Midnight Coding - Score: 1.02
   Because: energy closeness (+0.52), acoustic preference match (+0.5)

4. Focus Flow - Score: 1.00
   Because: energy closeness (+0.50), acoustic preference match (+0.5)

5. Storm Runner - Score: 0.99
   Because: energy closeness (+0.99)


=== Adversarial: Genre Not In Catalog (edm) — {'genre': 'edm', 'mood': 'happy', 'energy': 0.8, 'likes_acoustic': False} ===

1. Sunrise City - Score: 2.48
   Because: mood match (+1.0), energy closeness (+0.98), acoustic preference match (+0.5)

2. Rooftop Lights - Score: 2.46
   Because: mood match (+1.0), energy closeness (+0.96), acoustic preference match (+0.5)

3. Night Drive Loop - Score: 1.45
   Because: energy closeness (+0.95), acoustic preference match (+0.5)

4. Neon Tide - Score: 1.42
   Because: energy closeness (+0.92), acoustic preference match (+0.5)

5. Storm Runner - Score: 1.39
   Because: energy closeness (+0.89), acoustic preference match (+0.5)
```

**What surprised me:** Sunrise City and Gym Hero (the two pop songs) kept showing up near the top even for the Rock and EDM profiles, not because of genre, but because they happen to sit at an energy level that's "close enough" to a lot of different targets. For the "conflicting" adversarial profile, the system didn't get confused exactly, it just quietly dropped the "sad" mood (since no song in the catalog has that mood) and recommended the one metal song anyway, even though that same user said they like acoustic songs and the metal song is the least acoustic one in the whole catalog. For the "edm" fan, since that genre doesn't exist in the dataset, the system fell back on mood and energy only, and ended up recommending pop songs to someone who explicitly said they wanted edm, with no indication anything was off.

**Comparing pairs of profiles:**

- **Happy Pop vs. Chill Lofi:** these two are near-opposites (high energy/produced vs. low energy/acoustic), and the results are near-opposites too: Sunrise City (high energy, not acoustic) vs. Library Rain (low energy, acoustic). That's exactly what should happen, and it did.
- **Deep Intense Rock vs. Happy Pop:** both profiles want fairly high energy, but Rock's top pick is Storm Runner (intense) and Pop's top pick is Sunrise City (happy). That means mood is actually doing real work here, not just energy, since a system that only cared about energy would mix these two lists together.
- **Adversarial Conflicting vs. Happy Pop:** Happy Pop's #1 pick gets the acoustic bonus, but the conflicting profile's #1 pick (Iron Fever) does not, since a metal song and "likes acoustic" don't line up. That's a good sign the acoustic bonus is actually being enforced, not just handed out for free.
- **Adversarial EDM vs. Happy Pop:** these two profiles are identical except genre changed from "pop" to "edm" (which isn't in the catalog). Sunrise City is still the top pick either way, but its score drops from 4.48 to 2.48 once the genre points disappear, which really shows how much of the ranking genre alone is responsible for.

---

## 8. Future Work  

If I kept working on this, I'd first add some fuzzy or synonym matching for genre and mood, so "indie" and "indie pop" or "sad" and "melancholy" aren't treated as total mismatches just because the spelling doesn't line up exactly. Second, I'd add a diversity rule so the top 5 doesn't lean so hard on whichever genre happens to have the most songs in the catalog (like lofi right now). Third, I'd use valence and danceability as tiebreakers instead of ignoring them completely, so two songs that tie on genre, mood, and energy still get ranked in a meaningful order instead of an arbitrary one.

---

## 9. Personal Reflection  

My biggest learning moment was seeing how much a recommender's "personality" comes from a handful of weight numbers, not from anything the system actually understands. Bumping mood from 1.5 to 1.0, or genre from 2.0 to 1.0, visibly changed which songs won, even though nothing about the songs themselves changed. AI tools were genuinely helpful for moving fast between steps (writing the scoring loop, generating extra catalog rows, drafting adversarial test profiles), but I had to double-check the actual math myself, like recalculating a score by hand to confirm the energy closeness formula was doing what I thought, and rereading the adversarial test outputs closely to catch that the system was silently dropping a mood it couldn't match instead of flagging it.

What surprised me most is how convincing a really simple algorithm can feel. A weighted sum and a sort is not "intelligent" in any real sense, but with the right reasons printed next to each song ("genre match," "energy closeness"), it reads like the system understands your taste. That made me a lot more skeptical of real-world recommendation apps: a confident-sounding explanation doesn't mean the system actually grasped what you wanted, it might just mean the numbers happened to line up. If I extended this project, I'd want to try giving it real listening history instead of a one-time typed profile, since that feels like the actual gap between this toy version and something like Spotify.
