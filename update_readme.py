import json
import re
from datetime import datetime
from leaderboard_data import JSONLeaderboard, AoCUser

PUZZLE_DATA_FILENAME = 'puzzle_data.json'
README_TEMPLATE_FILENAME = 'README.md.template'
README_FILENAME = 'README.md'
DAYS_COMPLETED_REGEX = re.compile(r'(Days%20Completed-)([0-9]+)(-green)')
STAR_REGEX = re.compile(r'(Stars%20Obtained%20⭐-)([0-9]+)(-yellow)')
NOT_SOLVED_REGEX = re.compile(r'(Not%20Solved%20❌-)([0-9]+)(-red)')
SOLUTION_TABLE_REGEX = re.compile(r'\{\{SOLUTION_TABLE}}')

TABLE_HEADER = ("| Day "
                "|            Title            "
                "| Part 1 "
                "| Part 2 "
                "|                             Code                              |"
                "\n"
                "|:---:"
                "|:---------------------------:"
                "|:------:"
                "|:------:"
                "|:-------------------------------------------------------------:|"
                "\n"
                )

TABLE_ROW = ("| {{day_left_padded}}  "
             "| [{{puzzle_name}}][day{{day_left_padded}}] "
             "|   ⭐    "
             "|   ⭐    "
             "| [![Part 1][part1]](aoc-{{day}}-1.py) [![Part 2][part2]](aoc-{{day}}-2.py) |"
             "\n"
             )


def build_row(day: int, name: str) -> str:
    day_no_pad = f'{day}'
    day_left_padded = f'{day:02}'

    row = TABLE_ROW
    row = re.sub(r'\{\{day_left_padded}}', day_left_padded, row)
    row = re.sub(r'\{\{day}}', day_no_pad, row)
    row = re.sub(r'\{\{puzzle_name}}', name, row)
    return row


def build_table() -> str:
    table = ''
    table += TABLE_HEADER
    day = datetime.utcnow().day
    with open(PUZZLE_DATA_FILENAME, "r") as f:
        puzzle_data = json.load(f)
    for d in range(1, day + 1):
        table += build_row(d, puzzle_data[str(d)])
    return table


def update_readme(user: AoCUser):
    with open(README_TEMPLATE_FILENAME, "r", encoding="utf-8") as f:
        template = f.read()
    f.close()
    template = DAYS_COMPLETED_REGEX.sub(rf'\g<1>{user.days_completed}\g<3>', template, re.MULTILINE)
    template = STAR_REGEX.sub(rf'\g<1>{user.stars}\g<3>', template, re.MULTILINE)
    template = NOT_SOLVED_REGEX.sub(rf'\g<1>{user.challenges_not_solved}\g<3>', template, re.MULTILINE)
    solution_table = build_table()
    template = SOLUTION_TABLE_REGEX.sub(solution_table, template)
    with open(README_FILENAME, "w", encoding="utf-8") as f:
        f.write(template)
    f.close()


def main():
    json_leaderboard = JSONLeaderboard()
    user = json_leaderboard.get_user_data()
    update_readme(user)


if __name__ == "__main__":
    main()
