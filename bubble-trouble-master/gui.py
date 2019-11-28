from pygame.locals import *
from collections import OrderedDict

from game import *
from menu import *
from search_agent import *
from q_learning_agent import *

pygame.init()
pygame.display.set_caption('Bubble Trouble')
pygame.mouse.set_visible(True)
screen = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
clock = pygame.time.Clock()

font = pygame.font.SysFont('monospace', 30)
game = Game()
game_learning = Game()
agent = QLearningAgent()

def start_level_learning(level):
    game_learning.load_level(level)
    main_menu.is_active = False
    pygame.mouse.set_visible(False)
    clock1 = pygame.time.Clock()
    print('her')
    while game_learning.is_running:
        
        game_learning.update()
        draw_world()
        #handle_game_event()
        
        
        handle_game_automatically2(game_learning)
        
        pygame.display.update()
        if game_learning.is_completed or game_learning.game_over or \
                game_learning.level_completed or game_learning.is_restarted:
            print('1')
           # pygame.time.delay(3000)
        if game_learning.dead_player:
            print('2')
          #  pygame.time.delay(1000)
        if game_learning.is_restarted:
            print('3')
            game_learning.is_restarted = False
            game_learning._start_timer()
        clock1.tick(FPS)
        
def start_level(level):
    #for i in range (100):
       # start_level_learning(level)
    print('finished training')
    game.load_level(level)
    main_menu.is_active = False
    pygame.mouse.set_visible(False)
    
    #agent = QLearningAgent()
    while game.is_running:
        game.update()
        draw_world()
        #handle_game_event()
        
        
        handle_game_automatically2(game)
        
        pygame.display.update()
        if game.is_completed or game.game_over or \
                game.level_completed or game.is_restarted:
           
            pygame.time.delay(3000)
        if game.dead_player:
            pygame.time.delay(1000)
        if game.is_restarted:
            game.is_restarted = False
            game._start_timer()
        clock.tick(FPS)


def start_main_menu():
    while main_menu.is_active:
        main_menu.draw()
        handle_menu_event(main_menu)
        pygame.display.update()
        clock.tick(FPS)


def start_load_level_menu():
    load_level_menu.is_active = True
    while load_level_menu.is_active:
        load_level_menu.draw()
        handle_menu_event(load_level_menu)
        pygame.display.update()
        clock.tick(FPS)


def start_single_player_level_menu():
    game.is_multiplayer = False
    start_load_level_menu()


def start_multiplayer_level_menu():
    game.is_multiplayer = True
    start_load_level_menu()


def quit_game():
    pygame.quit()
    sys.exit()


def back():
    load_level_menu.is_active = False

main_menu = Menu(
    screen, OrderedDict(
        [('Single Player', start_single_player_level_menu),
            ('Two Players', start_multiplayer_level_menu),
            ('Quit', quit_game)]
    )
)

levels_available = [(str(lvl), (start_level, lvl))
                    for lvl in range(1, game.max_level_available + 1)]
levels_available.append(('Back', back))
load_level_menu = Menu(screen, OrderedDict(levels_available))


def draw_ball(ball):
    screen.blit(ball.image, ball.rect)


def draw_hex(hexagon):
    screen.blit(hexagon.image, hexagon.rect)


def draw_player(player):
    screen.blit(player.image, player.rect)


def draw_weapon(weapon):
    screen.blit(weapon.image, weapon.rect)


def draw_bonus(bonus):
    screen.blit(bonus.image, bonus.rect)


def draw_message(message, colour):
    label = font.render(message, 1, colour)
    rect = label.get_rect()
    rect.centerx = screen.get_rect().centerx
    rect.centery = screen.get_rect().centery
    screen.blit(label, rect)


def draw_timer():
    timer = font.render(str(game.time_left), 1, RED)
    rect = timer.get_rect()
    rect.bottomleft = 10, WINDOWHEIGHT - 10
    screen.blit(timer, rect)

def draw_score(player):
    timer = font.render(str(game._score(player)), 1, RED)
    rect = timer.get_rect()
    rect.bottomleft = WINDOWWIDTH - 50, WINDOWHEIGHT - 10
    screen.blit(timer, rect)


def draw_players_lives(player, is_main_player=True):
    player_image = pygame.transform.scale(player.image, (20, 20))
    rect = player_image.get_rect()
    for life_num in range(player.lives):
        if not is_main_player:
            screen.blit(player_image, ((life_num + 1) * 20, 10))
        else:
            screen.blit(
                player_image,
                (WINDOWWIDTH - (life_num + 1) * 20 - rect.width, 10)
            )


def draw_world():
    screen.fill(WHITE)
    for hexagon in game.hexagons:
        draw_hex(hexagon)
    for ball in game.balls:
        draw_ball(ball)
    for player_index, player in enumerate(game.players):
        if player.weapon.is_active:
            draw_weapon(player.weapon)
        draw_player(player)
        draw_players_lives(player, player_index)
    for bonus in game.bonuses:
        draw_bonus(bonus)
    draw_timer()
    draw_score(player)
    if game.game_over:
        draw_message('Game over!', RED)
        start_main_menu()
    if game.is_completed:
        draw_message('Congratulations! You win!!!', PURPLE)
        start_main_menu()
    if game.level_completed and not game.is_completed:
        draw_message('Well done! Level completed!', BLUE)
    if game.is_restarted:
        draw_message('Get ready!', BLUE)


def handle_game_event():
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_LEFT:
                game.players[0].moving_left = True
            elif event.key == K_RIGHT:
                game.players[0].moving_right = True
            elif event.key == K_SPACE and not game.players[0].weapon.is_active:
                game.players[0].shoot()
            elif event.key == K_ESCAPE:
                quit_game()
            if game.is_multiplayer:
                if event.key == K_a:
                    game.players[1].moving_left = True
                elif event.key == K_d:
                    game.players[1].moving_right = True
                elif event.key == K_LCTRL and \
                        not game.players[1].weapon.is_active:
                    game.players[1].shoot()
        if event.type == KEYUP:
            if event.key == K_LEFT:
                game.players[0].moving_left = False
            elif event.key == K_RIGHT:
                game.players[0].moving_right = False
            if game.is_multiplayer:
                if event.key == K_a:
                    game.players[1].moving_left = False
                elif event.key == K_d:
                    game.players[1].moving_right = False
        if event.type == QUIT:
            quit_game()

def handle_game_auto_event(events, game):
    for event in events:
      #  print(event.type)
      #  print('key ' , event.key)
        if event.type == KEYDOWN:
            if event.key == K_LEFT:
                game.players[0].moving_left = True
            elif event.key == K_RIGHT:
                game.players[0].moving_right = True
            elif event.key == K_SPACE and not game.players[0].weapon.is_active:
                game.players[0].shoot()
            elif event.key == K_ESCAPE:
                quit_game()
            if game.is_multiplayer:
                if event.key == K_a:
                    game.players[1].moving_left = True
                elif event.key == K_d:
                    game.players[1].moving_right = True
                elif event.key == K_LCTRL and \
                        not game.players[1].weapon.is_active:
                    game.players[1].shoot()
        if event.type == KEYUP:
            if event.key == K_LEFT:
                game.players[0].moving_left = False
            elif event.key == K_RIGHT:
                game.players[0].moving_right = False
            if game.is_multiplayer:
                if event.key == K_a:
                    game.players[1].moving_left = False
                elif event.key == K_d:
                    game.players[1].moving_right = False
        if event.type == QUIT:
            quit_game()
def handle_game_automatically(game):
    events = [];
    minBall = None
    minDist = WINDOWWIDTH
    player1 = game.players[0]
    print("!!!! : ",len(game.balls))
    ballsInLeftWithin75 = 0
    ballsInRightWithin75 = 0
    ballsWithin50 = 0
    for ball in game.balls:
        if abs(ball.rect[0] - player1.rect[0]) <= 50 :
            ballsWithin50 += 1
        ballToLeftOfPlayer = ball.rect[0] < player1.rect[0]
        if ballToLeftOfPlayer:
            if player1.rect[0] - ball.rect[0] <= 75:
                ballsInLeftWithin75 += 1
        else:
            print('right of player')
            if ball.rect[0] - player1.rect[0] <= 75:
                print('within 75')
                ballsInRightWithin75 += 1
        dirDist = 0;
        if ballToLeftOfPlayer:
            if ball.speed[0] < 0:
                dirDist = ball.rect[0]
        else:
            if ball.speed[0] > 0:
                print('speed > 0')
                dirDist = WINDOWWIDTH - ball.rect[0];
        #(ballToLeftOfPlayer ? (ball.speed[0] > 0 ? 0 : ball.rect[0]) : (ball.speed[0] < 0 ? 0 : WINDOWWIDTH - ball.rect[0]))
        ballDist = abs(ball.rect[0] - player1.rect[0]) + (dirDist * 2)
        print('dist',ballDist)
        if ballDist < minDist:
            ballDist = minDist
            minBall = ball;

    if ballsInLeftWithin75 + ballsInRightWithin75 > 1:
        events.append(pygame.event.Event(KEYDOWN, key=K_SPACE))
        if ballsInLeftWithin75 > ballsInRightWithin75:
            events.append(pygame.event.Event(KEYDOWN, key=K_RIGHT))
        else:
            events.append(pygame.event.Event(KEYDOWN, key=K_LEFT))
        handle_game_auto_event(events)            
        return    

    if minBall is None:
        print('minball is nones')
        return
    
    if abs(minBall.rect[0] - player1.rect[0]) < 100:
        if ballsWithin50 > 0 or ballsInRightWithin75 > 0 or ballsInLeftWithin75 > 0:
            events.append(pygame.event.Event(KEYDOWN, key=K_SPACE))
        if minBall.rect[0] < player1.rect[0]:
            if minBall.speed[0] > 0:
                events.append(pygame.event.Event(KEYDOWN, key=K_SPACE))
            if player1.rect[0] < WINDOWWIDTH - 100:
                events.append(pygame.event.Event(KEYDOWN, key=K_RIGHT))
            else:
                events.append(pygame.event.Event(KEYDOWN, key=K_LEFT))
        else:
            if minBall.speed[0] < 0:
                events.append(pygame.event.Event(KEYDOWN, key=K_SPACE))
            if player1.rect[0] > 100:
                events.append(pygame.event.Event(KEYDOWN, key=K_LEFT))
            else:
                events.append(pygame.event.Event(KEYDOWN, key=K_RIGHT))
    else:
        if minBall.rect[0] < player1.rect[0]:
            events.append(pygame.event.Event(KEYUP, key=K_RIGHT))
            events.append(pygame.event.Event(KEYDOWN, key=K_LEFT))
        else:
            events.append(pygame.event.Event(KEYUP, key=K_LEFT))
            events.append(pygame.event.Event(KEYDOWN, key=K_RIGHT))
    handle_game_auto_event(events)
    
def handle_game_automatically2(game):
    events = []
    
    """    
    events = [];
    minBall = None
    minDist = WINDOWWIDTH
    player1 = game.players[0]
  #  print("!!!! : ",len(game.balls))
    ballsInLeftWithin75 = 0
    ballsInRightWithin75 = 0
    ballsWithin50 = 0
    ballsDistance = []
    fire = False
    for ball in game.balls:
       # print('y coor', ball.rect[1])
        fire = abs(ball.rect.centerx - player1.rect.centerx) <= 50 
        ballsDistance.append(ball.rect[0] - player1.rect[0])
        if(minDist >  abs(ball.rect[0] - player1.rect[0])):
            minDist = abs(ball.rect[0] - player1.rect[0])
            minBall = ball
            

    if(minBall ==None):
        return
    if minDist > 30:
        right = minBall.rect.centerx > player1.rect.centerx
    else:
        #print('here')
        right = player1.moving_right
    
    balls = game.balls.copy()
    nextPlayer = player1
    """
    action = agent.getAction(game)

    if(action == None):
        return
    #right, fire = action
  #  print(action)
    move,fire = action
    
    
   # print('orginal ball', minBall.rect[0], minBall.rect[1])
   # print('next ball', nextBall.rect[0], nextBall.rect[1],)
   # print('orginal player', player1.rect[0], player1.rect[1])
   # print('next player', nextPlayer.rect[0], nextPlayer.rect[1],)
   # print(action)
    if fire == 'FIRE':
        #events.append(pygame.event.Event(KEYUP, key=K_SPACE))
        events.append(pygame.event.Event(KEYDOWN, key=K_SPACE))
    if move == 'RIGHT':
        #print('right')
        events.append(pygame.event.Event(KEYUP, key=K_LEFT))
        events.append(pygame.event.Event(KEYDOWN, key=K_RIGHT))
    elif move == 'LEFT':
        #print('left')
        events.append(pygame.event.Event(KEYUP, key=K_RIGHT))
        events.append(pygame.event.Event(KEYDOWN, key=K_LEFT))
    

    handle_game_auto_event(events, game)
    

def handle_game_automatically1(game):
    events = []
    """    
    events = [];
    minBall = None
    minDist = WINDOWWIDTH
    player1 = game.players[0]
  #  print("!!!! : ",len(game.balls))
    ballsInLeftWithin75 = 0
    ballsInRightWithin75 = 0
    ballsWithin50 = 0
    ballsDistance = []
    fire = False
    for ball in game.balls:
       # print('y coor', ball.rect[1])
        fire = abs(ball.rect.centerx - player1.rect.centerx) <= 50 
        ballsDistance.append(ball.rect[0] - player1.rect[0])
        if(minDist >  abs(ball.rect[0] - player1.rect[0])):
            minDist = abs(ball.rect[0] - player1.rect[0])
            minBall = ball
            

    if(minBall ==None):
        return
    if minDist > 30:
        right = minBall.rect.centerx > player1.rect.centerx
    else:
        #print('here')
        right = player1.moving_right
    
    balls = game.balls.copy()
    nextPlayer = player1
    """
    action = agent.getAction(game)

    if(action == None):
        return
    right, fire = action
    
    
    
   # print('orginal ball', minBall.rect[0], minBall.rect[1])
   # print('next ball', nextBall.rect[0], nextBall.rect[1],)
   # print('orginal player', player1.rect[0], player1.rect[1])
   # print('next player', nextPlayer.rect[0], nextPlayer.rect[1],)
   
   
    
    
    if fire:
        #events.append(pygame.event.Event(KEYUP, key=K_SPACE))
        events.append(pygame.event.Event(KEYDOWN, key=K_SPACE))
    if right:
        #print('right')
        events.append(pygame.event.Event(KEYUP, key=K_LEFT))
        events.append(pygame.event.Event(KEYDOWN, key=K_RIGHT))
    else:
        #print('left')
        events.append(pygame.event.Event(KEYUP, key=K_RIGHT))
        events.append(pygame.event.Event(KEYDOWN, key=K_LEFT))
    

    handle_game_auto_event(events)
def checkCollision(nextPlayer, balls, right, fire):
    #nextPlayer.shoot()
    nextPlayer = getNextStepPlayer(nextPlayer, right)
    
    #nextPlayer = getNextStepPlayer(nextPlayer, right)
    #nextPlayer = getNextStepPlayer(nextPlayer, right)
    #nextPlayer = getNextStepPlayer(nextPlayer, right)
    rightCopy = right
    collision = [[]]
    nextPlayer.shoot()
    
    for j in range(len(balls)):
            
            balls[j] = getNextStepBall(balls[j])
    
    for i in range(1):
        
        
        for j in range(len(balls)):
            
            if(check_for_bubble_collision(balls[j], nextPlayer)):
                #print('about to collide')
                #right = not right
                rightCopy = not right    
            
            
            
                
            balls[j] = getNextStepBall(balls[j])
        nextPlayer = getNextStepPlayer(nextPlayer, right)
        nextPlayer.weapon.update()
    if(rightCopy is not right):
        return rightCopy, fire
    for i in range(10):
        
        
        for j in range(len(balls)):
            
            
            if(pygame.sprite.collide_rect(balls[j], nextPlayer.weapon) and i < 5):
               # print('fire ')
                fire = True
            if(check_for_bubble_collision(balls[j], nextPlayer)):
                
                #print('about to collide')
                #right = not right
                rightCopy = not right
                
            balls[j] = getNextStepBall(balls[j])
        nextPlayer = getNextStepPlayer(nextPlayer, right)
        nextPlayer.weapon.update()
    
        
    if(fire):
        return rightCopy, fire 
    for i in range(1):
         
        for j in range(len(balls)):
            balls[j] = getNextStepBall(balls[j])
            if(pygame.sprite.collide_rect(balls[j], nextPlayer.weapon)):
               # print('fire ')
                fire = True
                return right, fire
        nextPlayer = getNextStepPlayer(nextPlayer, right)
        nextPlayer.weapon.update()
    return right, fire
def getNextStepPlayer(player, right):
    rect = player.rect.copy()
    if not right and player.rect.left >= 0:
        rect = rect.move(-PLAYER_SPEED, 0)
    if right and player.rect.right <= WINDOWWIDTH:
        rect = rect.move(PLAYER_SPEED, 0)
    playerCopy = Player()
    playerCopy.rect = rect
    
    playerCopy.weapon = player.weapon
    return playerCopy

def getNextStepBall(ball):
    
    speed = ball.speed.copy()
    speed[1] += GRAVITY
    rect = ball.rect.copy()
    rect = rect.move(speed)
    if rect.left < 0 or rect.right > WINDOWWIDTH:
            speed[0] = -speed[0]
    if rect.top < 0 or rect.bottom > WINDOWHEIGHT:
        speed[1] = -speed[1]
    rect.left = ball._clip(rect.left, 0, WINDOWWIDTH)
    rect.right = ball._clip(rect.right, 0, WINDOWWIDTH)
    rect.top = ball._clip(rect.top, 0, WINDOWHEIGHT)
    rect.bottom = ball._clip(rect.bottom, 0, WINDOWHEIGHT)
    #self.image.get_rect(centerx=x, centery=y)
    return Ball(rect.centerx , rect.centery, ball.size, speed)
    
    
def check_for_bubble_collision(bubble, player):
       #pygame.sprite.collide_rect(bubble, player.weapon) or
        return  pygame.sprite.collide_mask(bubble, player)
def handle_menu_event(menu):
    for event in pygame.event.get():
        
        if event.type == pygame.QUIT:
            quit_game()

        elif event.type == KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if menu == main_menu:
                    quit_game()
                else:
                    start_main_menu()
            if (event.key == pygame.K_UP or event.key == pygame.K_DOWN)\
                    and menu.current_option is None:
                menu.current_option = 0
                pygame.mouse.set_visible(False)
            elif event.key == pygame.K_UP and menu.current_option > 0:
                menu.current_option -= 1
            elif event.key == pygame.K_UP and menu.current_option == 0:
                menu.current_option = len(menu.options) - 1
            elif event.key == pygame.K_DOWN \
                    and menu.current_option < len(menu.options) - 1:
                menu.current_option += 1
            elif event.key == pygame.K_DOWN \
                    and menu.current_option == len(menu.options) - 1:
                menu.current_option = 0
            elif event.key == pygame.K_RETURN and \
                    menu.current_option is not None:
                option = menu.options[menu.current_option]
                if not isinstance(option.function, tuple):
                    option.function()
                else:
                    option.function[0](option.function[1])

        elif event.type == MOUSEBUTTONUP:
            for option in menu.options:
                if option.is_selected:
                    if not isinstance(option.function, tuple):
                        option.function()
                    else:
                        option.function[0](option.function[1])

        if pygame.mouse.get_rel() != (0, 0):
            pygame.mouse.set_visible(True)
            menu.current_option = None
