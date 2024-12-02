import json
import requests
import os
from dataclasses import dataclass
from datetime import datetime


@dataclass
class AoCUser:
    name: str
    stars: int
    daily_data: dict
    days_completed: int = 0
    challenges_not_solved: int = 0

    def __post_init__(self):
        for day in self.daily_data:
            if self.daily_data[day] == 2:
                self.days_completed += 1
        today = datetime.utcnow().date()
        total_stars = today.day * 2
        self.challenges_not_solved = total_stars - self.stars

    def __str__(self):
        return (f'{self.name}\n'
                f'stars: {self.stars}\n'
                f'completed: {self.days_completed}\n'
                f'not completed: {self.challenges_not_solved}\n'
                )


class JSONLeaderboard:
    """
    Gets Leaderboard data from Advent of Code user profile and caches it in a json file.
    Cache is updated only once per day if not otherwise invoked.
    Needs user id and session cookie in a config file.
    """
    CONFIG_FILE = 'config.json'
    LEADERBOARD_URL_BASE = 'https://adventofcode.com/2024/leaderboard/private/view/'
    LEADERBOARD_FILE = 'leaderboard.json'

    def __init__(self):
        self.json_data = {}
        with open(self.CONFIG_FILE, "r") as f:
            config = json.load(f)
        f.close()
        self.user_id = config['user_id']
        self.session_cookie = config['session_cookie']
        print(f'Proceeding with user id: {self.user_id} and session cookie: {self.session_cookie}')
        self.leaderboard_url = f'{self.LEADERBOARD_URL_BASE}{self.user_id}.json'
        today = datetime.utcnow().date()
        midnight_today = datetime(today.year, today.month, today.day, 0, 0, 0)
        leaderboard_file_last_modify = datetime.utcfromtimestamp(os.path.getmtime(self.LEADERBOARD_FILE))
        print(f'{self.LEADERBOARD_FILE} was last modified on {leaderboard_file_last_modify}')
        if leaderboard_file_last_modify < midnight_today:
            self.get_from_url()
            self.write_to_file()
        else:
            self.get_from_file()

    def get_from_url(self):
        print(f'Get JSON Data from AoC URL')
        cookies = {'session': self.session_cookie}
        self.json_data = requests.get(self.leaderboard_url, cookies=cookies).json()

    def get_from_file(self):
        print(f'Get JSON Data from {self.LEADERBOARD_FILE}')
        with open(self.LEADERBOARD_FILE, "r") as f:
            self.json_data = json.load(f)
        f.close()

    def write_to_file(self):
        print(f'Writing JSON Data to {self.LEADERBOARD_FILE}')
        with open(self.LEADERBOARD_FILE, "w") as f:
            json.dump(self.json_data, f)
        f.close()

    def get_user_data(self) -> AoCUser:
        user_data = self.json_data['members'][self.user_id]
        username = user_data['name']
        star_amount = user_data['stars']
        daily_data = user_data['completion_day_level']
        day_dict = {}
        for day in daily_data:
            match len(daily_data[day]):
                case 1:
                    day_dict[day] = 1
                case 2:
                    day_dict[day] = 2
                case _:
                    day_dict[day] = 0
        return AoCUser(username, star_amount, day_dict)


if __name__ == "__main__":
    json_leaderboard = JSONLeaderboard()
    user = json_leaderboard.get_user_data()
    print(user)
