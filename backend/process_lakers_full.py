#!/usr/bin/env python3
"""
Process full Lakers roster from Firecrawl scrape
"""

import sys
import json
from pathlib import Path

sys.path.insert(0, '/Users/kcdacre8tor/GSBPD2/backend')
from parse_roster_v2 import parse_roster_markdown_v2

LAKERS_MARKDOWN = """![Adou Thiero headshot](https://cdn.nba.com/headshots/nba/latest/260x190/1642876.png)

Adou

Thiero

Guard

1

Height

6'7"

Weight

220 lbs

Age

21

Years Pro

R

Country

USA

![Adou Thiero headshot](https://cdn.nba.com/headshots/nba/latest/1040x760/1642876.png)

Season

GP

2

PPG

3

APG

-

RPG

0.5

Height

6'7"

Weight

220 lbs

Age

21

Years Pro

R

Country

USA

[Bio](https://www.nba.com/player/1642876/adou-thiero/bio) [Shop](https://store.nba.com/?query=adou%20thiero)

![Jarred Vanderbilt headshot](https://cdn.nba.com/headshots/nba/latest/260x190/1629020.png)

Jarred

Vanderbilt

Forward

2

Height

6'8"

Weight

214 lbs

Age

26

Years Pro

7

Country

USA

![Jarred Vanderbilt headshot](https://cdn.nba.com/headshots/nba/latest/1040x760/1629020.png)

Season

GP

14

PPG

4.6

APG

1.5

RPG

5.6

Height

6'8"

Weight

214 lbs

Age

26

Years Pro

7

Country

USA

Play Name

[Bio](https://www.nba.com/player/1629020/jarred-vanderbilt/bio) [Shop](https://store.nba.com/?query=jarred%20vanderbilt)

![Dalton Knecht headshot](https://cdn.nba.com/headshots/nba/latest/260x190/1642261.png)

Dalton

Knecht

Forward

4

Height

6'6"

Weight

215 lbs

Age

24

Years Pro

1

Country

USA

![Dalton Knecht headshot](https://cdn.nba.com/headshots/nba/latest/1040x760/1642261.png)

Season

GP

14

PPG

7.1

APG

0.6

RPG

2.2

Height

6'6"

Weight

215 lbs

Age

24

Years Pro

1

Country

USA

Play Name

[Bio](https://www.nba.com/player/1642261/dalton-knecht/bio) [Shop](https://store.nba.com/?query=dalton%20knecht)

![Deandre Ayton headshot](https://cdn.nba.com/headshots/nba/latest/260x190/1629028.png)

Deandre

Ayton

Center

5

Height

7'0"

Weight

252 lbs

Age

27

Years Pro

7

Country

Bahamas

![Deandre Ayton headshot](https://cdn.nba.com/headshots/nba/latest/1040x760/1629028.png)

Season

GP

15

PPG

15.5

APG

0.9

RPG

8.4

Height

7'0"

Weight

252 lbs

Age

27

Years Pro

7

Country

Bahamas

[Bio](https://www.nba.com/player/1629028/deandre-ayton/bio) [Shop](https://shop.suns.com/phoenix-suns/deandre-ayton-gear/t-14583157+a-9080883210+z-95-3408385519?_s=bm-Suns-RosterPage)

![Gabe Vincent headshot](https://cdn.nba.com/headshots/nba/latest/260x190/1629216.png)

Gabe

Vincent

Guard

7

Height

6'2"

Weight

200 lbs

Age

29

Years Pro

6

Country

USA

![Gabe Vincent headshot](https://cdn.nba.com/headshots/nba/latest/1040x760/1629216.png)

Season

GP

5

PPG

4

APG

1.6

RPG

0.8

Height

6'2"

Weight

200 lbs

Age

29

Years Pro

6

Country

USA

Play Name

[Bio](https://www.nba.com/player/1629216/gabe-vincent/bio) [Shop](https://store.nba.com/?query=gabe%20vincent)

![Bronny James headshot](https://cdn.nba.com/headshots/nba/latest/260x190/1642355.png)

Bronny

James

Guard

9

Height

6'2"

Weight

210 lbs

Age

21

Years Pro

1

Country

USA

![Bronny James headshot](https://cdn.nba.com/headshots/nba/latest/1040x760/1642355.png)

Season

GP

10

PPG

2.1

APG

1.8

RPG

0.9

Height

6'2"

Weight

210 lbs

Age

21

Years Pro

1

Country

USA

Play Name

[Bio](https://www.nba.com/player/1642355/bronny-james/bio) [Shop](https://store.nba.com/?query=bronny%20james)

![Christian Koloko headshot](https://cdn.nba.com/headshots/nba/latest/260x190/1631132.png)

Christian

Koloko

Center

10

Height

6'11"

Weight

225 lbs

Age

25

Years Pro

3

Country

Cameroon

![Christian Koloko headshot](https://cdn.nba.com/headshots/nba/latest/1040x760/1631132.png)

Season

GP

2

PPG

-

APG

-

RPG

0.5

Height

6'11"

Weight

225 lbs

Age

25

Years Pro

3

Country

Cameroon

[Bio](https://www.nba.com/player/1631132/christian-koloko/bio) [Shop](https://store.nba.com/?query=christian%20koloko)

![Jaxson Hayes headshot](https://cdn.nba.com/headshots/nba/latest/260x190/1629637.png)

Jaxson

Hayes

Center-Forward

11

Height

7'0"

Weight

220 lbs

Age

25

Years Pro

6

Country

USA

![Jaxson Hayes headshot](https://cdn.nba.com/headshots/nba/latest/1040x760/1629637.png)

Season

GP

13

PPG

5.3

APG

1.1

RPG

4.1

Height

7'0"

Weight

220 lbs

Age

25

Years Pro

6

Country

USA

Play Name

[Bio](https://www.nba.com/player/1629637/jaxson-hayes/bio) [Shop](https://store.nba.com/?query=jaxson%20hayes)

![Jake LaRavia headshot](https://cdn.nba.com/headshots/nba/latest/260x190/1631222.png)

Jake

LaRavia

Forward

12

Height

6'7"

Weight

235 lbs

Age

24

Years Pro

3

Country

USA

![Jake LaRavia headshot](https://cdn.nba.com/headshots/nba/latest/1040x760/1631222.png)

Season

GP

16

PPG

10.3

APG

2.3

RPG

4.3

Height

6'7"

Weight

235 lbs

Age

24

Years Pro

3

Country

USA

[Bio](https://www.nba.com/player/1631222/jake-laravia/bio) [Shop](https://store.nba.com/?query=jake%20laravia)

![Maxi Kleber headshot](https://cdn.nba.com/headshots/nba/latest/260x190/1628467.png)

Maxi

Kleber

Forward

14

Height

6'10"

Weight

240 lbs

Age

33

Years Pro

8

Country

Germany

![Maxi Kleber headshot](https://cdn.nba.com/headshots/nba/latest/1040x760/1628467.png)

Season

GP

5

PPG

1.8

APG

0.8

RPG

2

Height

6'10"

Weight

240 lbs

Age

33

Years Pro

8

Country

Germany

[Bio](https://www.nba.com/player/1628467/maxi-kleber/bio) [Shop](https://store.nba.com/?query=maxi%20kleber)

![Austin Reaves headshot](https://cdn.nba.com/headshots/nba/latest/260x190/1630559.png)

Austin

Reaves

Guard

15

Height

6'5"

Weight

197 lbs

Age

27

Years Pro

4

Country

USA

![Austin Reaves headshot](https://cdn.nba.com/headshots/nba/latest/1040x760/1630559.png)

Season

GP

13

PPG

27.6

APG

7.3

RPG

5.5

Height

6'5"

Weight

197 lbs

Age

27

Years Pro

4

Country

USA

Play Name

[Bio](https://www.nba.com/player/1630559/austin-reaves/bio) [Shop](https://store.nba.com/?query=austin%20reaves)

![Nick Smith Jr. headshot](https://cdn.nba.com/headshots/nba/latest/260x190/1641733.png)

Nick

Smith Jr.

Guard

20

Height

6'2"

Weight

185 lbs

Age

21

Years Pro

2

Country

USA

![Nick Smith Jr. headshot](https://cdn.nba.com/headshots/nba/latest/1040x760/1641733.png)

Season

GP

6

PPG

7

APG

2.2

RPG

1

Height

6'2"

Weight

185 lbs

Age

21

Years Pro

2

Country

USA

[Bio](https://www.nba.com/player/1641733/nick-smith-jr/bio) [Shop](https://store.nba.com/?query=nick%20smith%20jr.)

![LeBron James headshot](https://cdn.nba.com/headshots/nba/latest/260x190/2544.png)

LeBron

James

Forward

23

Height

6'9"

Weight

250 lbs

Age

40

Years Pro

22

Country

USA

![LeBron James headshot](https://cdn.nba.com/headshots/nba/latest/1040x760/2544.png)

Season

GP

2

PPG

14

APG

10

RPG

4.5

Height

6'9"

Weight

250 lbs

Age

40

Years Pro

22

Country

USA

[Bio](https://www.nba.com/player/2544/lebron-james/bio) [Shop](https://store.nba.com/?query=lebron%20james)

![Drew Timme headshot](https://cdn.nba.com/headshots/nba/latest/260x190/1631166.png)

Drew

Timme

Forward

26

Height

6'9"

Weight

235 lbs

Age

25

Years Pro

1

Country

USA

![Drew Timme headshot](https://cdn.nba.com/headshots/nba/latest/1040x760/1631166.png)

Season

GP

-

PPG

-

APG

-

RPG

-

Height

6'9"

Weight

235 lbs

Age

25

Years Pro

1

Country

USA

[Bio](https://www.nba.com/player/1631166/drew-timme/bio) [Shop](https://store.nba.com/?query=drew%20timme)

![Rui Hachimura headshot](https://cdn.nba.com/headshots/nba/latest/260x190/1629060.png)

Rui

Hachimura

Forward

28

Height

6'8"

Weight

230 lbs

Age

27

Years Pro

6

Country

Japan

![Rui Hachimura headshot](https://cdn.nba.com/headshots/nba/latest/1040x760/1629060.png)

Season

GP

15

PPG

15

APG

1.1

RPG

3.9

Height

6'8"

Weight

230 lbs

Age

27

Years Pro

6

Country

Japan

Play Name

[Bio](https://www.nba.com/player/1629060/rui-hachimura/bio) [Shop](https://store.nba.com/?query=rui%20hachimura)

![Chris Mañon headshot](https://cdn.nba.com/headshots/nba/latest/260x190/1643024.png)

Chris

Mañon

Guard

30

Height

6'4"

Weight

209 lbs

Age

23

Years Pro

R

Country

USA

![Chris Mañon headshot](https://cdn.nba.com/headshots/nba/latest/1040x760/1643024.png)

Season

GP

2

PPG

-

APG

-

RPG

1

Height

6'4"

Weight

209 lbs

Age

23

Years Pro

R

Country

USA

[Bio](https://www.nba.com/player/1643024/chris-ma%C3%B1on/bio) [Shop](https://store.nba.com/?query=chris%20ma%C3%B1on)

![Marcus Smart headshot](https://cdn.nba.com/headshots/nba/latest/260x190/203935.png)

Marcus

Smart

Guard

36

Height

6'3"

Weight

220 lbs

Age

31

Years Pro

11

Country

USA

![Marcus Smart headshot](https://cdn.nba.com/headshots/nba/latest/1040x760/203935.png)

Season

GP

13

PPG

9.5

APG

2.9

RPG

2.2

Height

6'3"

Weight

220 lbs

Age

31

Years Pro

11

Country

USA

[Bio](https://www.nba.com/player/203935/marcus-smart/bio) [Shop](https://store.nba.com/?query=marcus%20smart)

![Luka Dončić headshot](https://cdn.nba.com/headshots/nba/latest/260x190/1629029.png)

Luka

Dončić

Forward-Guard

77

Height

6'8"

Weight

230 lbs

Age

26

Years Pro

7

Country

Slovenia

![Luka Dončić headshot](https://cdn.nba.com/headshots/nba/latest/1040x760/1629029.png)

Season

GP

12

PPG

34.5

APG

8.9

RPG

8.8

Height

6'8"

Weight

230 lbs

Age

26

Years Pro

7

Country

Slovenia

[Bio](https://www.nba.com/player/1629029/luka-don%C4%8Di%C4%87/bio) [Shop](https://store.nba.com/?query=luka%20don%C4%8Di%C4%87)"""

if __name__ == "__main__":
    players = parse_roster_markdown_v2(LAKERS_MARKDOWN, "1610612747", "Los Angeles Lakers")

    print(f"=" * 80)
    print(f"LAKERS ROSTER - {len(players)} Players")
    print(f"=" * 80)
    print()

    for p in players:
        print(f"✓ {p['name']:<25} #{p['jersey_number']:<3} {p['position']:<20} GP:{p['gp']:<3} PPG:{p['ppg']:<6.1f} RPG:{p['rpg']:<6.1f} APG:{p['apg']:<6.1f}")

    # Save to players.json
    base_dir = Path(__file__).parent
    players_file = base_dir / "nba_data" / "players.json"

    with open(players_file, 'w') as f:
        json.dump(players, f, indent=2)

    print()
    print(f"=" * 80)
    print(f"✓ Saved {len(players)} Lakers players to {players_file}")
    print(f"=" * 80)
