#!/usr/bin/env python3
"""
Process Celtics roster data from Firecrawl
"""

import sys
import json
import re
from pathlib import Path

sys.path.insert(0, '/Users/kcdacre8tor/GSBPD2/backend')
from scrape_and_parse_all_rosters import extract_player_data

# Celtics markdown from Firecrawl
CELTICS_MARKDOWN = """
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

![](https://cdn.nba.com/headshots/nba/latest/1040x760/1628449.png?111)

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

![](https://cdn.nba.com/headshots/nba/latest/1040x760/1627759.png?111)

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

![](https://cdn.nba.com/headshots/nba/latest/1040x760/1630568.png?111)

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

![](https://cdn.nba.com/headshots/nba/latest/1040x760/1642864.png?111)

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

![](https://cdn.nba.com/headshots/nba/latest/1040x760/1631199.png?111)

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

![](https://cdn.nba.com/headshots/nba/latest/1040x760/1630573.png?111)

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

![](https://cdn.nba.com/headshots/nba/latest/1040x760/1631169.png?111)

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

![](https://cdn.nba.com/headshots/nba/latest/1040x760/1630202.png?111)

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

![](https://cdn.nba.com/headshots/nba/latest/1040x760/1629674.png?111)

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

![](https://cdn.nba.com/headshots/nba/latest/1040x760/1631248.png?111)

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

![](https://cdn.nba.com/headshots/nba/latest/1040x760/1642917.png?111)

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

![](https://cdn.nba.com/headshots/nba/latest/1040x760/1629014.png?111)

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

![](https://cdn.nba.com/headshots/nba/latest/1040x760/1628369.png?111)

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

![](https://cdn.nba.com/headshots/nba/latest/1040x760/1630214.png?111)

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

![](https://cdn.nba.com/headshots/nba/latest/1040x760/1641775.png?111)

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

![](https://cdn.nba.com/headshots/nba/latest/1040x760/1628401.png?111)

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

![](https://cdn.nba.com/headshots/nba/latest/1040x760/1642873.png?111)

Amari

Williams

Forward-Center
"""

if __name__ == "__main__":
    players = extract_player_data(CELTICS_MARKDOWN, "1610612738", "Boston Celtics")

    print(f"Extracted {len(players)} players from Celtics roster")
    print()

    for player in players:
        print(f"✓ {player['name']:<25} #{player['jersey_number']:<3} {player['position']:<20} {player['ppg']:>5.1f} PPG")

    # Save to JSON
    base_dir = Path(__file__).parent
    output_file = base_dir / "nba_data" / "celtics_test.json"

    with open(output_file, 'w') as f:
        json.dump(players, f, indent=2)

    print()
    print(f"✓ Saved to {output_file}")
