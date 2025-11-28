"""
Odds calculation utilities
Pure math functions - no external dependencies
"""


def american_to_decimal(american_odds):
    """
    Convert American odds to decimal probability

    Args:
        american_odds (int): American odds (e.g., +200, -110)

    Returns:
        float: Decimal probability (0.0 to 1.0)

    Examples:
        >>> american_to_decimal(+200)
        0.333
        >>> american_to_decimal(-110)
        0.524
    """
    if american_odds > 0:
        return 100 / (american_odds + 100)
    else:
        return abs(american_odds) / (abs(american_odds) + 100)


def decimal_to_american(decimal_prob):
    """
    Convert decimal probability to American odds

    Args:
        decimal_prob (float): Probability (0.0 to 1.0)

    Returns:
        int: American odds

    Examples:
        >>> decimal_to_american(0.333)
        +200
        >>> decimal_to_american(0.524)
        -110
    """
    if decimal_prob >= 0.5:
        return int(-(decimal_prob / (1 - decimal_prob)) * 100)
    else:
        return int(((1 - decimal_prob) / decimal_prob) * 100)


def calculate_ev(our_prob, sportsbook_odds):
    """
    Calculate Expected Value (EV) of a bet

    Args:
        our_prob (float): Our calculated probability (0.0 to 1.0)
        sportsbook_odds (int): Sportsbook's American odds

    Returns:
        float: EV as percentage (positive = +EV)

    Examples:
        >>> calculate_ev(0.40, +200)  # We think 40% chance, they offer +200
        20.0  # 20% +EV bet
    """
    # Convert sportsbook odds to payout multiplier
    if sportsbook_odds > 0:
        payout_per_dollar = sportsbook_odds / 100
    else:
        payout_per_dollar = 100 / abs(sportsbook_odds)

    # EV = (our_prob × payout) - (1 - our_prob) × 1
    ev = (our_prob * payout_per_dollar) - (1 - our_prob)
    ev_percent = ev * 100

    return ev_percent


def calculate_parlay_odds(individual_probs, correlation=0.0):
    """
    Calculate parlay probability with optional correlation adjustment

    Args:
        individual_probs (list): List of individual probabilities
        correlation (float): Correlation coefficient (-1.0 to 1.0)

    Returns:
        tuple: (combined_prob, american_odds)

    Examples:
        >>> calculate_parlay_odds([0.3, 0.4], correlation=0.12)
        (0.1344, +644)
    """
    # Independent probability (multiply all)
    independent_prob = 1.0
    for prob in individual_probs:
        independent_prob *= prob

    # Apply correlation multiplier
    correlation_multiplier = 1 + correlation
    correlated_prob = independent_prob * correlation_multiplier

    # Ensure probability stays in valid range
    correlated_prob = min(max(correlated_prob, 0.0001), 0.9999)

    # Convert to American odds
    american_odds = decimal_to_american(correlated_prob)

    return correlated_prob, american_odds


def compare_odds(our_fair_odds, sportsbook_odds):
    """
    Compare our fair value to sportsbook odds

    Args:
        our_fair_odds (int): Our calculated fair American odds
        sportsbook_odds (int): Sportsbook's American odds

    Returns:
        dict: Comparison results with EV and recommendation
    """
    our_prob = american_to_decimal(our_fair_odds)
    ev = calculate_ev(our_prob, sportsbook_odds)

    if ev > 10:
        rating = "🔥 STRONG BET"
    elif ev > 5:
        rating = "✅ GOOD BET"
    elif ev > 0:
        rating = "⚠️ SLIGHT EDGE"
    else:
        rating = "❌ NO VALUE"

    return {
        'our_fair_odds': our_fair_odds,
        'our_probability': our_prob,
        'sportsbook_odds': sportsbook_odds,
        'sportsbook_implied_prob': american_to_decimal(sportsbook_odds),
        'ev_percent': ev,
        'is_plus_ev': ev > 0,
        'rating': rating
    }
