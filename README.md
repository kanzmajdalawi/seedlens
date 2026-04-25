# Verdikt

AI-powered startup evaluation agent for pre-seed and seed stage companies.
It will also function as a scouting agent connecting startups with VC's that would support their mission. Currently evaluates the investment thesis of top VC firms Andreessen Horowitz (a16z), Sequoia Capital, Tiger Global Management, General Catalyst, and Insight Partners.

Scores startups across five VC frameworks:
- Sequoia Arc PMF archetypes (Hair on Fire, Hard Fact, Future Vision)
- Sean Ellis 40% threshold test
- Lean Startup PMF Pyramid (retention, engagement, NPS)
- Harvard second-time founder bonus model
- Forbes meta-competency framework (pivot ability, fundraising, team-building)

## How it works

You paste a startup description or pitch summary into the terminal.
Verdikt returns a structured scorecard with weighted scores across multiple established VC frameworks refrenced above. 

Based on those, Verdikt will evaluate those metrics according to three layers: Founder Quality (35%), Market Opportunity (25%),
and PMF Signals (40%), plus moat and regulatory flags.

## Setup

1. Clone this repo
2. Install dependencies: `pip install -r requirements.txt`
3. Add your Anthropic API key to a `.env` file
4. Run: `python evaluate.py`

## Output

- Composite score out of 100
- Score per dimension with reasoning
- Red flag triggers
- PMF archetype label
- Recommended due diligence questions