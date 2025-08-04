"""
Reminder System Architecture

This module implements a multi-armed bandit system for personalizing reminders.

The system is designed as follows:
- Arms: Each "arm" of the bandit represents a different reminder strategy.
  The strategies are defined by a combination of:
    - Channel: (e.g., 'push', 'email', 'sms')
    - Timing: (e.g., '15_minutes_before', '1_hour_before', 'on_day')
- Reward: The reward signal is based on user interaction with the reminder.
  - A positive reward (e.g., +1) is given if the user completes the task within a certain time frame after receiving the reminder.
  - A neutral reward (e.g., 0) is given if the user does not complete the task.
  - A negative reward (e.g., -1) could be given if the user dismisses the reminder, but this is not implemented in the initial version.
- Algorithm: The system uses an Epsilon-Greedy algorithm to balance exploration and exploitation.
  - With probability epsilon, a random arm (reminder strategy) is chosen.
  - With probability 1 - epsilon, the arm with the highest estimated reward is chosen.
- Personalization: The system maintains a separate bandit for each user to personalize the reminder strategy to their preferences.
"""

import numpy as np

class ReminderBandit:
    def __init__(self, user_id, arms, epsilon=0.1):
        self.user_id = user_id
        self.arms = arms
        self.epsilon = epsilon
        self.counts = {arm: 0 for arm in self.arms}
        self.values = {arm: 0.0 for arm in self.arms}

    def select_arm(self):
        """
        Select an arm to play, balancing exploration and exploitation.
        """
        if np.random.random() > self.epsilon:
            # Exploit: choose the best arm so far
            return max(self.values, key=self.values.get)
        else:
            # Explore: choose a random arm
            return np.random.choice(self.arms)

    def update(self, arm, reward):
        """
        Update the value of an arm after receiving a reward.
        """
        self.counts[arm] += 1
        n = self.counts[arm]
        value = self.values[arm]
        # Update the value using the incremental average formula
        new_value = ((n - 1) / n) * value + (1 / n) * reward
        self.values[arm] = new_value

import json

class ReminderBanditManager:
    def __init__(self, storage_path='bandit_data.json'):
        self.storage_path = storage_path
        self.bandits = self._load_bandits()

    def _load_bandits(self):
        try:
            with open(self.storage_path, 'r') as f:
                data = json.load(f)
                bandits = {}
                for user_id, bandit_data in data.items():
                    bandit = ReminderBandit(user_id, bandit_data['arms'], bandit_data['epsilon'])
                    bandit.counts = bandit_data['counts']
                    bandit.values = bandit_data['values']
                    bandits[user_id] = bandit
                return bandits
        except FileNotFoundError:
            return {}

    def _save_bandits(self):
        data = {}
        for user_id, bandit in self.bandits.items():
            data[user_id] = {
                'arms': bandit.arms,
                'epsilon': bandit.epsilon,
                'counts': bandit.counts,
                'values': bandit.values,
            }
        with open(self.storage_path, 'w') as f:
            json.dump(data, f, indent=4)

    def get_bandit(self, user_id, arms, epsilon=0.1):
        if user_id not in self.bandits:
            self.bandits[user_id] = ReminderBandit(user_id, arms, epsilon)
        return self.bandits[user_id]

    def save_bandit(self, bandit):
        self.bandits[bandit.user_id] = bandit
        self._save_bandits()

if __name__ == '__main__':
    # Example usage
    arms = ['push_15_min', 'email_1_hour', 'sms_on_day']
    manager = ReminderBanditManager()

    # Get a bandit for a user
    bandit = manager.get_bandit(user_id='test_user', arms=arms)

    # Simulate some interactions
    for i in range(100):
        arm = bandit.select_arm()
        # Simulate a reward
        reward = 1 if arm == 'push_15_min' and np.random.random() < 0.7 else 0
        bandit.update(arm, reward)

    # Save the bandit's state
    manager.save_bandit(bandit)

    print(f"Counts: {bandit.counts}")
    print(f"Values: {bandit.values}")
    print(f"Best arm: {max(bandit.values, key=bandit.values.get)}")
