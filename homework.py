from dataclasses import dataclass, asdict
from typing import ClassVar, Type


@dataclass
class InfoMessage:
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    MESSAGE: ClassVar[str] = ('Тип тренировки: {training_type}; '
                              'Длительность: {duration:0.3f} ч.; '
                              'Дистанция: {distance:0.3f} км; '
                              'Ср. скорость: {speed:0.3f} км/ч; '
                              'Потрачено ккал: {calories:0.3f}.')

    def get_message(self) -> str:
        return self.MESSAGE.format(**asdict(self))


class Training:
    """Базовый класс тренировки."""
    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    MINUTES_IN_HOUR: int = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(
            self.__class__.__name__,
            self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories()
        )


class Running(Training):
    """Тренировка: бег."""
    CALORIES_MEAN_SPEED_MULTIPLIER: int = 18
    CALORIES_MEAN_SPEED_SHIFT: float = 1.79

    def get_spent_calories(self) -> float:
        min_v_chas = self.duration * self.MINUTES_IN_HOUR
        return (self.CALORIES_MEAN_SPEED_MULTIPLIER * self.get_mean_speed()
                + self.CALORIES_MEAN_SPEED_SHIFT
                ) * self.weight / self.M_IN_KM * min_v_chas


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    WEIGHT_MEAN_MULTIPLAYER: float = 0.035
    CALORIES_MEAN_MULTIPLAYER: float = 0.029
    KM_H_IN_M_S: float = 0.278
    SM_IN_M: int = 100

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: int,
                 ) -> None:
        super(SportsWalking, self).__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        speed_ed = self.get_mean_speed() * self.KM_H_IN_M_S
        height_m = self.height / self.SM_IN_M
        return ((self.WEIGHT_MEAN_MULTIPLAYER * self.weight
                 + (speed_ed ** 2 / height_m
                    ) * self.CALORIES_MEAN_MULTIPLAYER * self.weight
                 ) * self.duration * self.MINUTES_IN_HOUR)


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38
    SWIM_MEAN_FORMULA: float = 1.1
    SWIM_MEAN_MULTIPLAYER: int = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: int,
                 count_pool: int) -> None:
        super(Swimming, self).__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        distance = self.length_pool * self.count_pool
        return distance / self.M_IN_KM / self.duration

    def get_spent_calories(self) -> float:
        multiplayer = self.SWIM_MEAN_MULTIPLAYER * self.weight * self.duration
        return (self.get_mean_speed() + self.SWIM_MEAN_FORMULA) * multiplayer


def read_package(workout_type: str,
                 data: list
                 ) -> Training:
    """Прочитать данные полученные от датчиков."""

    training_types: dict[str, Type[Training]] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }

    if training_type := training_types.get(workout_type):
        return training_type(*data)
    raise ValueError('Неизвестный тип ренировки')


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())

    if __name__ == '__main__':
        packages: list[tuple[str, list[int]]] = [
            ('SWM', [720, 1, 80, 25, 40]),
            ('RUN', [15000, 1, 75]),
            ('WLK', [9000, 1, 75, 180]),
        ]

        for workout_type, data in packages:
            training = read_package(workout_type, data)
            main(training)
