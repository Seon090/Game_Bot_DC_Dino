import random
from typing import Dict, List, Tuple

TRACK_LENGTH = 20

ADJECTIVES = [
    "Spicy",
    "Zoomy",
    "Chunky",
    "Sneaky",
    "Derpy",
    "Turbo",
]
DINOS = ["Rex", "Trike", "Nugget", "Stompy", "Chomper", "Pickle"]


def ensure_player(scores: Dict[str, Dict[str, int | str]], user_id: int, display_name: str) -> Dict[str, int | str]:
    key = str(user_id)
    if key not in scores:
        nickname = f"{random.choice(ADJECTIVES)} {random.choice(DINOS)}"
        scores[key] = {"name": display_name, "dino": nickname, "points": 0, "wins": 0, "races": 0}
    else:
        scores[key]["name"] = display_name
    return scores[key]


def run_race_step(position: int) -> Tuple[int, str]:
    roll = random.randint(1, 6)
    event_roll = random.random()
    if event_roll < 0.15:
        move = max(0, roll - 2)
        return position + move, "slips on a banana peel 🍌"
    if event_roll > 0.85:
        move = roll + 3
        return position + move, "finds turbo nuggets ⚡"
    return position + roll, "runs like the rent is due 🦖"


def simulate_race(participant_ids: List[int]) -> Tuple[int, List[str]]:
    positions = {pid: 0 for pid in participant_ids}
    log: List[str] = []
    while True:
        for pid in participant_ids:
            positions[pid], event = run_race_step(positions[pid])
            log.append(f"{pid}: {event} -> {positions[pid]}/{TRACK_LENGTH}")
            if positions[pid] >= TRACK_LENGTH:
                return pid, log
