# Game_Bot_DC_Dino

Funny + competitive Discord dino racing bot.

## Features
- `!hatch`: get your random dino nickname
- `!dino`: view your dino stats
- `!race @user ...`: race against mentioned users with chaotic random events
- `!leaderboard`: top players by points and wins

## Setup
1. Create a Discord bot in the developer portal and copy the token.
2. Invite the bot to your server with `MESSAGE CONTENT INTENT` enabled.
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run:
   ```bash
   export DISCORD_BOT_TOKEN="your-token"
   python dino_bot.py
   ```

Player data is saved in `dino_scores.json`.
