from weapon import *
from player import *
from bubbles import *


class SearchAgent(pygame.sprite.Sprite):

    def __init__(self, image_name='player.png'):
        self.qvalues = {}

    def getAction(self, game):
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

        return self.checkCollision(nextPlayer, balls, right, False)

    def checkCollision(self, nextPlayer, balls, right, fire):
        #nextPlayer.shoot()
        nextPlayer = self.getNextStepPlayer(nextPlayer, right)
        
        #nextPlayer = getNextStepPlayer(nextPlayer, right)
        #nextPlayer = getNextStepPlayer(nextPlayer, right)
        #nextPlayer = getNextStepPlayer(nextPlayer, right)
        rightCopy = right
        collision = [[]]
        nextPlayer.shoot()
        
        for j in range(len(balls)):
                
                balls[j] = self.getNextStepBall(balls[j])
        
        for i in range(1):
            
            
            for j in range(len(balls)):
                
                if(self.check_for_bubble_collision(balls[j], nextPlayer)):
                    #print('about to collide')
                    #right = not right
                    rightCopy = not right    
                
                
                
                    
                balls[j] = self.getNextStepBall(balls[j])
            nextPlayer = self.getNextStepPlayer(nextPlayer, right)
            nextPlayer.weapon.update()
        if(rightCopy is not right):
            return rightCopy, fire
        for i in range(10):
            
            
            for j in range(len(balls)):
                
                
                if(pygame.sprite.collide_rect(balls[j], nextPlayer.weapon) and i < 5):
                   # print('fire ')
                    fire = True
                if(self.check_for_bubble_collision(balls[j], nextPlayer)):
                    
                    #print('about to collide')
                    #right = not right
                    rightCopy = not right
                    
                balls[j] = self.getNextStepBall(balls[j])
            nextPlayer = self.getNextStepPlayer(nextPlayer, right)
            nextPlayer.weapon.update()
        
            
        if(fire):
            return rightCopy, fire 
        for i in range(1):
             
            for j in range(len(balls)):
                balls[j] = self.getNextStepBall(balls[j])
                if(pygame.sprite.collide_rect(balls[j], nextPlayer.weapon)):
                   # print('fire ')
                    fire = True
                    return right, fire
            nextPlayer = self.getNextStepPlayer(nextPlayer, right)
            nextPlayer.weapon.update()
        return right, fire
    def getNextStepPlayer(self, player, right):
        rect = player.rect.copy()
        if not right and player.rect.left >= 0:
            rect = rect.move(-PLAYER_SPEED, 0)
        if right and player.rect.right <= WINDOWWIDTH:
            rect = rect.move(PLAYER_SPEED, 0)
        playerCopy = Player()
        playerCopy.rect = rect
        
        playerCopy.weapon = player.weapon
        return playerCopy

    def getNextStepBall(self, ball):
        
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
    def check_for_bubble_collision(self,bubble, player):
       #pygame.sprite.collide_rect(bubble, player.weapon) or
        return  pygame.sprite.collide_mask(bubble, player)         
