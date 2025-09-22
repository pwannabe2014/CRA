from mission2.attendance import AttendanceSystem


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
