# Load Minim library
add_library("Minim")
import os
import random

# Initialize PATH
# PATH = os.getcwd()
PATH = os.path.dirname(os.getcwd())


minim=Minim(this)


# Constants
NUM_ROWS = 7
NUM_COLUMNS = 7
PLATFORM_WIDTH = 80
PLATFORM_HEIGHT = 20
MAX_MINE = 5
MAX_SPEED = 20
MIN_SPEED = 5
SCREEN_W = 1400
SCREEN_H = 850
GROUND = 700

MAX_NUM_MINE=6
MAX_MINE_SPEED=5
MIN_MINE_SPEED=3

step = 0

# Define Player class
class Player:
   
    def __init__(self, x, y, r, img, slice_w, slice_h, num_slices):
        self.x = x
        self.y = y
        self.r = r
        self.g = GROUND
        self.vx = 0
        self.vy = 1
        self.img = loadImage(PATH + "/images/" + img)
        self.slice_w = slice_w
        self.slice_h = slice_h
        self.num_slices = num_slices
        self.slice = 0
        self.dir = RIGHT
        self.life = 3
        self.score = 0
        self.freeze_timer = 0
        self.frozen = False
        self.bullets = []
        self.num_bullets = 3  
        self.score_added=False
    
    # Gravity handling method to simulate gravity effect
    def gravity(self):
        # Check each platform to determine if the player is standing on one
        if game.scene_L1.visible:
            for platform in game.scene_L1.platforms:
                
                if self.y + self.r <= platform.y and self.y + self.r <= platform.y + 25 and self.x + self.r >= platform.x and self.x - self.r <= platform.x + platform.w:
                    self.g = platform.y 
                    break
                else:
                    self.g = GROUND
        # Repeat similar checks for other levels          
        elif game.scene_L2.visible:
            for platform in game.scene_L2.platforms:
                if self.y + self.r <= platform.y and self.y + self.r <= platform.y + 25 and self.x + self.r >= platform.x and self.x - self.r <= platform.x + platform.w:
                    self.g = platform.y 
                    break
                else:
                    self.g = GROUND
                
        elif game.scene_L3.visible: 
            for platform in game.scene_L3.platforms:
                if self.y + self.r <= platform.y and self.y + self.r <= platform.y + 25 and self.x + self.r >= platform.x and self.x - self.r <= platform.x + platform.w:
                    self.g = platform.y 
                    break
                else:
                    self.g = GROUND
        
        if self.y + self.r >= self.g:
            self.vy = 0
        else:
            self.vy += 0.75
            if self.y + self.r + self.vy > self.g:
                self.y = self.g - self.r
                self.vy = 0
    
    
    # Implement distance method
    def distance(self, other):
        return ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5
    
    
    # Implement get_powerups method
    def get_powerups(self):
        for item in game.power_ups:
            for power_up in item:
                if self.distance(power_up) <= self.r + power_up.r:
                    item.remove(power_up)
                    if power_up.collectible == "L":   # If it's a life power-up
                        if self.life < 5:
                            self.life += 1
                    if power_up.collectible == "B":   # If it's a bullet power-up
                        if self.num_bullets < 5:
                            self.num_bullets += 1
                        break
            
    # Implement method to shoot bullets
    def shoot(self):
        if self.num_bullets > 0:
            new_bullet = Bullet(self.x, self.y, 15, self)
            self.bullets.append(new_bullet)
            self.num_bullets = self.num_bullets - 1
    
    def reach_gold(self):
        # Check if player's center is inside the gold's rectangle
        if (self.x > game.gold.x and self.x < game.gold.x + game.gold.w and
            self.y > game.gold.y and self.y < game.gold.y + game.gold.h):
            return True
        else:
            return False

    # Implement update method to handle bullets
    def update_bullets(self):
        for bullet in self.bullets:
            bullet.update()
            # Remove bullets that have moved off the screen
            if bullet.x < 0 or bullet.x > SCREEN_W:
                self.bullets.remove(bullet)
                break

    # Implement display method to render bullets
    def display_bullets(self):
        for bullet in self.bullets:
            bullet.display()
    
    # Method to handle hits by bullets from another player
    def hit(self,other):
        for bullet in other.bullets:
            for player in game.players:  
                if player is not bullet.shooter and player.distance(bullet) <= self.r + bullet.r:
                    # Bullet hit this player
                    other.bullets.remove(bullet)
                    return True

    # Implement check_dead method
    def check_dead(self):
        return self.life == 0
    
    # Update method to apply gravity and move the player
    def update(self):
        self.gravity()
        self.x += self.vx
        self.y += self.vy
    
    def display(self):
        self.update()
        if self.dir == RIGHT:
            image(self.img, self.x - self.slice_w//2 , self.y - self.slice_h//2, self.slice_w, self.slice_h, self.slice * self.slice_w, 0, (self.slice + 1) * self.slice_w, self.slice_h )
        elif self.dir == LEFT:
            image(self.img, self.x - self.slice_w//2 , self.y - self.slice_h//2, self.slice_w, self.slice_h, (self.slice + 1) * self.slice_w, 0, self.slice * self.slice_w, self.slice_h )

# Define Player1 class
class Player1(Player):
   
    def __init__(self, x, y, r):
        Player.__init__(self, x, y, r,"sonc.png", 111, 100, 8)
        self.key_handler = {'a': False, 'd': False, 'w': False, 's': False}
    
    # Update method for Player1, handling movements and actions based on key presses
    def update(self):
        self.gravity()
        
        if self.key_handler['a'] == True:
            self.vx = -10
            self.dir = LEFT
        elif self.key_handler['d'] == True:
            self.vx = 10
            self.dir = RIGHT
        else:
            self.vx = 0
        
        if self.key_handler['w'] == True and self.y + self.r == self.g:
            self.vy = -13.5
        
        if frameCount % 2 == 0 and self.vx != 0 and self.vy == 0:
            self.slice = (self.slice + 1) % self.num_slices
        
        elif self.vx == 0:
            self.slice = 5 # Define standing position
        
        if not self.frozen:  # Check if the player is not frozen
            self.x += self.vx
            self.y += self.vy


        if self.frozen:
            if self.freeze_timer > 0:
                self.freeze_timer -= 1  # Decrement freeze timer
            else:
                self.frozen = False  # End freeze effect
        

        self.get_powerups()# Check for power-ups
        self.reach_gold() # Check if the player has reached the gold


        if self.x - self.r < 0:
            self.x = self.r  # Define left bound
        
        elif self.x + self.r > SCREEN_W - self.r:
            self.x = SCREEN_W - self.r*2  # Define right bound
            

# Define Player2 class
class Player2(Player):
    
    def __init__(self, x, y, r):
        Player.__init__(self, x, y, r, "sonc2.png", 111, 100, 8)
        self.key_handler = {LEFT: False, RIGHT: False, UP: False, DOWN: False}
        self.dir = LEFT
    
    # Update method for Player2, similar to Player1 but with controls for the second playe
    def update(self):
        self.gravity()
        
        if self.key_handler[LEFT] == True:
            self.vx = -10
            self.dir = LEFT
        
        elif self.key_handler[RIGHT] == True:
            self.vx = 10
            self.dir = RIGHT
            
        else:
            self.vx = 0
        
        if self.key_handler[UP] == True and self.y + self.r == self.g:
            self.vy = -13.5
        
        if frameCount % 2 == 0 and self.vx != 0 and self.vy == 0:
            self.slice = (self.slice + 1) % self.num_slices
        
        elif self.vx == 0:
            self.slice = 5 # Define standing position
        
        if not self.frozen:  # Check if the player is not frozen
            self.x += self.vx
            self.y += self.vy
        
        if self.frozen:
            if self.freeze_timer > 0:
                self.freeze_timer -= 1  # Decrement freeze timer
            else:
                self.frozen = False  # End freeze effect
    

        self.get_powerups()# Check for power-ups
        self.reach_gold()# Check if the player has reached the gold

    
        if self.x - self.r < 0:
            self.x = self.r  # Define left bound
        
        elif self.x + self.r > SCREEN_W - self.r:
            self.x = SCREEN_W - self.r*2  # Define right bound
    
   
# Define Bullet class
class Bullet:
    def __init__(self, x, y, r, shooter):
        self.x = x
        self.y = y
        self.r = r
        self.img = loadImage(PATH + "/images/bul4.png")
        self.dir = shooter.dir
        self.vx = 0
        self.shooter = shooter # Store a reference to the shooter

    # Implement update method
    def update(self):
        if self.dir == LEFT:
            self.vx = -15  # Define bullet's speed
        elif self.dir == RIGHT:
            self.vx = 15  # Define bullet's speed
        self.x += self.vx  # Define horizontal movement

    # Implement display method
    def display(self):
        self.update()
        image(self.img, self.x , self.y, 15, 15)


# Define Platform class
class Platform:
    
    def __init__(self, x, y, w, h, img_name):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.vx = 0
        self.img = loadImage(PATH + "/images/" + img_name)

    # Implement display method
    def display(self):
        image(self.img, self.x , self.y + 25 , self.w, self.h)

# Define Movable_Platform class
class Movable_Platform(Platform):
    
    def __init__(self, x, y, w, h, left_bound, right_bound,img_name):
        Platform.__init__(self, x, y, w, h,img_name)
        self.left_bound = left_bound
        self.right_bound = right_bound
        self.vx = -4
        self.dir = None
        self.img = loadImage(PATH + "/images/" + img_name)

    # Implement update method
    def update(self):
        if self.x > self.right_bound:
            self.vx *= -1
            self.dir = LEFT
        elif self.x < self.left_bound:
            self.vx *= -1
            self.dir = RIGHT
        self.x += self.vx  # Define horizontal movement

    # Implement display method
    def display(self):
        self.update()
        image(self.img, self.x, self.y + 25, self.w, self.h)

# Define Power_ups class
class Power_ups:
    def __init__(self, x, y, w, h, r, img_name, collectible):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.r = r
        self.collectible = collectible
        self.img = loadImage(PATH + "/images/" + img_name)

    # Implement display method
    def display(self):
        if self.collectible == "L":
            image(self.img, self.x, self.y, self.w, self.h)# Draw life power-up
        if self.collectible == "B":
            image(self.img, self.x, self.y, self.w, self.h)# Draw bullet power-up

# Define Button class
class Button:
    def __init__(self, x, y,w,h,str,color1_r=0, color1_g=0,color1_b=0, color2_r=120, color2_g=120,color2_b=120):
        self.x=x
        self.y=y
        self.w=w
        self.h=h
        self.str=str
        self.c1_r=color1_r
        self.c1_g=color1_g
        self.c1_b=color1_b
        self.c2_r=color2_r
        self.c2_g=color2_g
        self.c2_b=color2_b
    
    def display(self):
        stroke(0)
        strokeWeight(3)
        
        if self.x<=mouseX<=self.x+self.w and self.y<=mouseY<=self.y+self.h:
            fill(self.c2_r, self.c2_g,self.c2_b)# Change color on hover
        else:
            fill(self.c1_r,self.c1_g,self.c1_b)# Default color
        rect(self.x,self.y,self.w,self.h)
        textSize(35)
        fill(255)
        text(self.str, self.x+int(self.w/6),self.y+int(self.h*0.6))

# Bat class for creating bat obstacles
class Bat(list):
    def __init__(self,x,y):
        self.x=x
        self.y=y
        self.visible=False
        self.img=[]
        for i in range(5):
            self.img.append(loadImage(PATH+"/images/bat_{}.png".format(i)))
        global bat_last_show_time
        bat_last_show_time=millis()# Record the last time the bat was shown
        
    # Display method for Bat, handles animation and visibility
    def display(self):
        currentTime=millis()
        global bat_last_show_time
        if currentTime-bat_last_show_time>=4000:
            self.visible=True
            image(self.img[frameCount/10%5], self.x, self.y)
            if currentTime-bat_last_show_time >=5000:
                bat_last_show_time=millis()# Reset the timer
                self.visible=False
        if self.visible:
            if dist(self.x+75, self.y-35,game.player1.x+43, game.player1.y-75)<=80:
                game.player1.life-=1
            if dist(self.x+75, self.y-35,game.player2.x+43, game.player2.y-75)<=80:
                game.player2.life-=1

# Mine_Group class for managing groups of bombs
class Mine_Group(list):
    def __init__(self,num_v, num_h):
        self.num_v=num_v
        self.num_h=num_h
        
        for i in range(self.num_v):
            temp_v=random.randint(SCREEN_W*0.1,SCREEN_W*0.9)
            temp_speed_v=random.randint(MIN_MINE_SPEED,MAX_MINE_SPEED)
                     
            self.append(Mine(temp_v,0,temp_speed_v,"V"))
            
        self.append(Mine(int(SCREEN_W/2),0,temp_speed_v,"V"))
            
        for j in range(self.num_h):
            temp_hl=random.randint(100,SCREEN_H-300)
            temp_hr=random.randint(100,SCREEN_H-300)
            temp_speed_h=random.randint(MIN_MINE_SPEED+2,MAX_MINE_SPEED+4)
            self.append(Mine(0,temp_hl,temp_speed_h,"HL"))
            self.append(Mine(SCREEN_W,temp_hr,-temp_speed_h,"HR"))
            
    def display(self):
        for min in self:
            min.display()
            
    def update(self):
        for min in self:
            min.update()
            if min.check_visible()==False:
                if min.dir=="V":
                    min.y=0
                    min.x=random.randint(SCREEN_W*0.1,SCREEN_W*0.9)
                    min.speed=random.randint(MIN_MINE_SPEED,MAX_MINE_SPEED)
                    min.visible=True
                    break
                elif min.dir=="HL":
                    min.x=0
                    min.y=random.randint(100,SCREEN_H-270)
                    min.speed=random.randint(MIN_MINE_SPEED+2,MAX_MINE_SPEED+5)
                    min.visible=True
                    break

                else:
                    min.x=SCREEN_W
                    min.y=random.randint(100,SCREEN_H-270)
                    min.speed=-random.randint(MIN_MINE_SPEED+2,MAX_MINE_SPEED+5)
                    min.visible=True
                    break

# Define Mine class for bomb obstacles
class Mine():
    def __init__(self,x,y,speed,dir):
        self.x=x
        self.y=y
        self.visible=True
        self.speed=speed
        self.dir=dir
        self.img=loadImage(PATH+"/images/mine4.png")
        self.explosion=loadImage(PATH+"/images/explosion.png")

    
    def display(self):
        if self.dir=="HL":
            self.x=0
            self.y=random.randint(0,SCREEN_H-155)
            image(self.img,self.x,self.y)
        elif self.dir=="HR":
            self.x=SCREEN_W
            self.y=random.randint(0,SCREEN_H-155)
            image(self.img, self.x, self.y)
        elif self.dir=="V":
            self.x=random.randint(0,SCREEN_W-30)
            self.y=0
            image(self.img,self.x, self.y)
    
    def update(self):
        if self.visible:
            if self.dir=="HL" or self.dir=="HR":
                self.x+=self.speed
            elif self.dir=="V":
                self.y+=self.speed
            image(self.img,self.x,self.y)
    
    # Method to check if the bomb is still visible on the screen
    def check_visible(self):
        if (self.dir=="HL" and self.x>SCREEN_W-60) or (self.dir=="HR" and self.x<0) or self.y>GROUND-60:            
            self.explode()
            self.visible=False
            return False
        elif dist(self.x, self.y,game.player1.x, game.player1.y)<=40:
            self.explode()
            game.player1.life-=1
            self.visible=False
            return False
        elif dist(self.x, self.y, game.player2.x, game.player2.y)<=40:
            self.explode()
            self.visible=False
            game.player2.life-=1
            self.visible=False
            return False
        
        else:
            return True
   
    # Method to handle explosions 
    def explode(self):
        image(self.explosion,self.x,self.y)


class Gold:
    def __init__(self,x,y,w,h):
        self.x=x
        self.y=y
        self.w=w
        self.h=h
        self.img=loadImage(PATH+"/images/gold.png")
    
    def display(self):
        image(self.img, self.x, self.y, self.w, self.h)


# Define Game class
class Game:
    def __init__(self):
        self.player1 = Player1(50, GROUND - 30, 10)
        self.player2 = Player2(1230, GROUND - 30, 10)
        self.players = []
        self.mine_group = []
        self.platforms = []
        self.falling_obstacles = []
        self.power_ups = []
        self.start=True
        self.game_over=False
        self.scene_L1_instruction=Scene_Level_Instruction(1)
        self.scene_L2_instruction=Scene_Level_Instruction(2)
        self.scene_L3_instruction=Scene_Level_Instruction(3)
        self.level1=False
        self.level2=False
        self.level3=False
        self.winner=0
        self.StartandSelect=Start_Select()
        self.scene_L1=Scene_L1()
        self.scene_L2=Scene_L2()
        self.scene_L3=Scene_L3()
        self.scene_gameover=Scene_GameOver()
        self.music_start=minim.loadFile(PATH+"/sounds/Menu_BGM.mp3",1024)
        self.music_L1=minim.loadFile(PATH+"/sounds/Level1_BGM.mp3",1024)
        self.music_L2=minim.loadFile(PATH+"/sounds/level2_BGM.mp3",1024)
        self.music_L3=minim.loadFile(PATH+"/sounds/level3_BGM.mp3",1024)
        self.music_gameover=minim.loadFile(PATH+"/sounds/ms1.mp3",1024)
        self.gold=Gold(int(SCREEN_W/2)-70,0,100,100)

        self.players.append(self.player1)
        self.players.append(self.player2)
        
        self.power_ups.append(self.scene_L2.power_ups)
        self.power_ups.append(self.scene_L3.power_ups)          
    
    def run(self):    
        if self.start==True:
            self.StartandSelect.display()
            self.show_music(0)
        elif self.scene_L1_instruction.visible==True:
            self.scene_L1_instruction.display()
            self.show_music(0)
        elif self.scene_L2_instruction.visible==True:
            self.scene_L2_instruction.display()
            self.show_music(0)
        elif self.scene_L3_instruction.visible==True:
            self.scene_L3_instruction.display()
            self.show_music(0)
        elif self.scene_L1.visible:
            self.scene_L1.display()
            self.show_music(1)
            if self.check_winning():
                self.scene_L1.visible=False
        elif self.scene_L2.visible:
            self.scene_L2.display()
            self.show_music(2)
            if self.check_winning():
                self.scene_L2.visible=False
        elif self.scene_L3.visible:
            self.scene_L3.display()
            self.show_music(3)
            if self.check_winning():
                self.scene_L3.visible=False
        elif self.game_over:
            self.scene_gameover.display()
     
    # Method to reset the game state for Level 2       
    def reset_level2(self):
        game = Game()
        
        # self.player1.life = 5
        # self.player1.bullets = []
        # self.player2.bullets = []
        # self.player1.num_bullets = 3
        # self.player2.life = 5
        # self.player2.num_bullets = 3
        # self.player1.x = 50
        # self.player1.y = GROUND - 50
        # self.player2.x = SCREEN_W - 50
        # self.player2.y = GROUND - 50
        # self.scene_L2.visible = True
        # self.music_start.pause()
        # self.music_L1.loop()
      
    # Method to reset the game state for Level 3  
    def reset_level3(self):
        game = Game()
        
        # self.player1.life = 5
        # self.player1.bullets = []
        # self.player2.bullets = []
        # self.player1.num_bullets = 3
        # self.player2.life = 5
        # self.player2.num_bullets = 3
        # self.player1.x = 0
        # self.player1.y = GROUND - 50
        # self.player2.x = SCREEN_W - 50
        # self.player2.y = GROUND - 50
        # self.scene_L3.visible = True
        # self.music_start.pause()
        # self.music_L1.loop()

    def reset_game_over(self):
        
        game = Game()
        
    # Method to check if there is a winner in the game
    def check_winning(self):
        if not self.player2.score_added:
            if self.player1.life<=0 or self.player2.reach_gold():
                self.winner=2
                self.player2.score+=1
                self.game_over=True
                self.player2.score_added=True
                return True
        if not self.player1.score_added:
            if self.player2.life<=0 or self.player1.reach_gold():
                self.winner=1
                self.player1.score+=1
                self.game_over=True
                self.player1.score_added=True
                return True
  
    # Method to show music visualizations based on the current playing music
    def show_music(self,num):
        if num==1:
            fft=FFT(self.music_L1.bufferSize(), self.music_L1.sampleRate())
            fft.forward(self.music_L1.left)
        elif num==2:
            fft=FFT(self.music_L2.bufferSize(), self.music_L2.sampleRate())
            fft.forward(self.music_L2.left)
        elif num==3:
            fft=FFT(self.music_L3.bufferSize(), self.music_L3.sampleRate())
            fft.forward(self.music_L3.left)
        elif num==4:
            fft=FFT(self.music_gameover.bufferSize(), self.music_gameover.sampleRate())
            fft.forward(self.music_gameover.left)            
        elif num==0:
            fft=FFT(self.music_start.bufferSize(), self.music_start.sampleRate())
            fft.forward(self.music_start.left)
            
        noStroke()
        
        for i in range(fft.specSize()-470):
            pitch=fft.getBand(i)*5
            fill(255-pitch%255,255-pitch*2%255,255-pitch*3%255)
            rect(i*7+int(SCREEN_W*0.85), SCREEN_H-10,5, -fft.getBand(i)*2)
            
# Scene_L1 class for managing the Level 1 scene
class Scene_L1():
   
    def __init__(self):
        self.visible=False
        self.Bk_btn=Button(int(SCREEN_W*0.2),int(SCREEN_H*0.9),150,60," Back")
        self.Nxt_btn=Button(int(SCREEN_W*0.7),int(SCREEN_H*0.9),150,60," Next")
        self.mine_group=Mine_Group(1,1)
        self.background=loadImage(PATH+"/images/back1.jpg")
        self.platforms = []
        
        # Calculate spacing between platforms
        HORIZONTAL_SPACING = (SCREEN_W - 2 * 200 - NUM_COLUMNS * PLATFORM_WIDTH) / (NUM_COLUMNS - 1)
        VERTICAL_SPACING = (SCREEN_H - 2 * 150 - NUM_ROWS * PLATFORM_HEIGHT) / (NUM_ROWS - 1)
        
        # Generate platforms(level one)
        for row in range(NUM_ROWS):
            for col in range(NUM_COLUMNS):
                x = 200 + col * (PLATFORM_WIDTH + HORIZONTAL_SPACING)
                y = 100 + row * (PLATFORM_HEIGHT + VERTICAL_SPACING)
                # Skip platforms based on row and column conditions
                if row % 2 and col % 2:
                    continue 
                if row % 2 == 1 and col % 2:
                    continue
                else:
                    self.platforms.append(Platform(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT, "platform.png"))
        
    # Method to show the title for Level 1                
    def show_title(self):
        textSize(45)
        text("Game Level 1",int(SCREEN_W/2)-150,SCREEN_H-40)
        
    def display(self):
        self.visible=True
        background(255)
        image(self.background,0,0,SCREEN_W,SCREEN_H)
        fill(210)
        rect(0,SCREEN_H-100,SCREEN_W, 100)
        fill(255)
        textSize(25)
        text("Player1 Score: {}".format(game.player1.score), 20,30)
        text("Player1  Life:   {}".format(game.player1.life),20,60)
        text("Player2 Score: {}".format(game.player2.score), SCREEN_W-220,30)
        text("Player2  Life:   {}".format(game.player2.life),SCREEN_W-220,60)        
        self.Bk_btn.display()
        if not self.Nxt_btn==None:
            self.Nxt_btn.display()
        self.mine_group.update()
       
        for platform in self.platforms:
            platform.display()

            
        game.player1.display()
        game.player2.display() 
        game.gold.display()
        self.show_title()
    
# Scene_L2 class for managing the Level 2 scene, inherits from Scene_L1         
class Scene_L2():
    def __init__(self):
        self.visible=False
        self.Bk_btn=Button(int(SCREEN_W*0.2),int(SCREEN_H*0.9),150,60," Back")
        self.Nxt_btn=Button(int(SCREEN_W*0.7),int(SCREEN_H*0.9),150,60," Next")
        self.mine_group=Mine_Group(1,1)
        self.bat1=Bat(250,430)
        self.bat2=Bat(1000,430)
        self.background=loadImage(PATH+"/images/back2.jpg")
        self.player1_num_bullets = 3
        self.player2_num_bullets = 3
        self.platforms = []
        self.power_ups = []
    
        # Calculate spacing between platforms horizontally and vertically
        HORIZONTAL_SPACING = (SCREEN_W - 2 * 200 - NUM_COLUMNS * PLATFORM_WIDTH) / (NUM_COLUMNS - 1)
        VERTICAL_SPACING = (SCREEN_H - 2 * 150 - NUM_ROWS * PLATFORM_HEIGHT) / (NUM_ROWS - 1)
        
        # Generate platforms and movable platforms for Level 2
        for row in range(NUM_ROWS):
            for col in range(NUM_COLUMNS):
                x = 200 + col * (PLATFORM_WIDTH + HORIZONTAL_SPACING)
                y = 100 + row * (PLATFORM_HEIGHT + VERTICAL_SPACING)  # Using vertical spacing calculation
                if row % 2 == 1 and col % 2: 
                    continue  # Skip generating a movable platform in column 1
                if not row % 2 == 1 and col % 2 == 1: 
                    continue  # Skip generating a platform in column 1
                if row % 2 == 1:
                    self.platforms.append(Movable_Platform(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT, 150, 1250, "platform.png"))
                else:
                    self.platforms.append(Platform(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT, "platform.png"))

        # Generate random power-ups on three platforms
        platforms_with_powerups = random.sample(self.platforms, 10)
        cnt = 1
        for platform in platforms_with_powerups:
            x = (platform.x + platform.w // 2) - 30  # Center x position of the platform
            y = platform.y - 25  # Above the platform
            if cnt % 2:
                self.power_ups.append(Power_ups(x, y, 50, 50, 10 , "heart.png", "L"))
                cnt += 1
            else:
                self.power_ups.append(Power_ups(x, y, 50, 50, 10 , "bp.png", "B"))
                cnt += 1
        
    def generate_powerup(self):        
        platforms_with_powerups = random.sample(self.platforms, 6)
        cnt = 1
        for platform in platforms_with_powerups:
            x = (platform.x + platform.w // 2) - 30  # Center x position of the platform
            y = platform.y - 25  # Above the platform
            if cnt % 2:
                self.power_ups.append(Power_ups(x, y, 50, 50, 10 , "heart.png", "L"))
                cnt += 1
            else:
                self.power_ups.append(Power_ups(x, y, 50, 50, 10 , "bp.png", "B"))
                cnt += 1
            
    def show_title(self):
        textSize(45)
        text("Game Level 2",int(SCREEN_W/2)-150,SCREEN_H-40)       
    
    # Method to handle bullet shots and collisions
    def shot(self):
        if game.player1.hit(game.player2):
            game.player1.y = GROUND - game.player1.r
        if game.player2.hit(game.player1):
            game.player2.y = GROUND - game.player2.r
    
    # Method to display the bullet count for each player
    def show_bullet_count(self):
        fill(255)
        textSize(25)
        text("Player1 Bullets: {}".format(game.player1.num_bullets), 20,90)
        text("Player2 Bullets: {}".format(game.player2.num_bullets), SCREEN_W-220,90)
    
    def display(self):
        self.visible=True
        background(255)
        image(self.background,0,0,SCREEN_W,SCREEN_H)
        fill(210)
        rect(0,SCREEN_H-100,SCREEN_W, 100)
        fill(255)
        textSize(25)
        text("Player1 Score: {}".format(game.player1.score), 20,30)
        text("Player1  Life:   {}".format(game.player1.life),20,60)
        text("Player2 Score: {}".format(game.player2.score), SCREEN_W-220,30)
        text("Player2  Life:   {}".format(game.player2.life),SCREEN_W-220,60)        
        self.Bk_btn.display()
        if not self.Nxt_btn==None:
            self.Nxt_btn.display()
        self.mine_group.update()
       
        for platform in self.platforms:
            platform.display()
        for collectibles in self.power_ups:
            collectibles.display()

        game.player1.display()
        game.player2.display() 
        game.gold.display()
        self.show_title()
    
        self.show_bullet_count()
        self.shot()
        self.bat1.display()
        self.bat2.display()
        
        game.player1.update_bullets()
        game.player1.display_bullets()
        game.player2.update_bullets()
        game.player2.display_bullets()
        
# Scene_L3 class for managing the Level 3 scene, inherits from Scene_L2
class Scene_L3(Scene_L2):
   
    def __init__(self):
        Scene_L2.__init__(self)
        self.Nxt_btn=None
        self.Bk_btn=Button(int(SCREEN_W*0.3),int(SCREEN_H*0.9),150,60," Back")
        self.mine_group=Mine_Group(2,2)
        self.background=loadImage(PATH+"/images/back3.jpg")

    def show_title(self):
        textSize(45)
        text("Game Level 3", int(SCREEN_W/2)-20, SCREEN_H-40)

    def display(self):
        Scene_L2.display(self)

    # Method to handle bullet shots and collisions, including freeze effects in Level 3
    def shot(self):
        if game.player1.hit(game.player2):
            if not game.player1.frozen:  
                game.player1.frozen = True
                game.player1.freeze_timer = 120  
        if game.player2.hit(game.player1):
            if game.player2.frozen:  
                game.player2.frozen = True
                game.player2.freeze_timer = 120  

# Scene_GameOver class for managing the game over scene
class Scene_GameOver:
   
    def __init__(self):
        self.visible=False
        self.Restart_btn=Button(int(SCREEN_W/2 - 60), int(SCREEN_H*0.8), 170,80, "Restart")

        
    def display(self):
        self.visible=True
        background(210)
        self.Restart_btn.display()
        fill(255,0,0)
        textSize(55)
        text("Game Over", int(SCREEN_W/2)-150, int(SCREEN_H/2)-50)
        if game.winner==1:
            textSize(40)
            text("Player 1 Won!  Congratulations!", int(SCREEN_W/2)-300, int(SCREEN_H/2)+20)
        elif game.winner==2:
            textSize(40)
            text("Player 2 Won!  Congratulations!", int(SCREEN_W/2)-300, int(SCREEN_H/2)+20)  

# Start_Select class for managing the start and level selection screen
class Start_Select:
  
    def __init__(self):
        self.L1_btn=Button(SCREEN_W/2-100,SCREEN_H/2-150,200,100,"Level 1")
        self.L2_btn=Button(SCREEN_W/2-100,SCREEN_H/2,200,100,"Level 2")
        self.L3_btn=Button(SCREEN_W/2-100,SCREEN_H/2+150,200,100,"Level 3")
        self.background=loadImage(PATH+"/images/back0.jpg")


    def display(self):
        image(self.background,0,0,SCREEN_W,SCREEN_H)
        fill(255)
        textSize(60)
        text("Skyward Seeker",SCREEN_W/2-200,int(SCREEN_H*0.1))
        self.L1_btn.display()
        self.L2_btn.display()
        self.L3_btn.display()

# Scene_Level_Instruction class for managing level instruction scenes
class Scene_Level_Instruction:
    
    def __init__(self,level):
        self.visible=False
        self.Bk_btn=Button(int(SCREEN_W*0.2),int(SCREEN_H*0.85),150,60," Back")
        self.Start_btn=Button(int(SCREEN_W*0.7),int(SCREEN_H*0.85),150,60," Start")
        self.img=loadImage(PATH+"/images/L{}_Instructions.png".format(level))

    def display(self):
        if self.visible==True:
            background(210)
            image(self.img,0,0,SCREEN_W, SCREEN_H)
            self.Bk_btn.display()
            self.Start_btn.display()

# Setup function for setting up the Processing environment
def setup():
    size(SCREEN_W, SCREEN_H)

# Draw function for continuously updating the game state and rendering
def draw():
    game.run()
    game.check_winning()
    
# keyPressed function for handling key press events        
def keyPressed():
    # Movement keys for Player 2
    if keyCode == LEFT:
        game.player2.key_handler[LEFT] = True
    elif keyCode == RIGHT:
        game.player2.key_handler[RIGHT] = True  
    elif keyCode == UP:
        game.player2.key_handler[UP] = True
    # Shooting key for Player 2
    elif keyCode == DOWN:
        # Check if the shoot key is not already pressed down
        if not game.player2.key_handler[DOWN]:
            game.player2.key_handler[DOWN] = True
            # Trigger the shoot action
            game.player2.shoot()

    # Movement keys for Player 1    
    elif key == 'w' or key == 'W' :
        game.player1.key_handler['w'] = True
    elif key == 'a' or key == 'A':
        game.player1.key_handler['a'] = True
    elif key == 'd' or key == 'D':
        game.player1.key_handler['d'] = True
    # Shooting key for Player 1
    elif key == 's' or key == 'S':
        # Check if the shoot key is not already pressed down
        if not game.player1.key_handler['s']:
            game.player1.key_handler['s'] = True
            # Trigger the shoot action
            game.player1.shoot()

# keyReleased function for handling key release events
def keyReleased():
    # Release movement keys for Player 2
    if keyCode == LEFT:
        game.player2.key_handler[LEFT] = False
    elif keyCode == RIGHT:
        game.player2.key_handler[RIGHT] = False  
    elif keyCode == UP:
        game.player2.key_handler[UP] = False
    # Release shooting key for Player 2
    elif keyCode == DOWN:
        game.player2.key_handler[DOWN] = False

    # Release movement keys for Player 1
    elif key == 'w' or key == 'W' :
        game.player1.key_handler['w'] = False
    elif key == 'a' or key == 'A':
        game.player1.key_handler['a'] = False
    elif key == 'd' or key == 'D':
        game.player1.key_handler['d'] = False
    # Shooting key for Player 1
    elif key == 's' or key == 'S':
        game.player1.key_handler['s'] = False

# mouseClicked function for handling mouse click events
def mouseClicked():
    if game.start:
        if not game.music_start.isPlaying():
            game.music_start.loop()
        if game.StartandSelect.L1_btn.x<=mouseX<=game.StartandSelect.L1_btn.x+game.StartandSelect.L1_btn.w and game.StartandSelect.L1_btn.y<=mouseY<=game.StartandSelect.L1_btn.y+game.StartandSelect.L1_btn.h:
            game.start=False
            game.scene_L1_instruction.visible=True
        elif game.StartandSelect.L2_btn.x<=mouseX<=game.StartandSelect.L2_btn.x+game.StartandSelect.L2_btn.w and game.StartandSelect.L2_btn.y<=mouseY<=game.StartandSelect.L2_btn.y+game.StartandSelect.L2_btn.h:
            game.start=False
            game.scene_L2_instruction.visible=True
        elif game.StartandSelect.L3_btn.x<=mouseX<=game.StartandSelect.L3_btn.x+game.StartandSelect.L3_btn.w and game.StartandSelect.L3_btn.y<=mouseY<=game.StartandSelect.L3_btn.y+game.StartandSelect.L3_btn.h:
            game.start=False
            game.scene_L3_instruction.visible=True
    elif game.scene_L1_instruction.visible:
        if game.scene_L1_instruction.Bk_btn.x<=mouseX<=game.scene_L1_instruction.Bk_btn.x+game.scene_L1_instruction.Bk_btn.w and game.scene_L1_instruction.Bk_btn.y<=mouseY<=game.scene_L1_instruction.Bk_btn.y+game.scene_L1_instruction.Bk_btn.h:
            game.scene_L1_instruction.visible=False
            game.start=True
        elif game.scene_L1_instruction.Start_btn.x<=mouseX<=game.scene_L1_instruction.Start_btn.x+game.scene_L1_instruction.Start_btn.w and game.scene_L1_instruction.Start_btn.y<=mouseY<=game.scene_L1_instruction.Start_btn.y+game.scene_L1_instruction.Start_btn.h:
            game.scene_L1_instruction.visible=False
            game.player1.life=3
            game.player1.num_bullets=3
            game.player2.life=3
            game.player2.num_bullets=3
            game.player1.x=50
            game.player1.y=GROUND-50
            game.player2.x=SCREEN_W-50
            game.player2.y=GROUND-50
            game.scene_L1.visible=True
            game.music_start.pause()
            game.music_L1.loop()
    elif game.scene_L2_instruction.visible:
        if game.scene_L2_instruction.Bk_btn.x<=mouseX<=game.scene_L2_instruction.Bk_btn.x+game.scene_L2_instruction.Bk_btn.w and game.scene_L2_instruction.Bk_btn.y<=mouseY<=game.scene_L2_instruction.Bk_btn.y+game.scene_L2_instruction.Bk_btn.h:
            game.reset_level2()
            game.scene_L2_instruction.visible=False
            game.start=True
        elif game.scene_L2_instruction.Start_btn.x<=mouseX<=game.scene_L2_instruction.Start_btn.x+game.scene_L2_instruction.Start_btn.w and game.scene_L2_instruction.Start_btn.y<=mouseY<=game.scene_L2_instruction.Start_btn.y+game.scene_L2_instruction.Start_btn.h:
            game.scene_L2_instruction.visible=False
            game.scene_L2.visible=True
            game.player1.life=3
            game.player1.num_bullets=3
            game.player2.life=3
            game.player2.num_bullets=3
            game.player1.x=50
            game.player1.y=GROUND-50
            game.player2.x=SCREEN_W-50
            game.player2.y=GROUND-50
            game.music_start.pause()
            game.music_L2.loop()
    elif game.scene_L3_instruction.visible:
        if game.scene_L3_instruction.Bk_btn.x<=mouseX<=game.scene_L3_instruction.Bk_btn.x+game.scene_L3_instruction.Bk_btn.w and game.scene_L3_instruction.Bk_btn.y<=mouseY<=game.scene_L3_instruction.Bk_btn.y+game.scene_L3_instruction.Bk_btn.h:
            game.reset_level3()
            game.scene_L3_instruction.visible=False
            game.start=True
        elif game.scene_L3_instruction.Start_btn.x<=mouseX<=game.scene_L3_instruction.Start_btn.x+game.scene_L3_instruction.Start_btn.w and game.scene_L3_instruction.Start_btn.y<=mouseY<=game.scene_L3_instruction.Start_btn.y+game.scene_L3_instruction.Start_btn.h:
            game.scene_L3_instruction.visible=False
            game.scene_L3.visible=True
            game.player1.life=3
            game.player1.num_bullets=3
            game.player2.life=3
            game.player2.num_bullets=3
            game.player1.x=50
            game.player1.y=GROUND-50
            game.player2.x=SCREEN_W-50
            game.player2.y=GROUND-50
            game.music_start.pause()
            game.music_L3.loop()

    
    elif game.scene_L1.visible:
        game.player1=Player1(50, GROUND-50, 10)
        game.player2=Player2(1350, GROUND-50, 10)
        game.music_start.pause()
        game.music_L1.loop()
        game.scene_L1.display()
        if game.scene_L1.Bk_btn.x<=mouseX<=game.scene_L1.Bk_btn.x+game.scene_L1.Bk_btn.w and game.scene_L1.Bk_btn.y<=mouseY<=game.scene_L1.Bk_btn.y+game.scene_L1.Bk_btn.h:
            game.scene_L1.visible=False
            game.player1.life=3
            game.player1.score=0
            game.player2.life=3
            game.player2.score=0
            game.start=True
            game.music_L1.pause()
            game.music_start.loop()
        elif game.scene_L1.Nxt_btn.x<=mouseX<=game.scene_L1.Nxt_btn.x+game.scene_L1.Nxt_btn.w and game.scene_L1.Nxt_btn.y<=mouseY<=game.scene_L1.Nxt_btn.y+game.scene_L1.Nxt_btn.h:
            game.scene_L1.visible=False
            game.player1.life=3
            game.player1.score=0
            game.player2.life=3
            game.player2.score=0
            game.scene_L2.visible=True
            game.music_L1.pause()
            game.music_L2.loop()
    
    elif game.scene_L2.visible:
        game.player1=Player1(50, GROUND-50, 10)
        game.player2=Player2(1350, GROUND-50, 10)
        game.scene_L2.display()
        if game.scene_L2.Bk_btn.x<=mouseX<=game.scene_L2.Bk_btn.x+game.scene_L2.Bk_btn.w and game.scene_L2.Bk_btn.y<=mouseY<=game.scene_L2.Bk_btn.y+game.scene_L2.Bk_btn.h:
            game.scene_L2.visible=False
            game.player1.life=3
            game.player1.score=0
            game.player2.life=3
            game.player2.score=0
            game.player1.num_bullets=3
            game.player2.num_bullets=3
            game.start=True
            game.music_L2.pause()
            game.music_start.loop()

        elif game.scene_L2.Nxt_btn.x<=mouseX<=game.scene_L2.Nxt_btn.x+game.scene_L2.Nxt_btn.w and game.scene_L2.Nxt_btn.y<=mouseY<=game.scene_L2.Nxt_btn.y+game.scene_L2.Nxt_btn.h:
            game.scene_L2.visible=False
            game.player1.life=3
            game.player1.score=0
            game.player2.life=3
            game.player2.score=0
            game.player1.num_bullets=3
            game.player2.num_bullets=3
            game.scene_L3.visible=True
            game.music_L2.pause()
            game.music_L3.loop()

    elif game.scene_L3.visible:
        game.player1=Player1(50, GROUND-50, 10)
        game.player2=Player2(1350, GROUND-50, 10)
        game.scene_L3.display()
        if game.scene_L3.Bk_btn.x<=mouseX<=game.scene_L3.Bk_btn.x+game.scene_L3.Bk_btn.w and game.scene_L3.Bk_btn.y<=mouseY<=game.scene_L3.Bk_btn.y+game.scene_L3.Bk_btn.h:
            game.scene_L3.visible=False
            game.player1.life=3
            game.player1.score=0
            game.player2.life=3
            game.player2.score=0
            game.player1.num_bullets=3
            game.player2.num_bullets=3
            game.start=True
            game.music_L3.pause()
            game.music_start.loop()
            
    elif game.scene_gameover.visible:
        if game.scene_gameover.Restart_btn.x<=mouseX<=game.scene_gameover.Restart_btn.x+game.scene_gameover.Restart_btn.w and game.scene_gameover.Restart_btn.y<=mouseY<=game.scene_gameover.Restart_btn.y+game.scene_gameover.Restart_btn.h:
            # game.reset_game_over()
            game.scene_gameover.visible=False
            game.player1.life=3
            game.player1.num_bullets=3
            game.player2.life=3
            game.player2.num_bullets=3
            game.player1.score_added=False
            game.player2.score_added=False
            game.player1.x=50
            game.player1.y=GROUND-50
            game.player2.x=SCREEN_W-50
            game.player2.y=GROUND-50
            game.gameover=False
            game.music_L1.pause()
            game.music_L2.pause()
            game.music_L3.pause()
            game.music_gameover.pause()
            game.music_start.loop()
            game.start=True

    
     
# Running the game
game = Game()