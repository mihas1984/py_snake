# coding: utf8

# программа пизмея - написана михасом 31.07.2017

# импортируем библиотеку пигуейм и модуль рандома

import pygame
import random

# определяем размеры игрового поля и шрифта, который будет использоваться в игре

SCREEN_X = 1000
SCREEN_Y = 700

FONT_SIZE = 20

# задаем каталог, в котором будут расположены ресурсы, после чего 
# задаем файлы для изображений сегментов змеи, головы змеи в разных направлениях, фруктов, для фона и для картинки после игры,
# к каждому из них добавляем каталог ресурсов

RES_DIR = 'images\\'

SNAKE_PART = ['snake_blue.gif', 'snake_brown.gif', 'snake_gray.gif', 'snake_green.png', 'snake_red.png']
HEAD = {'RIGHT': RES_DIR + 'snake_right.gif', 'LEFT': RES_DIR + 'snake_left.gif', 
        'UP'   : RES_DIR + 'snake_up.gif',    'DOWN': RES_DIR + 'snake_down.gif'}
FURUITS = ['snake_fruit1.png', 'snake_fruit2.png','snake_fruit3.png']
BACKGROUND = RES_DIR + 'snake_fon.png'
THE_END = RES_DIR + 'snake_fon_end.png'

for i in range(len(SNAKE_PART)):
    SNAKE_PART[i] = RES_DIR + SNAKE_PART[i]
for i in range(len(FURUITS)):
    FURUITS[i] = RES_DIR + FURUITS[i]

# создаем класс для спрайтовой графики, положение графики, картинка, цвет прозрачного фона, размеры по х и у

class Sprite:
    def __init__(self, xpos, ypos, filename):
        self.x = xpos
        self.y = ypos
        self.bitmap = pygame.image.load(filename)
        self.bitmap.set_colorkey((0, 0, 0))
        self.size_x = self.bitmap.get_size()[0]
        self.size_y = self.bitmap.get_size()[1]

# создаем метод вывода спрайта на экран

    def render(self, where):
        where.blit(self.bitmap, (self.x, self.y))

# задаем сравнение пересечения, в общем виде (пока не используется) и конкретно для двух спрайтов

def Intersect(x1, x2, y1, y2, x1_size = 1, y1_size = 1, x2_size = 1, y2_size = 1): 
    return (x1 + x1_size > x2 ) and (x2 + x2_size > x1) and (y2 + y2_size > y1) and (y1 + y1_size > y2)

def SpriteIntersect(sprite_1, sprite_2): 
    return (sprite_1.x + sprite_1.size_x > sprite_2.x) and (
            sprite_2.x + sprite_2.size_x > sprite_1.x) and (
            sprite_2.y + sprite_2.size_y > sprite_1.y) and (
            sprite_1.y + sprite_1.size_y > sprite_2.y)

# главная функция - процесс игры, получает на входе текущий счет, на выходе возвращяет счет после игры

def main(score):

# задаем начальное направление, результат игры (пока не используется), начальную длину змеи

  direction = 'RIGHT'
  result = None
  snake_lenght = 2

# задаем базовый блок змеи (он не нужен, на будущее)

  snake_base = Sprite(0, 0, RES_DIR+"snake_base.png")

# создаем змею в ввиде массива, 1 элемент будет иметь тип "голова", остальные - случайный тип

  snake = [Sprite(10, 10+i*snake_base.size_y, SNAKE_PART[random.randint(0,len(SNAKE_PART)-1)]) for i in range(snake_lenght)]
  snake[0].bitmap = pygame.image.load(HEAD[direction])
  snake[0].bitmap.set_colorkey((0, 0, 0))

# задаем случайный фрукт где-то внизу экрана

  fruit = Sprite(500, 500, FURUITS[random.randint(0,len(FURUITS)-1)])

# задаем условия для выхода из главного цикла игры и прописываем сам цикл

  exit = False

  while not exit:

# загрузить фон и разместить его на экране

    fon = pygame.image.load(BACKGROUND)
    screen.blit(fon, (0, 0))

# обработка событий. Если нажали на крестик в углу - выйти из цикла

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit = True

# если нажали на клавишу, и это одна из кнопок управления - поменять направление движения змеи и поменять картинку для ее головы 

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                direction = 'UP'
                snake[0].bitmap = pygame.image.load(HEAD['UP'])
                snake[0].bitmap.set_colorkey((0, 0, 0))
            elif event.key == pygame.K_DOWN:
                direction = 'DOWN'
                snake[0].bitmap = pygame.image.load(HEAD['DOWN'])
                snake[0].bitmap.set_colorkey((0, 0, 0))
            elif event.key == pygame.K_RIGHT:
                direction = 'RIGHT'
                snake[0].bitmap = pygame.image.load(HEAD['RIGHT'])
                snake[0].bitmap.set_colorkey((0, 0, 0))
            elif event.key == pygame.K_LEFT:
                direction = 'LEFT'
                snake[0].bitmap = pygame.image.load(HEAD['LEFT'])
                snake[0].bitmap.set_colorkey((0, 0, 0))

# обработка сегментов змеи, от последнего до первого - если один из сегментов (любой) столкнулся с головой змеи - выйти,
# кроме того, каждый предыдущий сегмент разместить на место следующего по х и у и вывести на экран

    for i in range(snake_lenght-1, 0, -1):
        if SpriteIntersect(snake[i], snake[0]): 
            exit = True
            result = 'SnakeIntersect'
        snake[i].x, snake[i].y = snake[i-1].x, snake[i-1].y
        snake[i].render(screen)

# обработка головы змеи - в зависимости от того, какое установленно направление, сдвинуться на размер одного сегмента в нужную сторону,
# обработать столкновение головы змеи с любой из границ экрана, 
# после чего вывести голову на экран

    if direction == 'UP':
        snake[0].y -= snake_base.size_y
    elif direction == 'DOWN':
        snake[0].y += snake_base.size_y
    elif direction == 'LEFT':
        snake[0].x -= snake_base.size_x
    elif direction == 'RIGHT':
        snake[0].x += snake_base.size_x

    if snake[0].x not in range(0, SCREEN_X-snake[0].size_x) or snake[0].y not in range(0, SCREEN_Y-snake[0].size_y):
        exit = True
        result = 'BorderIntersect'

    snake[0].render(screen)

# если голова соприкоснулась с фруктом: добавить 1 к очкам, создать новый сегмент змеи в ее конце со случайной раскраской,
# увеличить на единицу ее длину. После чего попробовать где-нибудь на экране разместить новый фрукт, в случайном месте - 
# если окажется, что в этом месте находится уже один из сегментов змеи, то повторить, и так до тех пор, пока фрукт где-то не появится,
# после чего уже новый фрукт где-то нарисовать на экране

    if SpriteIntersect(snake[0], fruit): 
        score += 1
        snake.append(Sprite(snake[snake_lenght-1].x, snake[snake_lenght-1].y, SNAKE_PART[random.randint(0,len(SNAKE_PART)-1)]))
        snake_lenght += 1
        newFruit = False
        while not newFruit: 
            x = random.randint(0, SCREEN_X - fruit.size_x)
            y = random.randint(0, SCREEN_Y - fruit.size_y)
            fruit = Sprite(x, y, FURUITS[random.randint(0,len(FURUITS)-1)])
            for i in range(snake_lenght):
                if SpriteIntersect(snake[i], fruit):
                    break
            else: newFruit = True
              
    fruit.render(screen)

# добавляем счет в угол экрана

    score_font = pygame.font.SysFont("comicsansms", FONT_SIZE)
    result = score_font.render("Счет: " + str(score), 1, (0,0,255))
    screen.blit(result, (1000 - FONT_SIZE*5, 0))


# разместить экран в окне, после чего установить задержку, которая будет тем меньше, чем больше собрано фруктов,
# после чего обновить экран
                         
    window.blit(screen, (0, 0))
    pygame.time.delay(max(50-score, 10))
    pygame.display.flip()

# возвращяет счет после игры

  return score

# заключительный экран, получает на входе текущий счет, на выходе выдает, нужно ли начать новую игру (да или нет)

def end(score):

  exit = False
  while not exit:

# обработка событий, если нажата кнопка n - запустить новую игру, q - выйти

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_n: 
                return True
            elif event.key == pygame.K_q:
                return False

# загрузить финальную картинку, разместить ее на экране

    fon = pygame.image.load(THE_END)
    screen.blit(fon, (0, 0))

# инициировать шрифты, вывести на экран большим шрифтом результат и маленьким информацию о том, что нажимать

    score_font = pygame.font.SysFont("comicsansms", 100)
    result = score_font.render(str(score), 1, (0,0,255))
    screen.blit(result, (500, 500))

    info_font = pygame.font.SysFont('comicsansms', 35)
    info = info_font.render("Нажмите N чтоб начать новую игру или Q чтоб выйти", 1, (255,0,255))
    screen.blit(info, (20, 650))

# вывести экран в рабочее окно, запустить перерисовку

    window.blit(screen, (0, 0))
    pygame.display.flip()


if __name__ == '__main__':

# создаем главное окно, даем ему название, создаем экран на главном окне, где все будет происходить, задаем условия выхода из цикла
# инициализируем шрифты

    window = pygame.display.set_mode((SCREEN_X, SCREEN_Y))
    pygame.display.set_caption('Пизмея')
    screen = pygame.Surface((SCREEN_X, SCREEN_Y))
    pygame.font.init()

# главный цикл игры, обнуляем счет, запускаем игру, получаем счет на выходе, запускаем итоговый экран от счета, который определяет, 
# нужно ли начинать с начала игру

    new_game = True
    while new_game:
        score = 0
        score = main(score)
        new_game = end(score)
  
