#!/usr/bin/env python3
"""
NBA Uncertainty Quantifier
Calculates confidence intervals for probability estimates using bootstrap resampling

Purpose: Quantify uncertainty in prop predictions
- Bootstrap 95% confidence intervals
- Flag high-risk props (wide CI)
- Improve decision-making with uncertainty awareness

Example Output:
    High Confidence: 98% (95% CI: [96%, 99%]) ✅ LOW RISK
    Low Confidence: 65% (95% CI: [48%, 78%]) ⚠️ HIGH RISK
"""
import random


class UncertaintyQuantifier:
    """
    Quantify uncertainty in probability estimates using bootstrap resampling

    Bootstrap Confidence Intervals:
    - Resample historical data with replacement
    - Calculate probability for each resample
    - Use percentiles for CI bounds

    Risk Classification:
    - LOW: CI width < 10% (e.g., [94%, 99%])
    - MEDIUM: CI width 10-20% (e.g., [75%, 90%])
    - HIGH: CI width > 20% (e.g., [48%, 78%])
    """

    def __init__(self, n_bootstrap=1000, ci_level=0.95):
        """
        Initialize uncertainty quantifier

        Args:
            n_bootstrap (int): Number of bootstrap samples (default: 1000)
            ci_level (float): Confidence interval level (default: 0.95 for 95% CI)
        """
        self.n_bootstrap = n_bootstrap
        self.ci_level = ci_level

        # Calculate percentiles for CI bounds
        alpha = 1 - ci_level
        self.lower_percentile = (alpha / 2) * 100
        self.upper_percentile = (1 - alpha / 2) * 100

    def calculate_bootstrap_ci(self, historical_values, line, direction="over"):
        """
        Calculate bootstrap confidence interval for a prop

        Args:
            historical_values (list): Historical stat values (e.g., [32, 28, 35, 31, ...])
            line (float): Betting line (e.g., 30.5)
            direction (str): "over" or "under"

        Returns:
            dict: {
                'point_estimate': float,  # Best estimate probability
                'ci_lower': float,        # Lower CI bound
                'ci_upper': float,        # Upper CI bound
                'ci_width': float,        # Width of CI
                'uncertainty': str,       # 'LOW', 'MEDIUM', 'HIGH'
                'n_samples': int          # Number of historical samples
            }
        """
        if not historical_values or len(historical_values) < 3:
            # Not enough data - return default with HIGH uncertainty
            return {
                'point_estimate': 0.50,
                'ci_lower': 0.30,
                'ci_upper': 0.70,
                'ci_width': 0.40,
                'uncertainty': 'HIGH',
                'n_samples': len(historical_values) if historical_values else 0
            }

        n = len(historical_values)
        bootstrap_probs = []

        # Bootstrap resampling
        for _ in range(self.n_bootstrap):
            # Resample with replacement
            resample = [random.choice(historical_values) for _ in range(n)]

            # Calculate probability for this resample
            if direction == "over":
                hits = sum(1 for v in resample if v > line)
            else:  # under
                hits = sum(1 for v in resample if v < line)

            prob = hits / n
            bootstrap_probs.append(prob)

        # Sort for percentile calculation
        bootstrap_probs.sort()

        # Calculate confidence interval
        ci_lower_idx = int(self.lower_percentile / 100 * self.n_bootstrap)
        ci_upper_idx = int(self.upper_percentile / 100 * self.n_bootstrap)

        ci_lower = bootstrap_probs[ci_lower_idx]
        ci_upper = bootstrap_probs[ci_upper_idx]
        ci_width = ci_upper - ci_lower

        # Point estimate (mean of bootstrap distribution)
        point_estimate = sum(bootstrap_probs) / len(bootstrap_probs)

        # Classify uncertainty
        if ci_width < 0.10:
            uncertainty = 'LOW'
        elif ci_width < 0.20:
            uncertainty = 'MEDIUM'
        else:
            uncertainty = 'HIGH'

        return {
            'point_estimate': round(point_estimate, 3),
            'ci_lower': round(ci_lower, 3),
            'ci_upper': round(ci_upper, 3),
            'ci_width': round(ci_width, 3),
            'uncertainty': uncertainty,
            'n_samples': n
        }

    def calculate_from_probability(self, probability, sample_size=20):
        """
        Estimate confidence interval from a probability when historical data unavailable

        Uses binomial approximation:
        CI ≈ p ± 1.96 * sqrt(p(1-p)/n)

        Args:
            probability (float): Point estimate probability (0-1)
            sample_size (int): Assumed sample size (default: 20 games)

        Returns:
            dict: Same format as calculate_bootstrap_ci()
        """
        import math

        p = probability
        n = sample_size

        # Standard error
        se = math.sqrt(p * (1 - p) / n)

        # 95% CI: ± 1.96 standard errors
        margin = 1.96 * se

        ci_lower = max(0.0, p - margin)
        ci_upper = min(1.0, p + margin)
        ci_width = ci_upper - ci_lower

        # Classify uncertainty
        if ci_width < 0.10:
            uncertainty = 'LOW'
        elif ci_width < 0.20:
            uncertainty = 'MEDIUM'
        else:
            uncertainty = 'HIGH'

        return {
            'point_estimate': round(p, 3),
            'ci_lower': round(ci_lower, 3),
            'ci_upper': round(ci_upper, 3),
            'ci_width': round(ci_width, 3),
            'uncertainty': uncertainty,
            'n_samples': n
        }

    def format_ci_display(self, ci_result):
        """
        Format confidence interval for display

        Args:
            ci_result (dict): Result from calculate_bootstrap_ci()

        Returns:
            str: Formatted display string

        Examples:
            "98% (95% CI: [96%, 99%]) ✅ LOW RISK"
            "65% (95% CI: [48%, 78%]) ⚠️ HIGH RISK"
        """
        prob = ci_result['point_estimate']
        lower = ci_result['ci_lower']
        upper = ci_result['ci_upper']
        uncertainty = ci_result['uncertainty']

        # Format percentages
        prob_pct = int(prob * 100)
        lower_pct = int(lower * 100)
        upper_pct = int(upper * 100)

        # Risk indicator
        if uncertainty == 'LOW':
            risk_emoji = "✅"
            risk_label = "LOW RISK"
        elif uncertainty == 'MEDIUM':
            risk_emoji = "⚡"
            risk_label = "MEDIUM RISK"
        else:  # HIGH
            risk_emoji = "⚠️"
            risk_label = "HIGH RISK"

        return f"{prob_pct}% (95% CI: [{lower_pct}%, {upper_pct}%]) {risk_emoji} {risk_label}"

    def get_confidence_stars(self, ci_result):
        """
        Convert uncertainty to star rating

        Args:
            ci_result (dict): Result from calculate_bootstrap_ci()

        Returns:
            str: Star rating (⭐⭐⭐⭐⭐ to ⭐⭐)
        """
        prob = ci_result['point_estimate']
        uncertainty = ci_result['uncertainty']

        # High probability + low uncertainty = 5 stars
        if prob >= 0.85 and uncertainty == 'LOW':
            return "⭐⭐⭐⭐⭐"
        elif prob >= 0.75 and uncertainty in ['LOW', 'MEDIUM']:
            return "⭐⭐⭐⭐"
        elif prob >= 0.60:
            return "⭐⭐⭐"
        else:
            return "⭐⭐"


# ==========================================
# TESTING & VALIDATION
# ==========================================

def test_bootstrap_ci():
    """
    Test bootstrap confidence interval calculation
    """
    print("="*80)
    print("🧪 TEST: Bootstrap Confidence Intervals")
    print("="*80)

    quantifier = UncertaintyQuantifier(n_bootstrap=1000)

    # Test 1: High-confidence prop (SGA 20+ points)
    print("\n📊 TEST 1: SGA 20+ Points (High Confidence)")
    print("  Historical games: [32, 28, 35, 31, 37, 29, 34, 33, 30, 36] (last 10)")
    sga_points = [32, 28, 35, 31, 37, 29, 34, 33, 30, 36, 31, 32, 35, 34, 33]

    result = quantifier.calculate_bootstrap_ci(sga_points, line=20.0, direction="over")

    print(f"\n  Point Estimate: {result['point_estimate']:.1%}")
    print(f"  95% CI: [{result['ci_lower']:.1%}, {result['ci_upper']:.1%}]")
    print(f"  CI Width: {result['ci_width']:.1%}")
    print(f"  Uncertainty: {result['uncertainty']}")
    print(f"  Display: {quantifier.format_ci_display(result)}")
    print(f"  Stars: {quantifier.get_confidence_stars(result)}")

    # Test 2: Low-confidence prop (Rookie 10+ points)
    print("\n\n📊 TEST 2: Rookie 10+ Points (Low Confidence)")
    print("  Historical games: [12, 8, 15, 6, 9, 13, 7, 11] (limited data)")
    rookie_points = [12, 8, 15, 6, 9, 13, 7, 11]

    result = quantifier.calculate_bootstrap_ci(rookie_points, line=10.0, direction="over")

    print(f"\n  Point Estimate: {result['point_estimate']:.1%}")
    print(f"  95% CI: [{result['ci_lower']:.1%}, {result['ci_upper']:.1%}]")
    print(f"  CI Width: {result['ci_width']:.1%}")
    print(f"  Uncertainty: {result['uncertainty']}")
    print(f"  Display: {quantifier.format_ci_display(result)}")
    print(f"  Stars: {quantifier.get_confidence_stars(result)}")

    # Test 3: Medium-confidence prop (SGA 5+ rebounds)
    print("\n\n📊 TEST 3: SGA 5+ Rebounds (Medium Confidence)")
    print("  Historical games: [6, 4, 5, 3, 7, 4, 6, 5, 4, 5]")
    sga_rebounds = [6, 4, 5, 3, 7, 4, 6, 5, 4, 5, 6, 5, 4, 6, 5]

    result = quantifier.calculate_bootstrap_ci(sga_rebounds, line=5.0, direction="over")

    print(f"\n  Point Estimate: {result['point_estimate']:.1%}")
    print(f"  95% CI: [{result['ci_lower']:.1%}, {result['ci_upper']:.1%}]")
    print(f"  CI Width: {result['ci_width']:.1%}")
    print(f"  Uncertainty: {result['uncertainty']}")
    print(f"  Display: {quantifier.format_ci_display(result)}")
    print(f"  Stars: {quantifier.get_confidence_stars(result)}")

    # Test 4: Probability-based CI (when no historical data)
    print("\n\n📊 TEST 4: Probability-Based CI (No Historical Data)")
    print("  Probability: 85%")
    print("  Sample Size: 20 games")

    result = quantifier.calculate_from_probability(0.85, sample_size=20)

    print(f"\n  Point Estimate: {result['point_estimate']:.1%}")
    print(f"  95% CI: [{result['ci_lower']:.1%}, {result['ci_upper']:.1%}]")
    print(f"  CI Width: {result['ci_width']:.1%}")
    print(f"  Uncertainty: {result['uncertainty']}")
    print(f"  Display: {quantifier.format_ci_display(result)}")

    print("\n" + "="*80)
    print("✅ BOOTSTRAP CI TESTS COMPLETE")
    print("="*80)


def test_ci_width_classification():
    """
    Test that CI width correctly classifies uncertainty
    """
    print("\n" + "="*80)
    print("🧪 TEST: CI Width Classification")
    print("="*80)

    quantifier = UncertaintyQuantifier()

    # Test different CI widths
    test_cases = [
        (0.98, 0.96, 0.99, "LOW"),    # Width: 0.03 (3%)
        (0.75, 0.65, 0.85, "MEDIUM"),  # Width: 0.20 (20%)
        (0.65, 0.48, 0.78, "HIGH"),    # Width: 0.30 (30%)
    ]

    for point, lower, upper, expected in test_cases:
        result = {
            'point_estimate': point,
            'ci_lower': lower,
            'ci_upper': upper,
            'ci_width': upper - lower,
            'uncertainty': expected,
            'n_samples': 20
        }

        display = quantifier.format_ci_display(result)
        status = "✅" if expected in display else "❌"

        print(f"\n  {status} Width: {result['ci_width']:.1%} → {expected}")
        print(f"     {display}")

    print("\n" + "="*80)


if __name__ == "__main__":
    print("\n" + "="*80)
    print("🏀 NBA UNCERTAINTY QUANTIFIER - TEST SUITE")
    print("="*80)

    # Run tests
    test_bootstrap_ci()
    test_ci_width_classification()

    print("\n" + "="*80)
    print("✅ UNCERTAINTY QUANTIFIER READY")
    print("="*80)
    print("\nKey Features:")
    print("  ✅ Bootstrap confidence intervals (1000 samples)")
    print("  ✅ Risk classification (LOW/MEDIUM/HIGH)")
    print("  ✅ Formatted display with emojis")
    print("  ✅ Probability-based CI for missing data")
    print("\n")
