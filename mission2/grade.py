from abc import ABC, abstractmethod

class Grade(ABC):
    @property
    @abstractmethod
    def label(self):
        pass

    @property
    @abstractmethod
    def code(self):
        pass

    @abstractmethod
    def match(self, points):
        pass


class Gold(Grade):
    THRESHOLD = 50

    @property
    def label(self):
        return "GOLD"

    @property
    def code(self):
        return 1

    def match(self, points):
        return True if points >= self.THRESHOLD else False


class Silver(Grade):
    THRESHOLD = 30

    @property
    def label(self):
        return "SILVER"

    @property
    def code(self):
        return 2

    def match(self, points):
        return True if points >= self.THRESHOLD else False


class Normal(Grade):
    @property
    def label(self):
        return "NORMAL"

    @property
    def code(self):
        return 0

    def match(self, points):
        return True


class GradeFactory:
    grades = [Gold, Silver, Normal]

    @classmethod
    def create(cls, points) -> Grade:
        for grade_cls in cls.grades:
            grade = grade_cls()
            if grade.match(points):
                return grade
        raise AttributeError