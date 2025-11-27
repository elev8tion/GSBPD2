#!/usr/bin/env python3
"""
Parse NBA roster data from Firecrawl (improved format)
This format has cleaner structure with player data in sections
"""

import re

def parse_roster_markdown_v2(markdown, team_id, team_name):
    """
    Parse roster from improved Firecrawl format
    Each player section starts with an image and contains structured data
    """
    players = []

    # Split by player image markers
    player_sections = re.split(r'!\[.*?\]\(https://cdn\.nba\.com/headshots/nba/latest/260x190/(\d+)\.png\)', markdown)

    # Process pairs (player_id, content)
    for i in range(1, len(player_sections), 2):
        if i + 1 > len(player_sections):
            break

        player_id = player_sections[i]
        content = player_sections[i + 1] if i + 1 < len(player_sections) else ''

        try:
            lines = [l.strip() for l in content.split('\n') if l.strip()]

            player = {
                'team_id': team_id,
                'team_name': team_name,
                'player_id': player_id,
                'name': '',
                'position': '',
                'jersey_number': '',
                'height': '',
                'weight': '',
                'age': 0,
                'experience': '',
                'country': 'USA',
                'ppg': 0.0,
                'rpg': 0.0,
                'apg': 0.0,
                'gp': 0
            }

            # First non-empty line is first name
            # Second non-empty line is last name
            # Third is position
            # Fourth is jersey number

            if len(lines) >= 2:
                player['name'] = f"{lines[0]} {lines[1]}"

            if len(lines) >= 3:
                player['position'] = lines[2]

            if len(lines) >= 4 and lines[3].isdigit():
                player['jersey_number'] = lines[3]

            # Parse remaining fields
            idx = 4
            while idx < len(lines):
                line = lines[idx]

                # Height
                if line == 'Height' and idx + 1 < len(lines):
                    player['height'] = lines[idx + 1].replace('"', '').replace("'", '-').replace('lbs', '').strip()
                    idx += 2
                    continue

                # Weight
                if line == 'Weight' and idx + 1 < len(lines):
                    weight_str = lines[idx + 1].replace('lbs', '').strip()
                    player['weight'] = weight_str
                    idx += 2
                    continue

                # Age
                if line == 'Age' and idx + 1 < len(lines):
                    try:
                        player['age'] = int(lines[idx + 1])
                    except:
                        pass
                    idx += 2
                    continue

                # Years Pro (saved as 'experience' to match UI expectations)
                if line == 'Years Pro' and idx + 1 < len(lines):
                    player['experience'] = lines[idx + 1]
                    idx += 2
                    continue

                # Country
                if line == 'Country' and idx + 1 < len(lines):
                    player['country'] = lines[idx + 1]
                    idx += 2
                    continue

                # GP (Games Played)
                if line == 'GP' and idx + 1 < len(lines):
                    try:
                        val = lines[idx + 1]
                        if val != '-' and val.isdigit():
                            player['gp'] = int(val)
                    except:
                        pass
                    idx += 2
                    continue

                # PPG
                if line == 'PPG' and idx + 1 < len(lines):
                    try:
                        val = lines[idx + 1]
                        if val != '-':
                            player['ppg'] = float(val)
                    except:
                        pass
                    idx += 2
                    continue

                # APG
                if line == 'APG' and idx + 1 < len(lines):
                    try:
                        val = lines[idx + 1]
                        if val != '-':
                            player['apg'] = float(val)
                    except:
                        pass
                    idx += 2
                    continue

                # RPG
                if line == 'RPG' and idx + 1 < len(lines):
                    try:
                        val = lines[idx + 1]
                        if val != '-':
                            player['rpg'] = float(val)
                    except:
                        pass
                    idx += 2
                    continue

                idx += 1

            # Only add if we have a valid name
            if player['name'] and player['name'] != ' ':
                players.append(player)

        except Exception as e:
            print(f"  Error parsing player {player_id}: {e}")
            continue

    return players


# Test with Lakers data
if __name__ == "__main__":
    import json
    from pathlib import Path

    LAKERS_MD = """![Adou Thiero headshot](https://cdn.nba.com/headshots/nba/latest/260x190/1642876.png)

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

Season

GP

2

PPG

3

APG

-

RPG

0.5"""

    players = parse_roster_markdown_v2(LAKERS_MD, "1610612747", "Los Angeles Lakers")

    print(f"Parsed {len(players)} players")
    for p in players:
        print(f"✓ {p['name']:<25} #{p['jersey_number']:<3} {p['position']:<15} GP:{p['gp']:<3} PPG:{p['ppg']:<5.1f} RPG:{p['rpg']:<5.1f} APG:{p['apg']:<5.1f}")

    # Save test
    base_dir = Path(__file__).parent
    output_file = base_dir / "nba_data" / "lakers_parsed_v2.json"

    with open(output_file, 'w') as f:
        json.dump(players, f, indent=2)

    print(f"\n✓ Saved to {output_file}")
