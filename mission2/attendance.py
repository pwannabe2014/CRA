from enum import IntEnum
from typing import Dict
from abc import ABC, abstractmethod

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
        self._name: str = name
        self._points: int = 0
        self._grade: int = 0
        self.attendances = {"monday": 0, "tuesday": 0, "wednesday": 0, "thursday": 0, "friday": 0, "saturday": 0,
                            "sunday": 0}

    @property
    def points(self):
        return self._points

    @points.setter
    def points(self, points):
        self._points = points

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def grade(self):
        return self._grade

    @grade.setter
    def grade(self, grade):
        self._grade = grade

    @property
    def wednesday_count(self)->int:
        return self.attendances["wednesday"]

    @property
    def weekend_count(self)->int:
        return self.attendances["saturday"] + self.attendances["sunday"]

    def get_attendance(self, day_of_week)->int:
        return self.attendances.get(day_of_week, 0)

    def record_attendance(self, day_of_week):
        self.attendances[day_of_week] += 1

    def _calc_attendance_point(self, day_of_week):
        if day_of_week == "wednesday":  # 훈련일
            point = AttendanceScore.Training
        elif day_of_week == "saturday":  # 주말점수
            point = AttendanceScore.Weekend
        elif day_of_week == "sunday":  # 주말점수
            point = AttendanceScore.Weekend
        else:
            point = AttendanceScore.Default
        self.points += point

    def add_attendance(self, day_of_week):
        self.record_attendance(day_of_week)
        self._calc_attendance_point(day_of_week)

class AttendanceSystem:
    def __init__(self, players):
        self.players: Dict[str, Player] = players
        self._next_pid = 0

    def get_or_create_player(self, name):
        if name not in self.players:
            self._next_pid += 1
            self.players[name] = Player(self._next_pid, name)
        return self.players[name]

    def print_result(self):
        for player in self.players.values():
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
        for player in self.players.values():
            if (player.grade not in (grade_label["GOLD"], grade_label["SILVER"])
                    and player.wednesday_count == 0
                    and player.weekend_count == 0):
                print(player.name)



def input_file(limits=500):  # 리팩하기쉽지않으니 잘 구분해주세요  # 숫자코드를 읽는사람이 헷갈리죠
    attendance_system = AttendanceSystem(players={})  # <-- 뭐해주지..  player class를 관리해주는 역할

    try:
        with open("attendance_weekday_500.txt", encoding='utf-8') as f:
            for _ in range(limits):
                line = f.readline()
                if not line:
                    break
                parts = line.strip().split()
                if len(parts) == 2:
                    name, day_of_week = parts
                    player = attendance_system.get_or_create_player(name)
                    player.add_attendance(day_of_week)
        attendance_system.print_result()

    except FileNotFoundError:
        print("파일을 찾을 수 없습니다.")

if __name__ == "__main__":
    input_file()
