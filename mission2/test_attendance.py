from unittest import mock

import pytest
from unittest.mock import mock_open
from mission2.main import input_file
from mission2.attendance import AttendanceSystem
from mission2.grade import GradeFactory, Gold, Silver, Normal, Grade
from mission2.player import Player


def test_input_file_output(capsys):
    input_file()
    captured = capsys.readouterr()
    assert captured.out == ('NAME : Umar, POINT : 48, GRADE : SILVER\n'
                            'NAME : Daisy, POINT : 45, GRADE : SILVER\n'
                            'NAME : Alice, POINT : 61, GRADE : GOLD\n'
                            'NAME : Xena, POINT : 91, GRADE : GOLD\n'
                            'NAME : Ian, POINT : 23, GRADE : NORMAL\n'
                            'NAME : Hannah, POINT : 127, GRADE : GOLD\n'
                            'NAME : Ethan, POINT : 44, GRADE : SILVER\n'
                            'NAME : Vera, POINT : 22, GRADE : NORMAL\n'
                            'NAME : Rachel, POINT : 54, GRADE : GOLD\n'
                            'NAME : Charlie, POINT : 58, GRADE : GOLD\n'
                            'NAME : Steve, POINT : 38, GRADE : SILVER\n'
                            'NAME : Nina, POINT : 79, GRADE : GOLD\n'
                            'NAME : Bob, POINT : 8, GRADE : NORMAL\n'
                            'NAME : George, POINT : 42, GRADE : SILVER\n'
                            'NAME : Quinn, POINT : 6, GRADE : NORMAL\n'
                            'NAME : Tina, POINT : 24, GRADE : NORMAL\n'
                            'NAME : Will, POINT : 36, GRADE : SILVER\n'
                            'NAME : Oscar, POINT : 13, GRADE : NORMAL\n'
                            'NAME : Zane, POINT : 1, GRADE : NORMAL\n'
                            '\n'
                            'Removed player\n'
                            '==============\n'
                            'Bob\n'
                            'Zane\n')


def test_input_file_error(mocker):
    # Arrange
    with mock.patch('builtins.open') as mock_open:
        mock_open.side_effect = FileNotFoundError
        # Act & Assert
        input_file()


def test_input_none_line(mocker, capsys):
    # Arrange
    mock_file_content = None
    m = mock_open(read_data=mock_file_content)
    # Act
    captured = capsys.readouterr()
    with mock.patch('builtins.open', m):
        input_file()
    # Assert
    assert captured.out == ""


def test_grade_factory_create_except_normal(mocker):
    # Arrange
    total_points = 2
    mocker.patch.object(GradeFactory, "grades", [Gold, Silver])

    # Act & Assert
    with pytest.raises(AttributeError):
        GradeFactory().create(total_points=total_points)


@pytest.mark.parametrize("total_points, grade_cls", [
    (60, Gold),
    (40, Silver),
    (10, Normal),
])
def test_grade_factory_create_normal(total_points, grade_cls):
    # Arrange

    # Act
    grade_instance = GradeFactory().create(total_points=total_points)

    # Assert
    assert grade_instance.__class__ == grade_cls


def test_player_bonus_points_wednesday(mocker):
    # Arrange
    player = Player(1, "Kang")
    for _ in range(10):
        player._record_attendance("wednesday")

    # Act
    result = player.bonus_points

    # Assert
    assert result == 10


def test_player_bonus_points_weekend(mocker):
    # Arrange
    player = Player(1, "Kang")
    for _ in range(5):
        player._record_attendance("saturday")
    for _ in range(5):
        player._record_attendance("sunday")

    # Act
    result = player.bonus_points

    # Assert
    assert result == 10


@pytest.mark.parametrize("day_of_week, expect_score", [
    ("wednesday", 3),
    ("saturday", 2),
    ("sunday", 2),
    ("monday", 1),
    ("tuesday", 1),
    ("thursday", 1),
    ("friday", 1),
])
def test_calc_attendance_point(day_of_week, expect_score):
    # Arrange
    player = Player(1, "Kang")

    # Act
    result = player._calc_attendance_point(day_of_week)

    # Assert
    assert result == expect_score


def test_print_removed_player(capsys):
    # Arrange
    players = dict()
    players["Kang"] = Player(1, "Kang")
    players["Kan1"] = Player(2, "Kang1")

    attendance_system = AttendanceSystem(players)

    # Act
    attendance_system._print_removed_player()
    captured = capsys.readouterr()

    # Assert
    assert captured.out == '\nRemoved player\n==============\nKang\nKang1\n'


def test_print_without_remove_player(capsys, mocker):
    # Arrange
    players = dict()
    mocker.patch.object(Grade, "code", 1)
    mocker.patch.object(Player, "wednesday_count", 1)
    mocker.patch.object(Player, "weekend_count", 1)

    players["Kang"] = Player(1, "Kang")

    attendance_system = AttendanceSystem(players)

    # Act
    attendance_system._print_removed_player()
    captured = capsys.readouterr()

    # Assert
    assert captured.out == '\nRemoved player\n==============\n'


def test_create_player(mocker):
    # Arrange
    attendance_system = AttendanceSystem(dict())

    # Act
    next_pid = attendance_system._next_pid
    attendance_system.get_or_create_player("Kang")

    # Assert
    assert next_pid != attendance_system._next_pid
    assert "Kang" in attendance_system.players

def test_get_player(mocker):
    # Arrange
    attendance_system = AttendanceSystem(dict())
    attendance_system.get_or_create_player("Kang")
    next_pid = attendance_system._next_pid

    # act
    attendance_system.get_or_create_player("Kang")

    # Assrt
    assert next_pid == attendance_system._next_pid
