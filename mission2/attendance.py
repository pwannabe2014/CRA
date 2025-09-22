from typing import Dict

from mission2.player import Player


class AttendanceSystem:
    def __init__(self, players):
        self.players: Dict[str, Player] = players
        self._next_pid = 0

    def get_or_create_player(self, name):
        if name not in self.players:
            self._next_pid += 1
            self.players[name] = Player(self._next_pid, name)
        return self.players[name]

    def _print_removed_player(self):
        print("\nRemoved player")
        print("==============")
        for player in self.players.values():
            if (player.grade.code not in (1, 2)  # Gold가 1, silver가 2, normal이 0이라서 의미가 있다 판단되어 이부분은 code로 내버려둠
                    and player.wednesday_count == 0
                    and player.weekend_count == 0):
                print(player.name)

    def print_result(self):
        for player in self.players.values():
            print(f"NAME : {player.name}, POINT : {player.total_points}, GRADE : {player.grade.label}")
        self._print_removed_player()


def input_file(limits=500):
    attendance_system = AttendanceSystem(players={})

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
