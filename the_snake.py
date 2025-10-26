import pygame
from random import randint

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

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
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


# Тут опишите все классы игры.
class GameObject:
    """Базовый класс для объектов игры Змейка"""

    def __init__(self):
        self.position = (320, 240)
        self.body_color = None

    def draw(self):
        """Отрисовка объектов на игровом поле"""
        pass


class Apple(GameObject):
    """Класс для объекта Яблоко"""

    @staticmethod
    def randomize_position():
        """Генерация случайной позции Яблока в пределах Игрового поля"""
        position = (randint(2, 31) * 20, randint(2, 23) * 20)
        return position

    def __init__(self):
        super().__init__()
        Apple.body_color = APPLE_COLOR
        Apple.position = self.randomize_position()

    @classmethod
    def draw(cls):
        """Отрисовка Яблока"""
        rect = pygame.Rect(cls.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, cls.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс для объекта Змейка"""

    def __init__(self):
        super().__init__()
        self.length = 1
        self.positions = [self.position]
        self.last = self.positions[-1]
        self.direction = RIGHT  # (влево/вправо, вниз/вверх)
        self.next_direction = None
        self.body_color = SNAKE_COLOR

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
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    @staticmethod
    def bump_borders(new_position):
        """Проверка на врезание в границы"""
        x, y = new_position[0], new_position[1]
        if x not in range(0, 641) or y not in range(0, 481):
            return True

    def bump_yourself(self, new_position):
        """Проверка на врезание в себя"""
        if tuple(new_position) in self.positions:
            return True

    def eat_apple(self, new_position):
        """Проверка на то, что скушали яблоко"""
        if tuple(new_position) == Apple.position:
            new_apple = Apple()
            new_apple.draw()
            return True

    def clean_board(self):
        """Очищает игровое поле"""
        for position in self.positions:
            last_rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def move(self):
        """
        1. Обновление координат тела змейки
        2. Обновление тела змейки при съедании яблочка
        """
        self.last = self.positions[-1]
        delta_position = (self.direction[0] * 20, self.direction[1] * 20)
        for indx, position in enumerate(self.positions):
            if indx == 0:
                new_position = []
                for coord in range(2):
                    one_cord = position[coord] + delta_position[coord]
                    new_position.append(one_cord)
                if self.bump_borders(new_position):
                    print('Вы врезались в границу игровой зоны!')
                    self.clean_board()
                    self.reset()
                    break
                elif self.bump_yourself(new_position):
                    print('Вы врезались в себя!')
                    self.clean_board()
                    self.reset()
                    break
                elif self.eat_apple(new_position):
                    self.positions.insert(0, tuple(new_position))
                    self.length += 1
                last_positions = self.positions.copy()
                last_positions.insert(0, 0)
                self.positions[indx] = tuple(new_position)
            else:
                self.positions[indx] = last_positions[indx]

    def reset(self):
        """Сброс змейки до исходного состояния"""
        self.length = 1
        self.positions = [self.position]
        self.last = self.positions[-1]
        self.direction = RIGHT  # (влево/вправо, вниз/вверх)
        self.next_direction = None
        self.body_color = SNAKE_COLOR


def handle_keys(game_object):
    """Обработка действий с переданным объектом"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Логика игры"""
    # Инициализация PyGame:
    pygame.init()
    # Тут нужно создать экземпляры классов.
    apple = Apple()
    snake = Snake()
    apple.draw()
    snake.draw()

    while True:
        clock.tick(5)
        handle_keys(snake)
        snake.update_direction()
        snake.move()
        snake.draw()
        pygame.display.update()


if __name__ == '__main__':
    main()
