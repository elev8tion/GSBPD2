#!/usr/bin/env python3
"""
Load NFL player fumbles statistics into Kre8VidMems
Extracted from 56 screenshots
"""

import os
import sys
from pathlib import Path
from typing import Dict, Any

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent))

from lib.kre8vidmems.kre8vidmems.api.memory import Kre8VidMemory


def format_player_fumbles_stats(player: Dict[str, Any]) -> str:
    """Format player fumbles stats for memory storage with performance tags"""
    name = player.get('player', 'Unknown')
    ff = player.get('ff', 0)
    fr = player.get('fr', 0)
    fr_td = player.get('fr_td', 0)

    # Base stats text
    text = f"NFL Player Fumbles Stats | {name}"
    text += f" | FF (Forced Fumbles): {ff}"
    text += f" | FR (Fumble Recoveries): {fr}"
    text += f" | FR TD (Fumble Recovery TDs): {fr_td}"

    # Performance-based tags for defensive playmakers
    if ff >= 3:
        text += f" | elite ball hawk | {name} elite defender | turnover machine | pro bowl candidate"
    elif ff >= 2:
        text += f" | impact defender | {name} playmaker | turnover specialist"
    elif ff >= 1:
        text += f" | solid defender | {name} opportunistic | creates turnovers"

    # Fumble recovery specialist tags
    if fr >= 3:
        text += f" | fumble recovery specialist | {name} elite recovery | always around the ball"
    elif fr >= 2:
        text += f" | opportunistic defender | {name} good hands | ball hawk"
    elif fr >= 1:
        text += f" | alert defender | {name} awareness | recovers fumbles"

    # TD scorer from fumbles
    if fr_td >= 1:
        text += f" | touchdown scorer | {name} defensive TD | game changer | scoring threat"

    # Combined impact
    total_impact = ff + fr + (fr_td * 2)
    if total_impact >= 5:
        text += f" | defensive MVP candidate | {name} game wrecker | elite impact player"
    elif total_impact >= 3:
        text += f" | high impact defender | {name} difference maker | creates turnovers"

    return text


# All player data
players = [
    # Screenshot 1
    {"player": "CeeDee Lamb", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Travis Kelce", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Tee Higgins", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "DeAndre Washington", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Brandin Cooks", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Brandon Aiyuk", "ff": 0, "fr": 1, "fr_td": 0},
    {"player": "Davante Adams", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Alec Ingold", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "DeVante Adams", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Tyreek Hill", "ff": 0, "fr": 1, "fr_td": 0},
    {"player": "Jaylen Warren", "ff": 0, "fr": 1, "fr_td": 0},
    {"player": "Stefon Diggs", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Tee Higgins", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Christian Kirk", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "George Kittle", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Jamarr Chase", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Tyreek Hill", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Davante Adams", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Samson Ebukam", "ff": 1, "fr": 0, "fr_td": 0},
    {"player": "Mike Evans", "ff": 0, "fr": 0, "fr_td": 0},

    # Screenshot 2
    {"player": "Rashod Bateman", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Darius Stills", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Tee Higgins", "ff": 0, "fr": 1, "fr_td": 0},
    {"player": "David Njoku", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Trevion Bradford", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Cole Kmet", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Antonio Gibson", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Jayson Moore II", "ff": 0, "fr": 1, "fr_td": 0},
    {"player": "Gideon Greeley", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Chris Green", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Dallas Goedert", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Isaiah Likely", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Peyton Barber", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Malik Williams", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Kaden Ellis", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Josh Dotson", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Daryl Williams", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Christian Benford", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Julius Johnson", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Zaire Kelly", "ff": 0, "fr": 0, "fr_td": 0},

    # Screenshot 3
    {"player": "Byron Murphy", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Myles Murphy", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Byron Murphy II", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Kenneth Murray, Jr.", "ff": 0, "fr": 1, "fr_td": 0},
    {"player": "Eric Murray", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Malik Mustapha", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "PJ Mustipher", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Jason Myers", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Malik Nabors", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Jalen Nailor", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Dusell Nehami", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Siran Neal", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Greg Newsome II", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Josh Newton", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Bilal Nichols", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Law Nichols III", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Perry Nickerson", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Nick Niemann", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Keisean Nixon", "ff": 0, "fr": 1, "fr_td": 0},
    {"player": "Maema Njongmeta", "ff": 0, "fr": 0, "fr_td": 0},

    # Screenshot 4
    {"player": "Darreck Nxadi", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Walter Nolen", "ff": 0, "fr": 1, "fr_td": 1},
    {"player": "Comar Norman-Lott", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Joe Noteboom", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Trevor Nowsaki", "ff": 0, "fr": 1, "fr_td": 0},

    # Screenshot 5
    {"player": "Tyler Nubin", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Rakeem Nunez-Roches", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Uchenna Nwosu", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Patrick O'Connell", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Pat O'Connor", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Days Olayesinigba", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Osa Odighizuwa", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Emmanuel Ogbah", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Aimen Ogbondaire", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Olti Ogborna", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Andrew Ogletree", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Dame Ogunbowale", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Larry Ogunsakin", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "David Okaibe", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Moro Ojomo", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Ameez Qulain", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "BJ Ojulari", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Ty Okada", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Bobby Okamikie", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Chaj Okorafor", "ff": 0, "fr": 0, "fr_td": 0},

    # Screenshot 6
    {"player": "Basil Okoye", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Jeff Okudah", "ff": 0, "fr": 1, "fr_td": 0},
    {"player": "Kiari Oluadapo", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Chukcwhufuma Oledapo", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Chris Olave", "ff": 0, "fr": 0, "fr_td": 0},

    # Screenshot 7
    {"player": "Bryce Oliver", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Isaiah Oliver", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Sagan Olshi", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Charles Omemchu", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Mike Onwenu", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "David Onyemate", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Ruke Orhotomo", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Amaur Onaweriye", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Matthew Orzech", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Esezi Otomewo", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Connor O'Toole", "ff": 0, "fr": 1, "fr_td": 0},
    {"player": "Cadie Otton", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Robbie Outts", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "DeMaryon Overshaw", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Olafu Oweh", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Jonathan Owens", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Tyler Owens", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Ivan Pace Jr.", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Josh Palmer", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Owen Pappoe", "ff": 0, "fr": 0, "fr_td": 0},

    # Screenshot 8
    {"player": "Jacob Parrish", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Tim Patrick", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Riley Patterson", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Karly Paye", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Rico Payton", "ff": 0, "fr": 0, "fr_td": 0},

    # Screenshot 9
    {"player": "Ricky Pearsal", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Aeneas Peebles", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "JJ Pegues", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Mike Perrell", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Jabulli Peppers", "ff": 0, "fr": 1, "fr_td": 0},
    {"player": "Seroge Perine", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "David Perryman", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Jeremiah Pharma Jr.", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Asdru Phillips", "ff": 0, "fr": 1, "fr_td": 0},
    {"player": "Dal'Shawn Phillips", "ff": 0, "fr": 1, "fr_td": 0},
    {"player": "Jardan Phillips", "ff": 0, "fr": 2, "fr_td": 0},
    {"player": "Jordan Phillips", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Jordan Phillips", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Clark Phillips III", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "George Pickora", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Alec Pierce", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "James Pierre", "ff": 0, "fr": 1, "fr_td": 1},
    {"player": "Bradley Pinion", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Jason Pinnock", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Jalen Pitra", "ff": 0, "fr": 0, "fr_td": 0},

    # Screenshot 10
    {"player": "Anthony Pittman", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Sarah Pola-Mao", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Elijah Punder", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Garian Porter", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Joey Porter Jr.", "ff": 0, "fr": 0, "fr_td": 0},

    # Screenshot 11
    {"player": "Jackson Powers-Johnson", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Jordan Poyer", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Germaine Pratt", "ff": 0, "fr": 1, "fr_td": 0},
    {"player": "Adam Prentice", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Oak Prescott", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Nehemiah Pritchett", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Dominick Puri", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Jalen Ramsey", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Shalon Rankins", "ff": 0, "fr": 1, "fr_td": 1},
    {"player": "Taylor Rapp", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Spencer Rattler", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "LaRyan Ray", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "OJ Reader", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Jeremy Reaves", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Haason Reddick", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Jarran Reed", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Jaylen Reed", "ff": 0, "fr": 1, "fr_td": 0},
    {"player": "Nikko Reed", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Troy Reeder", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Jarrick Reed II", "ff": 0, "fr": 0, "fr_td": 0},

    # Screenshot 12
    {"player": "Justin Reid", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Kaarre Reid", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Shannon Revel Jr.", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Craig Reynolds", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Josh Reynolds", "ff": 0, "fr": 0, "fr_td": 0},

    # Screenshot 13
    {"player": "Jim Rhattigan", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Luke Rhodes", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Sean Rhyan", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Patrick Ricari", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Monty Rice", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Decameron Richardson", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Demian Richardson", "ff": 0, "fr": 1, "fr_td": 0},
    {"player": "Bo Richter", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "John Ridgeway", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Xeles Ringe", "ff": 0, "fr": 1, "fr_td": 0},
    {"player": "Jalen Rivers", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Malcolm Roach", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Glandon Roberts", "ff": 0, "fr": 1, "fr_td": 0},
    {"player": "Elijah Roberts", "ff": 0, "fr": 1, "fr_td": 0},
    {"player": "Sam Roberts", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Roy Robertson-Harris", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "A'Shawn Robinson", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Chop Robinson", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Curtis Robinson", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Garuus Robinson", "ff": 0, "fr": 0, "fr_td": 0},

    # Screenshot 14
    {"player": "Dominique Robinson", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Mark Robinson", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Micah Robinson", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Guc Robinson", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Ty Robinson", "ff": 0, "fr": 0, "fr_td": 0},

    # Screenshot 15
    {"player": "Wan'Dale Robinson", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Robert Rochell", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Levi Drake Rodriguez", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Malcolm Rodriguez", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Chris Rodriguez Jr.", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Christian Roland-Wallace", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "D'Angelo Ross", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Jalen Royals", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Hayden Rucci", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Jeremy Ruckert", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Carter Rummon", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Brady Russell", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Mike Sanrietti", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Cameron Sample", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Drew Sample", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Dylan Sampson", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Curtis Samuel", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Deloui Samuel Sr.", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Jack Sanborn", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Ja'Tavion Sanders", "ff": 0, "fr": 0, "fr_td": 0},

    # Screenshot 16
    {"player": "Sheldur Sanders", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "T.J. Sanders", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Jonas Sarker", "ff": 0, "fr": 1, "fr_td": 0},
    {"player": "Eric Saubert", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Khalen Saunders", "ff": 0, "fr": 0, "fr_td": 0},

    # Screenshot 17
    {"player": "Jonah Savaiama", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Jack Sawyer", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Jacob Saylors", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Branden Schuler", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Luke Schoonmaker", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Dalton Schultz", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Carson Schwesinger", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Daniel Scott", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Nick Scott", "ff": 0, "fr": 1, "fr_td": 0},
    {"player": "Javier Scott", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Nic Scoutrion", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Trey Sermon", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Tim Settle", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Rashid Shaheed", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Khalil Shakir", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Tyrell Shavers", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Kendall Sheffield", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Nathan Shepherd", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Trent Sherfield", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Jamie Sherrill", "ff": 0, "fr": 0, "fr_td": 0},

    # Screenshot 18
    {"player": "Jamien Sherwood", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Will Shipley", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Justin Shorter", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Tyler Siaugh", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Trent Sieg", "ff": 0, "fr": 1, "fr_td": 0},

    # Screenshot 19
    {"player": "Zach Sieler", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Manyese Style", "ff": 0, "fr": 1, "fr_td": 0},
    {"player": "Elijah Simmons", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Jodii Simmons", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Taonton Simpson", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Devin Singletary", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Jackson Simmon", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "JL Skinner", "ff": 0, "fr": 1, "fr_td": 0},
    {"player": "Bian Slowoosiak", "ff": 0, "fr": 1, "fr_td": 0},
    {"player": "Tadarrell Statum", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Darius Slay", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Joey Slye", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Stone Smart", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Arian Smith", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Jaylin Smith", "ff": 0, "fr": 1, "fr_td": 0},
    {"player": "Masson Smith", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Madi Smith", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Preston Smith", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Breognn Smith", "ff": 0, "fr": 1, "fr_td": 1},
    {"player": "Tremón Smith", "ff": 0, "fr": 0, "fr_td": 0},

    # Screenshot 20
    {"player": "Tyree Smith", "ff": 0, "fr": 1, "fr_td": 0},
    {"player": "Xavier Smith", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Za'Darius Smith", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Chris Smith II", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Jason Smith-Nigba", "ff": 0, "fr": 0, "fr_td": 0},

    # Screenshot 21
    {"player": "Chau Smith-Wade", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Damuane Snoot", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "LChariss Snoot", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Charles Snowden", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Jason Solomon", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Barryn Sorell", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Brwyn Sparr-Fund", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Tyast Spears", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Baylor Spector", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "E.J. Speed", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Omar Speights", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Nazir Stackhouse", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Sarah Stabford", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Maldi Starks", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Amon-Ra St. Brown", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Branidon Stephens", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Grover Stewart", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Josiah Stewart", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Shemar Stewart", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Gwaertez Stiggers", "ff": 0, "fr": 0, "fr_td": 0},

    # Screenshot 22
    {"player": "Tahsol Still", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Jack Stoll", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Goro Stone", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Jordan Stout", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Xantavious Street", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Laren Strickland", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Danny Striggrow", "ff": 0, "fr": 1, "fr_td": 0},
    {"player": "Justin Strnad", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Dorian Strong", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Grant Stuard", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Danny Stutsman", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Ty Summers", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Rex Sunshara", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Charz Sunrell", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Pat Sustain II", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Courtland Sutton", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "T'Vondre Sweat", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Bradyn Swinson", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "T.J. Tampa", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "JaRani Tavai", "ff": 0, "fr": 0, "fr_td": 0},

    # Screenshot 23
    {"player": "Alanidat Taylor", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Darrell Taylor", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Ja'Sir Taylor", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Jonathan Taylor", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Keith Taylor", "ff": 0, "fr": 0, "fr_td": 0},

    # Screenshot 24
    {"player": "Tory Taylor", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Cam Taylor-Britt", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Leonard Taylor III", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Dalton Taylor-Demerson", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "A.J. Terrell", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Kayan Thibodeaux", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Azarryah Thomas", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Cameron Thomas", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Daniel Thomas", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Drake Thomas", "ff": 0, "fr": 1, "fr_td": 0},
    {"player": "Ian Thomas", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Juanyeh Thomas", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Rodiney Thomas", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Tristan Thomas", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Brian Thomas Jr.", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Jisan Thornhill", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Dari'S Thornton Jr.", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Jerry Tillery", "ff": 0, "fr": 1, "fr_td": 0},
    {"player": "Gordrea Tillman", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Tommy Togiai", "ff": 0, "fr": 0, "fr_td": 0},

    # Screenshot 25
    {"player": "Jay Toia", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Galvin Tomkinson", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Keynte Tonga", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Jake Tonges", "ff": 0, "fr": 0, "fr_td": 0},

    # Screenshot 26 (Navigation bar screenshot - skipped)

    # Screenshot 27
    {"player": "Robert Toryan", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Henry Teftrio", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Austin Trammell", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Duve Tranquill", "ff": 0, "fr": 1, "fr_td": 0},
    {"player": "Adam Trastrean", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Layden Traudewell", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Brycen Tremayne", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Tommy Tremble", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Jeremiah Trotter Jr.", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Joe Tryon-Shoyinka", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Tim Trucker", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Jay Tufele", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "JT Tuimoidau", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Marlon Tuipulotu", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Josh Tupou", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Dallas Turner", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "OJ Turner II", "ff": 0, "fr": 1, "fr_td": 0},
    {"player": "Jordan Turner", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Kobee Turner", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Malik Turner", "ff": 0, "fr": 0, "fr_td": 0},

    # Screenshot 28
    {"player": "Shermar Turner", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Ka'Vontae Turpin", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Shayshul Tuten", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Sky Tuttle", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Joshua Uche", "ff": 0, "fr": 0, "fr_td": 0},

    # Screenshot 29
    {"player": "Brend Urban", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Eyoma Uesariko", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Slone Vaki", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Carrington Valentina", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Greedy Vance", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Andrew Van Ginkel", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Lukas Van Ness", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Kyle Van Noy", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Vita Vea", "ff": 0, "fr": 1, "fr_td": 0},
    {"player": "Kimani Vidal", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Kirda Vider", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Travis Volbick", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Jaylen Waddle", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Bobby Wagner", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "William Wagner", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Daone Walker", "ff": 0, "fr": 1, "fr_td": 0},
    {"player": "Daconttir Walker", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Jahdar Walker", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Mykal Walker", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Quay Walker", "ff": 0, "fr": 0, "fr_td": 0},

    # Screenshot 30
    {"player": "Tavan Walker", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Jesh Wallace", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Tevin Wallace", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Tyler Wallace", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "David Wallow", "ff": 0, "fr": 0, "fr_td": 0},

    # Screenshot 31
    {"player": "Alex Ward", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Charusis Ward", "ff": 0, "fr": 1, "fr_td": 0},
    {"player": "Darnell Ward", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Jay Ward", "ff": 0, "fr": 1, "fr_td": 0},
    {"player": "Shad Ward", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Broderick Washington", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Malik Washington", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Parker Washington", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Tahi Washington", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Trey Washington", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Jaylen Watson", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Luke Wattenberg", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Marless Watts", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Xavier Watts", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Marhuss Wax", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Jori Weaks", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Kristian Welch", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Pete Werner", "ff": 0, "fr": 2, "fr_td": 0},
    {"player": "CJ West", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Nick Westbrook-Ikhine", "ff": 0, "fr": 0, "fr_td": 0},

    # Screenshot 32
    {"player": "Ja'Markus Weston", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Jack Westover", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Tershawn Wharton", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Cody White", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Kellan White", "ff": 0, "fr": 1, "fr_td": 0},

    # Screenshot 33
    {"player": "Ryar White", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Ta'Darious White", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Blake Whitehead", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Nick Whiteside", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Jordan Whittington", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Nate Wiggins", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Elijah Wilkinson", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Jonah Williams", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Chris Williams", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Danson Williams", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Dowen Williams", "ff": 0, "fr": 1, "fr_td": 0},
    {"player": "Elijah Williams", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Evan Williams", "ff": 0, "fr": 1, "fr_td": 0},
    {"player": "James Williams", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Jameson Williams", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Jeanette Williams", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Jonah Williams", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Joshua Williams", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Leonard Williams", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Milton Williams", "ff": 0, "fr": 0, "fr_td": 0},

    # Screenshot 34
    {"player": "Myzel Williams", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Heidi Williams", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Quency Williams", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Jayson Williams", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Trent Williams", "ff": 0, "fr": 0, "fr_td": 0},

    # Screenshot 35
    {"player": "Tydik Williams", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Kendall Williamson", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Brayden Wills", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Emmanuel Wilson", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Garrett Wilson", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Logan Wilson", "ff": 0, "fr": 1, "fr_td": 0},
    {"player": "Mario Wilson", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Payton Wilson", "ff": 0, "fr": 1, "fr_td": 0},
    {"player": "Roman Wilson", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Tones Wilson", "ff": 0, "fr": 1, "fr_td": 0},
    {"player": "James Winchester", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Andrew Wingord", "ff": 0, "fr": 1, "fr_td": 0},
    {"player": "Makti Winge", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Kevin Winston Jr.", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Dee Writers", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Rashad Weadom", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Deatrich Wise", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Devon Witherspoon", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Al'Audis Witherspoon", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Samuel Womack", "ff": 0, "fr": 0, "fr_td": 0},

    # Screenshot 36
    {"player": "D.J. Wonnum", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Zach Wood", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Colby Wooden", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Charles Woods", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Jash Woods", "ff": 0, "fr": 0, "fr_td": 0},

    # Screenshot 37
    {"player": "Xavier Woods", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Craig Woodson", "ff": 0, "fr": 1, "fr_td": 0},
    {"player": "Riq Woolen", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Xavier Worthy", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Nahashan Wright", "ff": 0, "fr": 1, "fr_td": 0},
    {"player": "Devonta Wyatt", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Colben Yarkoff", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Rock Ya-Sin", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Isaac Yadon", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Byron Young", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Danite Young", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Ben Yurasak", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Grey Zabel", "ff": 0, "fr": 0, "fr_td": 0},
    {"player": "Kevin Zeitler", "ff": 0, "fr": 0, "fr_td": 0},
]

def main():
    """Load all fumbles stats into Kre8VidMems"""
    print("Loading NFL Player Fumbles Stats...")
    print(f"Total players: {len(players)}")

    # Create memory instance
    memory = Kre8VidMemory()

    # Process all players
    chunks = []
    for player in players:
        chunk = format_player_fumbles_stats(player)
        chunks.append(chunk)

    # Add summary chunk with top performers
    summary = "NFL Fumbles Stats Summary 2025"

    # Find top forced fumbles
    top_ff = sorted([p for p in players if p['ff'] > 0], key=lambda x: x['ff'], reverse=True)[:10]
    if top_ff:
        summary += "\n\nTop Forced Fumbles Leaders:"
        for p in top_ff:
            summary += f"\n- {p['player']}: {p['ff']} FF"

    # Find top fumble recoveries
    top_fr = sorted([p for p in players if p['fr'] > 0], key=lambda x: x['fr'], reverse=True)[:10]
    if top_fr:
        summary += "\n\nTop Fumble Recovery Leaders:"
        for p in top_fr:
            summary += f"\n- {p['player']}: {p['fr']} FR"

    # Find TD scorers
    td_scorers = [p for p in players if p['fr_td'] > 0]
    if td_scorers:
        summary += "\n\nFumble Recovery TD Scorers:"
        for p in td_scorers:
            summary += f"\n- {p['player']}: {p['fr_td']} TD"

    chunks.append(summary)

    # Load into memory
    print(f"Loading {len(chunks)} chunks into memory...")
    for i, chunk in enumerate(chunks, 1):
        memory.add(chunk)
        if i % 50 == 0:
            print(f"Added {i} chunks (Total: {i})")

    # Save memory
    memory_path = "data/memories/nfl-player-fumbles-stats"
    memory.save(memory_path)
    print(f"✓ Saved fumbles stats to {memory_path.split('/')[-1]}")

    # Print statistics
    print(f"\n✓ All NFL player fumbles stats loaded successfully!")
    print(f"Total players: {len(players)}")
    print(f"\nPlayers with forced fumbles (FF > 0): {sum(1 for p in players if p['ff'] > 0)}")
    print(f"Players with fumble recoveries (FR > 0): {sum(1 for p in players if p['fr'] > 0)}")
    print(f"Players with fumble recovery TDs (FR_TD > 0): {sum(1 for p in players if p['fr_td'] > 0)}")

    # Print top performers
    if top_ff:
        print(f"\nTop 5 Players by Forced Fumbles:")
        for i, p in enumerate(top_ff[:5], 1):
            print(f"{i}. {p['player']}: {p['ff']} FF")

    if top_fr:
        print(f"\nTop 5 Players by Fumble Recoveries:")
        for i, p in enumerate(top_fr[:5], 1):
            print(f"{i}. {p['player']}: {p['fr']} FR")


if __name__ == "__main__":
    main()
