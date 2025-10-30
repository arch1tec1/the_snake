from random import choice, randint

import pygame as pg

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
CENTER_SCREEN = (GRID_WIDTH * 10, GRID_HEIGHT * 10)

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pg.display.set_caption('Змейка')

# Настройка времени:
clock = pg.time.Clock()


# Тут опишите все классы игры.
class GameObject:
    """Базовый класс для объектов игры Змейка"""

    def __init__(
        self,
        body_color=BOARD_BACKGROUND_COLOR,
        border_color=BORDER_COLOR
    ):
        self.position = CENTER_SCREEN
        self.body_color = body_color
        self.border_color = border_color

    def draw(self):
        """Отрисовка объектов на игровом поле"""
        raise NotImplementedError(f'Не реализован метод "{self.draw.__doc__}"')

    def draw_cell(self, position):
        """Отрисовка одной ячейки"""
        rect = pg.Rect(position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, self.body_color, rect)
        pg.draw.rect(screen, self.border_color, rect, 1)

    def clean_cell(self, position):
        """Затирание ячейки"""
        rect = pg.Rect(position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, BOARD_BACKGROUND_COLOR, rect)


class Apple(GameObject):
    """Класс для объекта Яблоко"""

    def __init__(
        self, body_color=APPLE_COLOR,
        border_color=APPLE_COLOR,
        busy_positions=(CENTER_SCREEN, )
    ):
        super().__init__(body_color, border_color)
        self.randomize_position(busy_positions)

    def randomize_position(self, busy_positions):
        """Генерация случайной позции Яблока в пределах Игрового поля"""
        while True:
            self.position = (
                randint(2, GRID_WIDTH - 1) * GRID_SIZE,
                randint(2, GRID_HEIGHT - 1) * GRID_SIZE
            )

            if self.position not in busy_positions:
                break

    def draw(self):
        """Отрисовка Яблока"""
        self.draw_cell(self.position)


class Snake(GameObject):
    """Класс для объекта Змейка"""

    def __init__(self, body_color=SNAKE_COLOR, border_color=BORDER_COLOR):
        super().__init__(body_color, border_color)
        self.length = 1
        self.positions = [self.position]
        self.last = self.positions[-1]
        self.direction = RIGHT  # (влево/вправо, вниз/вверх)
        self.next_direction = None

    def update_direction(self):
        """Метод обновления направления после нажатия на кнопку"""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def get_head_position(self):
        """Возвращает положение головы Змейки"""
        return self.positions[0]

    def draw(self):
        """Отрисовывает змейку на экране, затирая след"""
        for position in self.positions[:-1]:
            self.draw_cell(position)

        # Отрисовка головы змейки
        self.draw_cell(self.get_head_position())

        # Затирание последнего сегмента
        if self.last:
            self.clean_cell(self.last)

    def move(self):
        """Обновление координат тела змейки"""
        x, y = self.direction
        x_head, y_head = self.get_head_position()

        new_x, new_y = (
            (x_head + x * GRID_SIZE) % SCREEN_WIDTH,
            (y_head + y * GRID_SIZE) % SCREEN_HEIGHT
        )
        self.positions.insert(0, (new_x, new_y))

        if len(self.positions) > self.length:
            self.last = self.positions.pop(-1)

    def reset(self):
        """Сброс змейки до исходного состояния"""
        self.length = 1
        self.positions = [self.position]
        self.last = self.positions[-1]
        self.direction = choice((RIGHT, LEFT, UP, DOWN))
        self.next_direction = None


def handle_keys(game_object):
    """Обработка действий с переданным объектом"""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pg.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pg.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pg.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Логика игры"""
    # Инициализация PyGame:
    pg.init()
    # Тут нужно создать экземпляры классов.
    snake = Snake()
    apple = Apple()

    while True:
        clock.tick(5)
        handle_keys(snake)
        snake.update_direction()
        snake.move()

        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position(snake.positions)

        elif snake.get_head_position() in snake.positions[1:]:
            snake.reset()
            screen.fill(BOARD_BACKGROUND_COLOR)
            apple.randomize_position(snake.positions)

        snake.draw()
        apple.draw()
        pg.display.update()


if __name__ == '__main__':
    main()
