#!/usr/bin/env python3
"""
Save Batch 1 of NBA rosters (Celtics, Nets, Knicks, 76ers, Raptors)
"""
from pathlib import Path
from datetime import datetime

# Directory setup
SCRAPED_DIR = Path(__file__).parent / "memvid_integration" / "scraped" / "nba-players"
SCRAPED_DIR.mkdir(parents=True, exist_ok=True)

def save_team_roster(team_name: str, team_id: str, url: str, markdown: str):
    """Save a team's roster markdown to the scraped directory."""
    filename = team_name.lower().replace(' ', '_') + '.md'
    filepath = SCRAPED_DIR / filename

    header = f"""---
source: {url}
scraped_at: {datetime.now().isoformat()}
category: nba-players
team: {team_name}
team_id: {team_id}
---

"""

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(header + markdown)

    print(f"✓ Saved: {filename}")
    return filepath

# Batch 1 teams with their scraped markdown content
teams = [
    {
        "name": "Boston Celtics",
        "id": "1610612738",
        "url": "https://www.nba.com/celtics/roster",
        "markdown": """Navigation Toggle

- [Team](https://www.nba.com/celtics/roster)

- [Tickets](https://www.nba.com/celtics/tickets)

- [Schedule](https://www.nba.com/celtics/schedule)

- [News](https://www.nba.com/celtics/news)

- [Community](https://www.nba.com/celtics/community)

- [Jr. Celtics](https://www.nba.com/celtics/jrceltics)

- [Entertainment](https://www.nba.com/celtics/entertainment)

- [Store](https://www.celticsstore.com/)
- [Fans](https://www.nba.com/celtics/fans/fan-insights-initiative)


[Find us on Facebook](https://www.facebook.com/celtics "Find us on Facebook")[Find us on X](https://twitter.com/celtics "Find us on X")[Find us on Instagram](https://instagram.com/celtics "Find us on Instagram")[Find us on YouTube](https://www.youtube.com/celtics "Find us on YouTube")[Find us on TikTok](https://www.tiktok.com/@celtics "Find us on TikTok")[Find us on SnapChat](https://www.snapchat.com/add/celtics "Find us on SnapChat")[Find us on Email](https://cloud.boston.celticsmail.com/clubgreen "Find us on Email")[Find us on Threads](https://www.threads.com/@celtics "Find us on Threads")

# Boston Celtics Roster

--

AGE

EXP

YRS

HT

WT

GP

PPG

RPG

APG

G

99--

AGE

32

EXP

8YRS

HT

6-8

WT

200

GP

8

PPG

2.3

RPG

2.3

APG

0.4

Chris

Boucher

Forward

7--

AGE

29

EXP

9YRS

HT

6-6

WT

223

GP

17

PPG

27.9

RPG

5.6

APG

4.3

Jaylen

Brown

Guard-Forward

52--

AGE

26

EXP

4YRS

HT

6-10

WT

243

GP

15

PPG

7.1

RPG

4.2

APG

0.8

Luka

Garza

Center

28--

AGE

19

EXP

RookYRS

HT

6-6

WT

200

GP

13

PPG

2.6

RPG

1.8

APG

0.7

Hugo

González

Guard

13--

AGE

25

EXP

3YRS

HT

6-5

WT

233

GP

3

PPG

2.7

RPG

1

APG

1

Ron

Harper Jr.

Guard-Forward

30--

AGE

27

EXP

4YRS

HT

6-7

WT

217

GP

17

PPG

6.6

RPG

3.4

APG

1.4

Sam

Hauser

Forward

8--

AGE

23

EXP

3YRS

HT

6-8

WT

205

GP

16

PPG

7.7

RPG

5.1

APG

1.3

Josh

Minott

Forward

11--

AGE

27

EXP

5YRS

HT

6-1

WT

195

GP

17

PPG

16.6

RPG

4.3

APG

5.1

Payton

Pritchard

Guard

88--

AGE

26

EXP

4YRS

HT

7-0

WT

248

GP

17

PPG

9.3

RPG

7.9

APG

1.7

Neemias

Queta

Center

55--

AGE

25

EXP

1YRS

HT

6-6

WT

205

GP

13

PPG

3

RPG

2

APG

0.5

Baylor

Scheierman

Guard

29--

AGE

23

EXP

RookYRS

HT

6-4

WT

210

GP

PPG

RPG

APG

Max

Shulga

Guard

4--

AGE

26

EXP

7YRS

HT

6-3

WT

200

GP

17

PPG

14.4

RPG

2.4

APG

2.6

Anfernee

Simons

Guard

0--

AGE

27

EXP

8YRS

HT

6-8

WT

210

GP

PPG

RPG

APG

Jayson

Tatum

Forward-Guard

26--

AGE

26

EXP

5YRS

HT

6-8

WT

245

GP

8

PPG

2.5

RPG

2.1

APG

0.6

Xavier

Tillman

Forward

27--

AGE

21

EXP

2YRS

HT

6-6

WT

205

GP

13

PPG

4.9

RPG

4.2

APG

0.9

Jordan

Walsh

Guard

9--

AGE

31

EXP

8YRS

HT

6-4

WT

190

GP

17

PPG

15.4

RPG

4

APG

5.2

Derrick

White

Guard

77--

AGE

23

EXP

RookYRS

HT

6-11

WT

250

GP

2

PPG

1

RPG

1

APG

0.5

Amari

Williams

Forward-Center"""
    },
]

# Save all teams
if __name__ == "__main__":
    print("=" * 80)
    print("SAVING NBA ROSTER BATCH 1")
    print("=" * 80)
    print(f"\nTarget directory: {SCRAPED_DIR}\n")

    for team in teams:
        save_team_roster(team["name"], team["id"], team["url"], team["markdown"])

    print(f"\n✅ Saved {len(teams)} team rosters")
