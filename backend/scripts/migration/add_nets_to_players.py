#!/usr/bin/env python3
"""
Add Nets roster to players.json
"""

import sys
import json
from pathlib import Path

sys.path.insert(0, '/Users/kcdacre8tor/GSBPD2/backend')
from parse_roster_v2 import parse_roster_markdown_v2

NETS_MARKDOWN = """![Ziaire Williams headshot](https://cdn.nba.com/headshots/nba/latest/260x190/1630533.png)

Ziaire

Williams

Forward

1

Height

6'9"

Weight

185 lbs

Age

24

Years Pro

4

Country

USA

Season

GP

14

PPG

9.2

APG

0.6

RPG

2.6

![Danny Wolf headshot](https://cdn.nba.com/headshots/nba/latest/260x190/1642874.png)

Danny

Wolf

Forward

2

Height

6'11"

Weight

250 lbs

Age

21

Years Pro

R

Country

USA

Season

GP

3

PPG

0.7

APG

0.7

RPG

0.7

![Drake Powell headshot](https://cdn.nba.com/headshots/nba/latest/260x190/1642962.png)

Drake

Powell

Guard-Forward

4

Height

6'5"

Weight

195 lbs

Age

20

Years Pro

R

Country

USA

Season

GP

11

PPG

6.9

APG

2

RPG

2

![Haywood Highsmith headshot](https://cdn.nba.com/headshots/nba/latest/260x190/1629312.png)

Haywood

Highsmith

Forward

7

Height

6'5"

Weight

220 lbs

Age

28

Years Pro

5

Country

USA

Season

GP

-

PPG

-

APG

-

RPG

-

![Egor Dëmin headshot](https://cdn.nba.com/headshots/nba/latest/260x190/1642856.png)

Egor

Dëmin

Guard

8

Height

6'8"

Weight

200 lbs

Age

19

Years Pro

R

Country

Russia

Season

GP

16

PPG

7.6

APG

3.4

RPG

3.4

![E.J. Liddell headshot](https://cdn.nba.com/headshots/nba/latest/260x190/1630604.png)

E.J.

Liddell

Forward

9

Height

6'6"

Weight

240 lbs

Age

24

Years Pro

2

Country

USA

Season

GP

6

PPG

2

APG

-

RPG

1.3

![Tyson Etienne headshot](https://cdn.nba.com/headshots/nba/latest/260x190/1630623.png)

Tyson

Etienne

Guard

10

Height

6'0"

Weight

200 lbs

Age

26

Years Pro

1

Country

USA

Season

GP

6

PPG

1

APG

-

RPG

-

![Tyrese Martin headshot](https://cdn.nba.com/headshots/nba/latest/260x190/1631213.png)

Tyrese

Martin

Forward

13

Height

6'6"

Weight

215 lbs

Age

26

Years Pro

2

Country

USA

Season

GP

17

PPG

8.4

APG

2.7

RPG

3.3

![Terance Mann headshot](https://cdn.nba.com/headshots/nba/latest/260x190/1629611.png)

Terance

Mann

Guard-Forward

14

Height

6'6"

Weight

215 lbs

Age

29

Years Pro

6

Country

USA

Season

GP

17

PPG

8.6

APG

3.6

RPG

3.4

![Michael Porter Jr. headshot](https://cdn.nba.com/headshots/nba/latest/260x190/1629008.png)

Michael

Porter Jr.

Forward

17

Height

6'10"

Weight

218 lbs

Age

27

Years Pro

6

Country

USA

Season

GP

16

PPG

24.3

APG

3

RPG

7.4

![Day'Ron Sharpe headshot](https://cdn.nba.com/headshots/nba/latest/260x190/1630549.png)

Day'Ron

Sharpe

Center

20

Height

6'10"

Weight

265 lbs

Age

24

Years Pro

4

Country

USA

Season

GP

16

PPG

6.7

APG

1.8

RPG

5.5

![Noah Clowney headshot](https://cdn.nba.com/headshots/nba/latest/260x190/1641730.png)

Noah

Clowney

Forward-Center

21

Height

6'10"

Weight

210 lbs

Age

21

Years Pro

2

Country

USA

Season

GP

17

PPG

12.2

APG

1.6

RPG

3.5

![Jalen Wilson headshot](https://cdn.nba.com/headshots/nba/latest/260x190/1630592.png)

Jalen

Wilson

Forward

22

Height

6'6"

Weight

220 lbs

Age

25

Years Pro

2

Country

USA

Season

GP

14

PPG

5.4

APG

0.6

RPG

1

![Cam Thomas headshot](https://cdn.nba.com/headshots/nba/latest/260x190/1630560.png)

Cam

Thomas

Guard

24

Height

6'3"

Weight

210 lbs

Age

24

Years Pro

4

Country

Japan

Season

GP

8

PPG

21.4

APG

2.6

RPG

1.4

![Nic Claxton headshot](https://cdn.nba.com/headshots/nba/latest/260x190/1629651.png)

Nic

Claxton

Center

33

Height

6'11"

Weight

215 lbs

Age

26

Years Pro

6

Country

USA

Season

GP

17

PPG

14.1

APG

4.1

RPG

7.5

![Ben Saraf headshot](https://cdn.nba.com/headshots/nba/latest/260x190/1642879.png)

Ben

Saraf

Guard

77

Height

6'6"

Weight

200 lbs

Age

19

Years Pro

R

Country

Israel

Season

GP

7

PPG

3.3

APG

2.4

RPG

1.9

![Nolan Traore headshot](https://cdn.nba.com/headshots/nba/latest/260x190/1642849.png)

Nolan

Traore

Guard

88

Height

6'3"

Weight

185 lbs

Age

19

Years Pro

R

Country

France

Season

GP

4

PPG

1.8

APG

1.3

RPG

0.3"""

if __name__ == "__main__":
    # Parse Nets roster
    nets_players = parse_roster_markdown_v2(NETS_MARKDOWN, "1610612751", "Brooklyn Nets")

    print(f"Parsed {len(nets_players)} Nets players")

    # Load existing players.json (Lakers)
    base_dir = Path(__file__).parent
    players_file = base_dir / "nba_data" / "players.json"

    with open(players_file, 'r') as f:
        all_players = json.load(f)

    lakers_count = len(all_players)

    # Add Nets players
    all_players.extend(nets_players)

    # Save updated players.json
    with open(players_file, 'w') as f:
        json.dump(all_players, f, indent=2)

    print(f"\n✓ Updated players.json:")
    print(f"  - Lakers: {lakers_count} players")
    print(f"  - Nets: {len(nets_players)} players")
    print(f"  - Total: {len(all_players)} players from 2 teams")
    print(f"\n✓ Saved to {players_file}")
