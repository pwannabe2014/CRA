from unittest import mock

import pytest
from unittest.mock import mock_open
from mission2.attendance import *

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

def test_input_none_line(mocker,capsys):  # 리팩하기쉽지않으니 잘 구분해주세요  # 숫자코드를 읽는사람이 헷갈리죠
    # Arrange
    mock_file_content = None
    m = mock_open(read_data=mock_file_content)
    # Act
    captured = capsys.readouterr()
    with mock.patch('builtins.open', m):
        input_file()
    # Assert
    assert captured.out == ""

# # player 있는케이스와 없는케이스
# def test_get_or_create_player(mocker):
#     mocker.patch("mission2.attendance.players", {})
#     mocker.patch("mission2.attendance.pid", 0)
#     player = get_or_create_player("Kang")
#     assert player.name == "Kang"
