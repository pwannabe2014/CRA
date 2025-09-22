from abc import abstractmethod, ABC

from mission2.grade import GradeFactory


class Score(ABC):
    @property
    @abstractmethod
    def score(self):
        pass

class TrainingScore(Score):
    @property
    def score(self):
        return 3

class WeekendScore(Score):
    @property
    def score(self):
        return 2

class DefaultScore(Score):
    @property
    def score(self):
        return 1

class Player:
    BONUS_POINTS = 10
    WEDNESDAY_THRESHOLD = 9
    WEEKEND_THRESHOLD = 9

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
    def bonus_points(self):
        bonus_points = 0
        if self._get_attendance("wednesday") > self.WEDNESDAY_THRESHOLD:
            bonus_points += self.BONUS_POINTS
        if self._get_attendance("saturday") + self._get_attendance("sunday") > self.WEEKEND_THRESHOLD:
            bonus_points += self.BONUS_POINTS
        return bonus_points

    @property
    def total_points(self):
        return self._points + self.bonus_points

    @property
    def grade(self):
        return GradeFactory().create(total_points=self.total_points)

    @property
    def wednesday_count(self) -> int:
        return self.attendances["wednesday"]

    @property
    def weekend_count(self) -> int:
        return self.attendances["saturday"] + self.attendances["sunday"]

    def _get_attendance(self, day_of_week) -> int:
        return self.attendances.get(day_of_week, 0)

    def _record_attendance(self, day_of_week):
        self.attendances[day_of_week] += 1

    def _calc_attendance_point(self, day_of_week):
        if day_of_week == "wednesday":
            score = TrainingScore().score
        elif day_of_week == "saturday":
            score = WeekendScore().score
        elif day_of_week == "sunday":
            score = WeekendScore().score
        else:
            score = DefaultScore().score
        self.points += score

    def add_attendance(self, day_of_week):
        self._record_attendance(day_of_week)
        self._calc_attendance_point(day_of_week)
