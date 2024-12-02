import re
from leaderboard_data import JSONLeaderboard, AoCUser

README_FILENAME = 'README.md'
DAYS_COMPLETED_REGEX = re.compile(r'(Days%20Completed-)([0-9]+)(-green)')
STAR_REGEX = re.compile(r'(Stars%20Obtained%20⭐-)([0-9]+)(-yellow)')
NOT_SOLVED_REGEX = re.compile(r'(Not%20Solved%20❌-)([0-9]+)(-red)')


def update_readme(user: AoCUser):
    with open(README_FILENAME, "r", encoding="utf-8") as f:
        readme = f.read()
    f.close()
    readme = re.sub(DAYS_COMPLETED_REGEX, rf'\g<1>{user.days_completed}\g<3>', readme, re.MULTILINE)
    readme = re.sub(STAR_REGEX, rf'\g<1>{user.stars}\g<3>', readme, re.MULTILINE)
    readme = re.sub(NOT_SOLVED_REGEX, rf'\g<1>{user.challenges_not_solved}\g<3>', readme, re.MULTILINE)
    with open(README_FILENAME, "w", encoding="utf-8") as f:
        f.write(readme)
    f.close()


def main():
    json_leaderboard = JSONLeaderboard()
    user = json_leaderboard.get_user_data()
    update_readme(user)


if __name__ == "__main__":
    main()
