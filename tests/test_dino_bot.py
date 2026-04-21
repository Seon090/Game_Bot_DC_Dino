import random
import unittest

from dino_logic import TRACK_LENGTH, run_race_step, simulate_race


class DinoBotLogicTests(unittest.TestCase):
    def test_run_race_step_never_moves_backwards(self):
        random.seed(7)
        pos = 0
        for _ in range(20):
            new_pos, _ = run_race_step(pos)
            self.assertGreaterEqual(new_pos, pos)
            pos = new_pos

    def test_simulate_race_returns_participant_winner_and_logs(self):
        random.seed(11)
        participants = [1, 2, 3]
        winner, logs = simulate_race(participants)

        self.assertIn(winner, participants)
        self.assertTrue(logs)
        self.assertTrue(any(f"{winner}:" in entry and f"/{TRACK_LENGTH}" in entry for entry in logs))


if __name__ == "__main__":
    unittest.main()
