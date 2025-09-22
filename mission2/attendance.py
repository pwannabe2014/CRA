from enum import IntEnum
from typing import Dict

BONUS_POINTS = 10
GOLD_MIN = 50
SILVER_MIN = 30
WEDNESDAY_THRESHOLD = 9
WEEKEND_THRESHOLD = 9

grade_label = {"GOLD": 1, "SILVER": 2, "NORMAL": 0}


class AttendanceScore(IntEnum):
    Training = 3
    Weekend = 2
    Default = 1


class Player:
    def __init__(self, pid, name):
        self.pid = pid
        self.name = name
        self.points = 0
        self.grade = 0
        self.attendances = {"monday": 0,
                            "tuesday":0,
                            "wednesday": 0,
                            "thursday": 0,
                            "friday": 0,
                            "saturday": 0,
                            "sunday": 0}
        self.wednesday_count = 0
        self.weekend_count = 0

    def add_point(self, point):
        self.points += point

    def get_attendance(self, day_of_week):
        return self.attendances.get(day_of_week, 0)

    def record_attendance(self, day_of_week):
        self.attendances[day_of_week] += 1


players: Dict[str, Player] = {}
next_pid = 0


def add_attendance(day_of_week, player: Player):
    player.record_attendance(day_of_week)
    if day_of_week == "wednesday":  # 훈련일
        point = AttendanceScore.Training
        player.wednesday_count += 1
    elif day_of_week == "saturday":  # 주말점수
        point = AttendanceScore.Weekend
        player.weekend_count += 1
    elif day_of_week == "sunday":  # 주말점수
        point = AttendanceScore.Weekend
        player.weekend_count += 1
    else:
        point = AttendanceScore.Default

    player.add_point(point)


def get_or_create_player(name):
    global next_pid  # 1시작으로 잡자
    if name not in players:
        next_pid += 1
        players[name] = Player(next_pid, name)
    return players[name]


# 머리속에있는 스파게티를 풀어서 함수단위로 잘짜주세요. # 다끝나신분들은 퇴근
def input2(name, day_of_week):
    global next_pid
    player = get_or_create_player(name)
    add_attendance(day_of_week, player)


def print_result():
    global next_pid
    for player in players.values():
        if player.get_attendance("wednesday") > WEDNESDAY_THRESHOLD:
            player.points += BONUS_POINTS
        if player.get_attendance("saturday") + player.get_attendance("sunday") > WEEKEND_THRESHOLD:
            player.points += BONUS_POINTS

        if player.points >= GOLD_MIN:
            player.grade = grade_label["GOLD"]
        elif player.points >= SILVER_MIN:
            player.grade = grade_label["SILVER"]
        else:
            player.grade = grade_label["NORMAL"]

        print(f"NAME : {player.name}, POINT : {player.points}, GRADE : ", end="")
        if player.grade == grade_label["GOLD"]:
            print("GOLD")
        elif player.grade == grade_label["SILVER"]:
            print("SILVER")
        else:
            print("NORMAL")

    print("\nRemoved player")
    print("==============")
    for player in players.values():
        if (player.grade not in (grade_label["GOLD"], grade_label["SILVER"])
                and player.wednesday_count == 0
                and player.weekend_count == 0):
            print(player.name)


def input_file(limits=500):  # 리팩하기쉽지않으니 잘 구분해주세요  # 숫자코드를 읽는사람이 헷갈리죠
    try:
        with open("attendance_weekday_500.txt", encoding='utf-8') as f:
            for _ in range(limits):
                line = f.readline()
                if not line:
                    break
                parts = line.strip().split()
                if len(parts) == 2:
                    input2(parts[0], parts[1])
        print_result()

    except FileNotFoundError:
        print("파일을 찾을 수 없습니다.")


if __name__ == "__main__":
    input_file()
