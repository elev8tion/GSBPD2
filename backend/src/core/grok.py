import random

class GrokInsightGenerator:
    def generate_insight(self, prediction: float, team_strength: float, opponent_strength: float) -> str:
        margin = abs(prediction)
        is_positive = prediction > 0
        
        if margin < 2:
            quotes = [
                "This one's tighter than a submarine hatch. Flip a coin, or maybe consult a tea leaf reader.",
                "Too close to call! It's a toss-up, like predicting the weather on Mars.",
                "Razor thin margins here. Proceed with caution, intrepid bettor."
            ]
        elif margin < 7:
            if is_positive:
                quotes = [
                    "Looking good! They might just pull this off. Don't bet the farm, but maybe the tractor.",
                    "Positive vibes detected. The odds are tilting in your favor, slightly.",
                    "A decent edge. Like having a towel in a galaxy of chaos, it's useful."
                ]
            else:
                quotes = [
                    "Underdog alert! They're fighting an uphill battle. Maybe sit this one out?",
                    "Not looking great. Unless they have a secret weapon, I'd stay away.",
                    "Negative outlook. Proceed only if you enjoy living dangerously."
                ]
        else:
            if is_positive:
                quotes = [
                    "Slam dunk! (Wrong sport, but you get it). This looks like a solid win.",
                    "The stars are aligning! High confidence in this spread covering.",
                    "KC DaCRE8TOR approves! This margin is wider than the Grand Canyon."
                ]
            else:
                quotes = [
                    "Oof. This looks like a train wreck waiting to happen. Avoid!",
                    "Major underdog energy. You'd have better luck navigating an asteroid field.",
                    "Don't do it! The probability engine is screaming 'NO' in 42 languages."
                ]
                
        return random.choice(quotes)
