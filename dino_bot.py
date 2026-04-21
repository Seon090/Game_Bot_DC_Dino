import json
import os
from pathlib import Path
from typing import Dict

import discord
from discord.ext import commands

from dino_logic import TRACK_LENGTH, ensure_player, simulate_race

SCORE_FILE = Path("dino_scores.json")


def load_scores() -> Dict[str, Dict[str, int | str]]:
    if not SCORE_FILE.exists():
        return {}
    with SCORE_FILE.open("r", encoding="utf-8") as f:
        return json.load(f)


def save_scores(scores: Dict[str, Dict[str, int | str]]) -> None:
    with SCORE_FILE.open("w", encoding="utf-8") as f:
        json.dump(scores, f, indent=2)



intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready() -> None:
    print(f"{bot.user} is stomping around the server.")


@bot.command(name="hatch")
async def hatch(ctx: commands.Context) -> None:
    scores = load_scores()
    player = ensure_player(scores, ctx.author.id, ctx.author.display_name)
    save_scores(scores)
    await ctx.send(f"🥚 {ctx.author.mention} hatched **{player['dino']}**. Let the chaos begin!")


@bot.command(name="dino")
async def dino(ctx: commands.Context) -> None:
    scores = load_scores()
    player = ensure_player(scores, ctx.author.id, ctx.author.display_name)
    save_scores(scores)
    await ctx.send(
        f"🦕 **{player['dino']}** | Points: **{player['points']}** | Wins: **{player['wins']}** | Races: **{player['races']}**"
    )


@bot.command(name="race")
async def race(ctx: commands.Context) -> None:
    scores = load_scores()
    racers = [ctx.author]
    for member in ctx.message.mentions:
        if member.id != ctx.author.id:
            racers.append(member)

    unique_racers = []
    seen = set()
    for racer in racers:
        if racer.id not in seen:
            unique_racers.append(racer)
            seen.add(racer.id)

    if len(unique_racers) < 2:
        await ctx.send("Need at least 2 racers. Mention someone: `!race @friend`")
        return

    for racer in unique_racers:
        ensure_player(scores, racer.id, racer.display_name)

    winner_id, race_log = simulate_race([r.id for r in unique_racers])

    for racer in unique_racers:
        player = scores[str(racer.id)]
        player["races"] += 1
        player["points"] += 1
    winner = scores[str(winner_id)]
    winner["wins"] += 1
    winner["points"] += 2
    save_scores(scores)

    max_lines = 8
    highlights = "\n".join(race_log[-max_lines:])
    winner_member = next(r for r in unique_racers if r.id == winner_id)
    await ctx.send(
        "🏁 **Dino Derby Results** 🏁\n"
        f"Winner: {winner_member.mention} and **{winner['dino']}**!\n"
        f"Last {max_lines} moments:\n```\n{highlights}\n```"
    )


@bot.command(name="leaderboard")
async def leaderboard(ctx: commands.Context) -> None:
    scores = load_scores()
    if not scores:
        await ctx.send("No racers yet. Use `!hatch` and `!race` first.")
        return

    ranked = sorted(scores.values(), key=lambda p: (p["points"], p["wins"]), reverse=True)[:10]
    lines = [
        f"{i + 1}. {player['name']} ({player['dino']}) - {player['points']} pts, {player['wins']} wins"
        for i, player in enumerate(ranked)
    ]
    await ctx.send("🦖 **Top Dino Champions**\n" + "\n".join(lines))


if __name__ == "__main__":
    token = os.getenv("DISCORD_BOT_TOKEN")
    if not token:
        raise RuntimeError("Set DISCORD_BOT_TOKEN environment variable before starting the bot.")
    bot.run(token)
