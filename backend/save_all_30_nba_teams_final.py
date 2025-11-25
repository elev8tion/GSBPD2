#!/usr/bin/env python3
"""
Save All 30 NBA Team Rosters - Final Complete Script
Saves all scraped NBA roster data to memvid scraped directory
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

# All 30 NBA teams with scraped data
teams_data = [
    {
        "name": "Boston Celtics",
        "id": "1610612738",
        "url": "https://www.nba.com/celtics/roster",
        "markdown": """## Boston Celtics Roster

Players include:
- Jayson Tatum (#0, Forward-Guard, 6'8", 210 lbs, Age 27, 8 YRS PRO)
- Jaylen Brown (#7, Guard-Forward, 6'6", 223 lbs, Age 29, 9 YRS PRO) - 27.9 PPG, 4.3 APG, 5.6 RPG
- Derrick White (#9, Guard, 6'4", 190 lbs, Age 31, 8 YRS PRO) - 15.4 PPG, 5.2 APG, 4 RPG
- Payton Pritchard (#11, Guard, 6'1", 195 lbs, Age 27, 5 YRS PRO) - 16.6 PPG, 5.1 APG, 4.3 RPG
- Neemias Queta (#88, Center, 7'0", 248 lbs, Age 26, 4 YRS PRO) - 9.3 PPG, 1.7 APG, 7.9 RPG
- Al Horford (#42, Center-Forward, 6'9", 240 lbs, Age 39, 18 YRS PRO) - 5.8 PPG, 1.8 APG, 4.3 RPG"""
    },
    {
        "name": "Brooklyn Nets",
        "id": "1610612751",
        "url": "https://www.nba.com/nets/roster",
        "markdown": """## Brooklyn Nets Roster

Players include:
- Mikal Bridges (#1, Forward, 6'6", 209 lbs, Age 29, 7 YRS PRO) - 13.4 PPG, 3.3 APG, 3.3 RPG
- Cameron Johnson (#2, Forward, 6'8", 210 lbs, Age 29, 6 YRS PRO) - 23.1 PPG, 2.9 APG, 4.4 RPG
- Dennis Schröder (#17, Guard, 6'1", 175 lbs, Age 32, 12 YRS PRO) - 6 PPG, 12.4 APG, 3.7 RPG"""
    },
    {
        "name": "New York Knicks",
        "id": "1610612752",
        "url": "https://www.nba.com/knicks/roster",
        "markdown": """## New York Knicks Roster

Players include:
- Jalen Brunson (#11, Guard, 6'2", 190 lbs, Age 29, 7 YRS PRO) - 22.8 PPG, 7.4 APG, 3.3 RPG
- Josh Hart (#3, Guard, 6'4", 215 lbs, Age 30, 8 YRS PRO) - 10.2 PPG, 4.2 APG, 9.1 RPG
- OG Anunoby (#8, Forward, 6'7", 232 lbs, Age 28, 8 YRS PRO) - 18.9 PPG, 1.9 APG, 5.9 RPG
- Karl-Anthony Towns (#32, Center-Forward, 7'0", 248 lbs, Age 29, 10 YRS PRO) - 25.2 PPG, 4.2 APG, 12.8 RPG"""
    },
    {
        "name": "Philadelphia 76ers",
        "id": "1610612755",
        "url": "https://www.nba.com/sixers/roster",
        "markdown": """## Philadelphia 76ers Roster

Players include:
- Tyrese Maxey (#0, Guard, 6'2", 200 lbs, Age 25, 5 YRS PRO) - 28.1 PPG, 6.7 APG, 4.4 RPG
- Joel Embiid (#21, Center, 7'0", 280 lbs, Age 31, 11 YRS PRO)
- Kelly Oubre Jr. (#9, Forward, 6'7", 203 lbs, Age 30, 10 YRS PRO) - 9.8 PPG, 1.5 APG, 4.9 RPG"""
    },
    {
        "name": "Toronto Raptors",
        "id": "1610612761",
        "url": "https://www.nba.com/raptors/roster",
        "markdown": """## Toronto Raptors Roster

Players include:
- RJ Barrett (#9, Guard-Forward, 6'6", 214 lbs, Age 25, 6 YRS PRO) - 19.4 PPG, 6 APG, 5.8 RPG
- Gradey Dick (#1, Guard-Forward, 6'7", 205 lbs, Age 22, 2 YRS PRO) - 14.1 PPG, 1.8 APG, 3 RPG
- Jakob Poeltl (#19, Center, 7'1", 245 lbs, Age 30, 9 YRS PRO) - 11.5 PPG, 2.6 APG, 10.8 RPG
- Scottie Barnes (#4, Forward, 6'7", 227 lbs, Age 24, 4 YRS PRO)"""
    },
    {
        "name": "Chicago Bulls",
        "id": "1610612741",
        "url": "https://www.nba.com/bulls/roster",
        "markdown": """## Chicago Bulls Roster

Players include:
- Nikola Vučević (#9, Center, 7'0", 260 lbs, Age 35, 14 YRS PRO) - 18.8 PPG, 2.9 APG, 9.5 RPG
- Coby White (#0, Guard, 6'5", 195 lbs, Age 25, 6 YRS PRO) - 17.6 PPG, 4.2 APG, 3.7 RPG
- Josh Giddey (#3, Guard, 6'9", 216 lbs, Age 23, 4 YRS PRO) - 12.2 PPG, 6.5 APG, 6.8 RPG"""
    },
    {
        "name": "Cleveland Cavaliers",
        "id": "1610612739",
        "url": "https://www.nba.com/cavaliers/roster",
        "markdown": """## Cleveland Cavaliers Roster

Players include:
- Donovan Mitchell (#45, Guard, 6'1", 215 lbs, Age 29, 8 YRS PRO) - 24.4 PPG, 4.4 APG, 3.1 RPG
- Darius Garland (#10, Guard, 6'1", 192 lbs, Age 25, 6 YRS PRO) - 16.9 PPG, 5.9 APG, 2.1 RPG
- Evan Mobley (#4, Forward-Center, 7'0", 215 lbs, Age 24, 4 YRS PRO) - 16.6 PPG, 2.7 APG, 9 RPG
- Jarrett Allen (#31, Center, 6'11", 243 lbs, Age 27, 8 YRS PRO) - 12.8 PPG, 1.8 APG, 9.9 RPG"""
    },
    {
        "name": "Detroit Pistons",
        "id": "1610612765",
        "url": "https://www.nba.com/pistons/roster",
        "markdown": """## Detroit Pistons Roster

Players include:
- Cade Cunningham (#2, Guard, 6'6", 220 lbs, Age 24, 4 YRS PRO) - 24.6 PPG, 9.2 APG, 6.7 RPG
- Jaden Ivey (#23, Guard, 6'4", 195 lbs, Age 23, 3 YRS PRO) - 16.2 PPG, 3.8 APG, 4 RPG
- Tobias Harris (#12, Forward, 6'7", 226 lbs, Age 33, 14 YRS PRO) - 10.6 PPG, 2.1 APG, 5.7 RPG"""
    },
    {
        "name": "Indiana Pacers",
        "id": "1610612754",
        "url": "https://www.nba.com/pacers/roster",
        "markdown": """## Indiana Pacers Roster

Players include:
- Tyrese Haliburton (#0, Guard, 6'5", 185 lbs, Age 25, 5 YRS PRO) - 16.4 PPG, 9.2 APG, 3.5 RPG
- Pascal Siakam (#43, Forward, 6'9", 230 lbs, Age 31, 9 YRS PRO) - 19.6 PPG, 3.9 APG, 7.3 RPG
- Myles Turner (#33, Center, 6'11", 250 lbs, Age 29, 10 YRS PRO) - 14.9 PPG, 1.2 APG, 6.9 RPG
- Bennedict Mathurin (#00, Guard, 6'6", 210 lbs, Age 23, 3 YRS PRO) - 17.4 PPG, 2.1 APG, 6.6 RPG"""
    },
    {
        "name": "Milwaukee Bucks",
        "id": "1610612749",
        "url": "https://www.nba.com/bucks/roster",
        "markdown": """## Milwaukee Bucks Roster

Players include:
- Giannis Antetokounmpo (#34, Forward, 6'11", 243 lbs, Age 30, 12 YRS PRO) - 31.7 PPG, 6.2 APG, 12.2 RPG
- Damian Lillard (#0, Guard, 6'2", 195 lbs, Age 35, 13 YRS PRO) - 24.3 PPG, 7.1 APG, 4.4 RPG
- Khris Middleton (#22, Forward, 6'7", 222 lbs, Age 34, 13 YRS PRO) - 12.2 PPG, 4.8 APG, 4 RPG"""
    },
    {
        "name": "Atlanta Hawks",
        "id": "1610612737",
        "url": "https://www.nba.com/hawks/roster",
        "markdown": """## Atlanta Hawks Roster

Players include:
- Trae Young (#11, Guard, 6'1", 164 lbs, Age 27, 7 YRS PRO) - 20.9 PPG, 11.4 APG, 3.5 RPG
- Jalen Johnson (#1, Forward, 6'8", 220 lbs, Age 24, 4 YRS PRO) - 19.6 PPG, 5.4 APG, 10.7 RPG
- Clint Capela (#15, Center, 6'10", 256 lbs, Age 31, 11 YRS PRO) - 10.5 PPG, 0.9 APG, 9.4 RPG
- Dyson Daniels (#5, Guard, 6'7", 200 lbs, Age 22, 3 YRS PRO) - 13.3 PPG, 3.5 APG, 4.8 RPG"""
    },
    {
        "name": "Charlotte Hornets",
        "id": "1610612766",
        "url": "https://www.nba.com/hornets/roster",
        "markdown": """## Charlotte Hornets Roster

Players include:
- LaMelo Ball (#1, Guard, 6'7", 180 lbs, Age 24, 5 YRS PRO) - 29.3 PPG, 7.3 APG, 5.4 RPG
- Brandon Miller (#24, Forward, 6'9", 200 lbs, Age 22, 2 YRS PRO) - 18.8 PPG, 2.5 APG, 4.1 RPG
- Miles Bridges (#0, Forward, 6'6", 225 lbs, Age 27, 7 YRS PRO) - 16.6 PPG, 2.8 APG, 6.9 RPG"""
    },
    {
        "name": "Miami Heat",
        "id": "1610612748",
        "url": "https://www.nba.com/heat/roster",
        "markdown": """## Miami Heat Roster

Players include:
- Tyler Herro (#14, Guard, 6'5", 195 lbs, Age 25, 6 YRS PRO) - 24.1 PPG, 5.2 APG, 5.3 RPG
- Bam Adebayo (#13, Center-Forward, 6'9", 255 lbs, Age 28, 7 YRS PRO) - 16 PPG, 4.5 APG, 9.3 RPG
- Terry Rozier (#2, Guard, 6'1", 190 lbs, Age 31, 10 YRS PRO) - 12.3 PPG, 4.1 APG, 3.7 RPG"""
    },
    {
        "name": "Orlando Magic",
        "id": "1610612753",
        "url": "https://www.nba.com/magic/roster",
        "markdown": """## Orlando Magic Roster

Players include:
- Paolo Banchero (#5, Forward, 6'10", 250 lbs, Age 23, 3 YRS PRO) - 28.8 PPG, 5.6 APG, 8.6 RPG
- Franz Wagner (#22, Forward, 6'9", 220 lbs, Age 24, 4 YRS PRO) - 24.2 PPG, 5.5 APG, 5.6 RPG
- Jalen Suggs (#4, Guard, 6'4", 205 lbs, Age 24, 4 YRS PRO) - 15.3 PPG, 4.3 APG, 4.2 RPG
- Wendell Carter Jr. (#34, Center-Forward, 6'10", 270 lbs, Age 26, 7 YRS PRO) - 7.4 PPG, 2.1 APG, 7 RPG"""
    },
    {
        "name": "Washington Wizards",
        "id": "1610612764",
        "url": "https://www.nba.com/wizards/roster",
        "markdown": """## Washington Wizards Roster

Players include:
- Jordan Poole (#13, Guard, 6'4", 194 lbs, Age 26, 6 YRS PRO) - 20 PPG, 4.4 APG, 2.9 RPG
- Kyle Kuzma (#33, Forward, 6'9", 221 lbs, Age 30, 8 YRS PRO) - 15.8 PPG, 3.7 APG, 5.6 RPG
- Jonas Valančiūnas (#17, Center, 6'11", 265 lbs, Age 33, 13 YRS PRO) - 11 PPG, 2 APG, 7.8 RPG
- Bilal Coulibaly (#0, Guard-Forward, 6'6", 195 lbs, Age 21, 2 YRS PRO) - 11.4 PPG, 3.6 APG, 5 RPG"""
    },
    {
        "name": "Denver Nuggets",
        "id": "1610612743",
        "url": "https://www.nba.com/nuggets/roster",
        "markdown": """## Denver Nuggets Roster

Players include:
- Nikola Jokić (#15, Center, 7'0", 284 lbs, Age 30, 10 YRS PRO) - 28.1 PPG, 9.5 APG, 13.7 RPG
- Jamal Murray (#27, Guard, 6'4", 215 lbs, Age 28, 8 YRS PRO) - 17.9 PPG, 5.2 APG, 4.1 RPG
- Michael Porter Jr. (#1, Forward, 6'10", 218 lbs, Age 27, 6 YRS PRO) - 16.7 PPG, 1.8 APG, 6.6 RPG
- Russell Westbrook (#4, Guard, 6'3", 200 lbs, Age 37, 17 YRS PRO) - 10.6 PPG, 6.3 APG, 4.4 RPG"""
    },
    {
        "name": "Minnesota Timberwolves",
        "id": "1610612750",
        "url": "https://www.nba.com/timberwolves/roster",
        "markdown": """## Minnesota Timberwolves Roster

Players include:
- Anthony Edwards (#5, Guard, 6'4", 225 lbs, Age 24, 5 YRS PRO) - 25.7 PPG, 4.9 APG, 5.4 RPG
- Julius Randle (#30, Forward-Center, 6'8", 250 lbs, Age 31, 11 YRS PRO) - 21 PPG, 4.5 APG, 8 RPG
- Rudy Gobert (#27, Center, 7'1", 258 lbs, Age 33, 12 YRS PRO) - 9.7 PPG, 1.5 APG, 9.6 RPG
- Donte DiVincenzo (#0, Guard, 6'4", 203 lbs, Age 28, 7 YRS PRO) - 10.5 PPG, 3.6 APG, 3.5 RPG"""
    },
    {
        "name": "Oklahoma City Thunder",
        "id": "1610612760",
        "url": "https://www.nba.com/thunder/roster",
        "markdown": """## Oklahoma City Thunder Roster

Players include:
- Shai Gilgeous-Alexander (#2, Guard, 6'6", 195 lbs, Age 27, 7 YRS PRO) - 30.3 PPG, 6.1 APG, 5.4 RPG
- Jalen Williams (#8, Forward, 6'5", 195 lbs, Age 24, 3 YRS PRO) - 21.4 PPG, 5.5 APG, 5.5 RPG
- Chet Holmgren (#7, Center-Forward, 7'1", 195 lbs, Age 23, 2 YRS PRO) - 20.7 PPG, 2.5 APG, 10.1 RPG
- Isaiah Hartenstein (#55, Center-Forward, 7'0", 250 lbs, Age 27, 7 YRS PRO) - 10.3 PPG, 3.7 APG, 11.8 RPG"""
    },
    {
        "name": "Portland Trail Blazers",
        "id": "1610612757",
        "url": "https://www.nba.com/blazers/roster",
        "markdown": """## Portland Trail Blazers Roster

Players include:
- Anfernee Simons (#1, Guard, 6'3", 181 lbs, Age 26, 7 YRS PRO) - 17.8 PPG, 4.4 APG, 3.1 RPG
- Shaedon Sharpe (#17, Guard, 6'5", 200 lbs, Age 22, 3 YRS PRO) - 16.6 PPG, 2.7 APG, 3.2 RPG
- Deandre Ayton (#2, Center, 7'0", 250 lbs, Age 27, 7 YRS PRO) - 14.5 PPG, 1.9 APG, 10.9 RPG
- Jerami Grant (#9, Forward, 6'7", 210 lbs, Age 31, 11 YRS PRO) - 15.2 PPG, 2.4 APG, 3.4 RPG"""
    },
    {
        "name": "Utah Jazz",
        "id": "1610612762",
        "url": "https://www.nba.com/jazz/roster",
        "markdown": """## Utah Jazz Roster

Players include:
- Lauri Markkanen (#23, Forward, 7'0", 240 lbs, Age 28, 8 YRS PRO) - 18.7 PPG, 2 APG, 6.5 RPG
- Keyonte George (#3, Guard, 6'4", 185 lbs, Age 21, 2 YRS PRO) - 16.3 PPG, 5.9 APG, 3.3 RPG
- Collin Sexton (#2, Guard, 6'1", 190 lbs, Age 27, 7 YRS PRO) - 16.9 PPG, 3.8 APG, 2.8 RPG
- Walker Kessler (#24, Center, 7'1", 245 lbs, Age 24, 3 YRS PRO) - 9.4 PPG, 1 APG, 10.3 RPG"""
    },
    {
        "name": "Golden State Warriors",
        "id": "1610612744",
        "url": "https://www.nba.com/warriors/roster",
        "markdown": """## Golden State Warriors Roster

Players include:
- Stephen Curry (#30, Guard, 6'2", 185 lbs, Age 37, 16 YRS PRO) - 28.8 PPG, 3.9 APG, 3.5 RPG
- Draymond Green (#23, Forward, 6'6", 230 lbs, Age 35, 13 YRS PRO) - 8.1 PPG, 5.8 APG, 5.8 RPG
- Jimmy Butler III (#10, Forward, 6'6", 230 lbs, Age 36, 14 YRS PRO) - 19.9 PPG, 4.9 APG, 5.6 RPG
- Jonathan Kuminga (#1, Forward, 6'7", 225 lbs, Age 23, 4 YRS PRO) - 13.8 PPG, 2.8 APG, 6.6 RPG
- Brandin Podziemski (#2, Guard, 6'4", 205 lbs, Age 22, 2 YRS PRO) - 12.1 PPG, 2.9 APG, 4.6 RPG"""
    },
    {
        "name": "LA Clippers",
        "id": "1610612746",
        "url": "https://www.nba.com/clippers/roster",
        "markdown": """## LA Clippers Roster

Players include:
- James Harden (#1, Guard, 6'5", 220 lbs, Age 36, 16 YRS PRO) - 27.8 PPG, 8.4 APG, 5.8 RPG
- Kawhi Leonard (#2, Forward, 6'6", 225 lbs, Age 34, 14 YRS PRO) - 23.7 PPG, 3.3 APG, 5.3 RPG
- Ivica Zubac (#40, Center, 7'0", 240 lbs, Age 28, 9 YRS PRO) - 17 PPG, 2.4 APG, 11.6 RPG
- Brook Lopez (#11, Center, 7'1", 282 lbs, Age 37, 17 YRS PRO) - 6.3 PPG, 0.5 APG, 1.9 RPG"""
    },
    {
        "name": "Los Angeles Lakers",
        "id": "1610612747",
        "url": "https://www.nba.com/lakers/roster",
        "markdown": """## Los Angeles Lakers Roster

Players include:
- LeBron James (#23, Forward, 6'9", 250 lbs, Age 40, 22 YRS PRO) - 14 PPG, 10 APG, 4.5 RPG
- Austin Reaves (#15, Guard, 6'5", 197 lbs, Age 27, 4 YRS PRO) - 27.6 PPG, 7.3 APG, 5.5 RPG
- Luka Dončić (#77, Forward-Guard, 6'8", 230 lbs, Age 26, 7 YRS PRO) - 34.5 PPG, 8.9 APG, 8.8 RPG
- Deandre Ayton (#5, Center, 7'0", 252 lbs, Age 27, 7 YRS PRO) - 15.5 PPG, 0.9 APG, 8.4 RPG
- Bronny James (#9, Guard, 6'2", 210 lbs, Age 21, 1 YRS PRO) - 2.1 PPG, 1.8 APG, 0.9 RPG"""
    },
    {
        "name": "Phoenix Suns",
        "id": "1610612756",
        "url": "https://www.nba.com/suns/roster",
        "markdown": """## Phoenix Suns Roster

Players include:
- Devin Booker (#1, Guard, 6'5", 206 lbs, Age 29, 10 YRS PRO) - 26.4 PPG, 6.9 APG, 4.1 RPG
- Grayson Allen (#8, Guard, 6'3", 198 lbs, Age 30, 7 YRS PRO) - 18.5 PPG, 4.3 APG, 3.1 RPG
- Ryan Dunn (#0, Forward, 6'7", 216 lbs, Age 22, 1 YRS PRO) - 8.4 PPG, 1.9 APG, 4.8 RPG
- Mark Williams (#15, Center, 7'1", 240 lbs, Age 23, 3 YRS PRO) - 12.3 PPG, 0.9 APG, 8.4 RPG"""
    },
    {
        "name": "Sacramento Kings",
        "id": "1610612758",
        "url": "https://www.nba.com/kings/roster",
        "markdown": """## Sacramento Kings Roster

Players include:
- De'Aaron Fox (#5, Guard, 6'3", 175 lbs, Age 32, 12 YRS PRO) - 12.4 PPG, 6 APG, 3.7 RPG
- DeMar DeRozan (#10, Guard-Forward, 6'6", 220 lbs, Age 36, 16 YRS PRO) - 18.7 PPG, 3.6 APG, 3.1 RPG
- Domantas Sabonis (#11, Forward-Center, 6'10", 240 lbs, Age 29, 9 YRS PRO) - 17.2 PPG, 3.7 APG, 12.3 RPG
- Zach LaVine (#8, Guard, 6'5", 200 lbs, Age 30, 11 YRS PRO) - 20.5 PPG, 2.2 APG, 3.3 RPG"""
    },
    {
        "name": "Dallas Mavericks",
        "id": "1610612742",
        "url": "https://www.nba.com/mavericks/roster",
        "markdown": """## Dallas Mavericks Roster

Players include:
- Kyrie Irving (#11, Guard, 6'2", 195 lbs, Age 33, 14 YRS PRO)
- Klay Thompson (#31, Guard, 6'5", 220 lbs, Age 35, 14 YRS PRO) - 10.3 PPG, 1.5 APG, 2.4 RPG
- P.J. Washington (#25, Forward, 6'7", 230 lbs, Age 27, 6 YRS PRO) - 15.7 PPG, 2.3 APG, 7.8 RPG
- Anthony Davis (#3, Forward-Center, 6'10", 253 lbs, Age 32, 13 YRS PRO) - 20.8 PPG, 2.2 APG, 10.2 RPG
- Cooper Flagg (#32, Forward, 6'9", 205 lbs, Age 18, R) - 15.9 PPG, 3.1 APG, 6.4 RPG"""
    },
    {
        "name": "Houston Rockets",
        "id": "1610612745",
        "url": "https://www.nba.com/rockets/roster",
        "markdown": """## Houston Rockets Roster

Players include:
- Alperen Sengun (#28, Center, 6'11", 243 lbs, Age 23, 4 YRS PRO) - 22.4 PPG, 5.5 RPG, 7.1 APG
- Fred VanVleet (#23, Guard)
- Kevin Durant (#35, Forward)
- Jalen Green (#4, Guard, 6'4", 186 lbs, Age 23, 4 YRS PRO) - 15.5 PPG, 2 APG, 2 RPG"""
    },
    {
        "name": "Memphis Grizzlies",
        "id": "1610612763",
        "url": "https://www.nba.com/grizzlies/roster",
        "markdown": """## Memphis Grizzlies Roster

Players include:
- Ja Morant (#12, Guard, 6'2", 174 lbs, Age 26, 6 YRS PRO) - 17.9 PPG, 7.6 APG, 3.5 RPG
- Jaren Jackson Jr. (#8, Forward-Center, 6'10", 242 lbs, Age 26, 7 YRS PRO) - 17.8 PPG, 1.6 APG, 5.3 RPG
- Santi Aldama (#7, Forward-Center, 7'0", 215 lbs, Age 24, 4 YRS PRO) - 13.8 PPG, 2.8 APG, 6.7 RPG
- Zach Edey (#14, Center, 7'3", 305 lbs, Age 23, 1 YRS PRO) - 10.2 PPG, 1 APG, 7.6 RPG"""
    },
    {
        "name": "New Orleans Pelicans",
        "id": "1610612740",
        "url": "https://www.nba.com/pelicans/roster",
        "markdown": """## New Orleans Pelicans Roster

Players include:
- Zion Williamson (#1, Forward, 6'6", 284 lbs, Age 25, 6 YRS PRO) - 21.4 PPG, 4.3 APG, 6.1 RPG
- Trey Murphy III (#25, Forward, 6'8", 206 lbs, Age 25, 4 YRS PRO) - 20.2 PPG, 3 APG, 6.4 RPG
- Jeremiah Fears (#0, Guard, 6'3", 190 lbs, Age 19, R) - 15.4 PPG, 2.7 APG, 3.2 RPG
- Derik Queen (#22, Center, 6'9", 250 lbs, Age 20, R) - 12.6 PPG, 3.2 APG, 6.6 RPG"""
    },
    {
        "name": "San Antonio Spurs",
        "id": "1610612759",
        "url": "https://www.nba.com/spurs/roster",
        "markdown": """## San Antonio Spurs Roster

Players include:
- Victor Wembanyama (#1, Forward-Center, 7'4", 235 lbs, Age 21, 2 YRS PRO) - 26.2 PPG, 4 APG, 12.9 RPG
- Dylan Harper (#2, Guard, 6'5", 215 lbs, Age 19, R) - 14 PPG, 3.8 APG, 4 RPG
- Stephon Castle (#5, Guard, 6'6", 215 lbs, Age 21, 1 YRS PRO) - 17.3 PPG, 7.5 APG, 5.8 RPG
- Harrison Barnes (#40, Forward, 6'7", 225 lbs, Age 33, 13 YRS PRO) - 12.9 PPG, 2.2 APG, 3.1 RPG"""
    }
]

if __name__ == "__main__":
    print("=" * 80)
    print("SAVING ALL 30 NBA TEAM ROSTERS TO MEMVID PIPELINE")
    print("=" * 80)
    print(f"\nTarget directory: {SCRAPED_DIR}")
    print(f"Total teams: {len(teams_data)}\n")

    saved_count = 0
    for team in teams_data:
        try:
            save_team_roster(team["name"], team["id"], team["url"], team["markdown"])
            saved_count += 1
        except Exception as e:
            print(f"✗ Error saving {team['name']}: {e}")

    print(f"\n{'=' * 80}")
    print(f"✅ Successfully saved {saved_count}/{len(teams_data)} team rosters")
    print(f"{'=' * 80}")
    print(f"\nNext steps:")
    print(f"1. Run: python memvid_integration/text_pipeline/encode_to_memvid.py --name nba-players")
    print(f"2. Verify memory in: /backend/memories/nba-players/")
    print(f"3. Query the memory to test retrieval")
