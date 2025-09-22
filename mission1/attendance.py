from enum import IntEnum


class DayofWeek(IntEnum):
    Mon = 0
    Tue = 1
    Wed = 2
    Thu = 3
    Fri = 4
    Sat = 5
    Sun = 6


class AttendanceScore(IntEnum):
    Training = 3
    Weekend = 2
    Default = 1


TOTAL_ATTENDANCE_LIST = 500
id_map = {}
id_cnt = 0

# dat[사용자ID][요일] # 코테에나 좋으니 수정 필요
dat = [[0] * 100 for _ in range(100)]
points = [0] * 100
grade = [0] * 100
names = [''] * 100
wed = [0] * 100
weeken = [0] * 100

# 머리속에있는 스파게티를 풀어서 함수단위로 잘짜주세요. # 다끝나신분들은 퇴근
def input2(name, day_of_week):
    global id_cnt

    registration_player_id(name)

    player_id = id_map[name] # 이거그냥 id 아님 ?

    add_point = 0
    index = 0

    if day_of_week == "monday":
        index = 0
        add_point += AttendanceScore.Default
    elif day_of_week == "tuesday":
        index = 1
        add_point += AttendanceScore.Default
    elif day_of_week == "wednesday":  # 훈련일
        index = 2
        add_point += AttendanceScore.Training
        wed[player_id] += 1
    elif day_of_week == "thursday":
        index = 3
        add_point += AttendanceScore.Default
    elif day_of_week == "friday":
        index = 4
        add_point += AttendanceScore.Default
    elif day_of_week == "saturday":  # 주말점수
        index = 5
        add_point += AttendanceScore.Weekend
        weeken[player_id] += 1
    elif day_of_week == "sunday":  # 주말점수
        index = 6
        add_point += AttendanceScore.Weekend
        weeken[player_id] += 1

    dat[player_id][index] += 1
    points[player_id] += add_point


def registration_player_id(name):
    global id_cnt
    if name not in id_map:
        id_cnt += 1
        id_map[name] = id_cnt
        names[id_cnt] = name


def input_file():  # 리팩하기 쉽지 않으니 잘 구분해주세요  # 숫자코드
    try:
        with open("attendance_weekday_500.txt", encoding='utf-8') as f:
            for _ in range(TOTAL_ATTENDANCE_LIST):
                line = f.readline()
                if not line:
                    break
                parts = line.strip().split()
                if len(parts) == 2:
                    input2(parts[0], parts[1])

        for i in range(1, id_cnt + 1):  # 최종id_cnt에 대해서 변화필요
            if dat[i][DayofWeek.Wed] > 9:
                points[i] += 10
            if dat[i][DayofWeek.Sat] + dat[i][DayofWeek.Sun] > 9:
                points[i] += 10

            if points[i] >= 50:
                grade[i] = 1
            elif points[i] >= 30:
                grade[i] = 2
            else:
                grade[i] = 0

            print(f"NAME : {names[i]}, POINT : {points[i]}, GRADE : ", end="")
            if grade[i] == 1:
                print("GOLD")
            elif grade[i] == 2:
                print("SILVER")
            else:
                print("NORMAL")

        print("\nRemoved player")
        print("==============")
        for i in range(1, id_cnt + 1):
            if grade[i] not in (1, 2) and wed[i] == 0 and weeken[i] == 0:
                print(names[i])

    except FileNotFoundError:
        print("파일을 찾을 수 없습니다.")


if __name__ == "__main__":
    input_file()
