from mission2.grade import GradeFactory

class Player:
    BONUS_POINTS = 10
    WEDNESDAY_THRESHOLD = 9
    WEEKEND_THRESHOLD = 9
    attendance_score = {"Training": 3, "Weekend": 2, "Normal": 1}

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
            score = self.attendance_score["Training"]
        elif day_of_week == "saturday":
            score = self.attendance_score["Weekend"]
        elif day_of_week == "sunday":
            score = self.attendance_score["Weekend"]
        else:
            score = self.attendance_score["Normal"]
        return score

    def add_attendance(self, day_of_week):
        self._record_attendance(day_of_week)
        self.points += self._calc_attendance_point(day_of_week)
