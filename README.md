# World Cup Predictor 2026

A web app where you predict FIFA World Cup 2026 match results and compete against friends on a leaderboard.

**Live:** https://worldcup-predictor-gitx.onrender.com

---

## What it does

You register an account, predict the score of every group stage match before it kicks off, and earn points when results come in. 3 points for an exact score, 1 point for getting the winner or draw right. A leaderboard tracks everyone's points across the tournament.

There's also a knockout bracket view, FIFA rankings for all 48 qualified nations with flags, a live countdown to the opening match, and group filters to browse all 72 matches.

## Stack

- Flask + SQLAlchemy
- PostgreSQL on Render
- Tailwind CSS
- Flask-Login

## Run locally

```bash
git clone https://github.com/jkyplayz-rb/worldcup-predictor.git
cd worldcup-predictor
pip install -r requirements.txt
python3 app.py
```

## Scoring

- Exact score → 3 pts
- Correct result → 1 pt
- Wrong → 0 pts

## Tournament dates

Group stage runs June 11 – June 26, 2026. Final is July 19.