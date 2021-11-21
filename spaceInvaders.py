# -*- coding: utf-8 -*-
# Sefa the g4
# Space Invaders

import turtle
import math
import random
import platform

# If on Windows, you should import winsound
if platform.system() == "Windows":
    try:
        import winsound
    except:
        print("Winsound module not available.")

# Set up the SCREEN

sc = turtle.Screen()
sc.title("Space Invaders")
sc.bgcolor("#078219")
sc.bgpic("space_invaders_background.gif")
sc.tracer(0)

# Register the shapes

turtle.register_shape("invader.gif")
turtle.register_shape("player.gif")

# Draw BORDERS

border_pen = turtle.Turtle()
border_pen.speed(0)
border_pen.color("white")
border_pen.penup()
border_pen.setposition(-300,-300)
border_pen.pendown()
border_pen.pensize(3)
for side in range(4): #4 4 kenar için
    border_pen.fd(600) # forward
    border_pen.lt(90) # left
border_pen.hideturtle()

# Set the score to 0
score = 0

# Draw the score
score_pen = turtle.Turtle()
score_pen.speed(0)
score_pen.color("white")
score_pen.penup()
score_pen.setposition(-290,280)
scorestring = "Score: {}".format(score)
score_pen.write(scorestring, False, align="left", font=("Arial",14,"normal"))
score_pen.hideturtle()

# Create the PLAYER turtle

player = turtle.Turtle()
player.color("blue")
player.shape("player.gif")
player.penup()
player.speed(0)
player.setposition(0,-250)
player.setheading(90) # üçgeni 90* çevirir
playerspeed = 25

# Choose a number of enemies 
number_of_enemies = 7
# Create an empty list of enemies
enemies = []
# Add enemies to the list
for i in range(number_of_enemies):
    #Create the enemy
    enemies.append(turtle.Turtle())
for enemy in enemies:
    enemy.color("red")
    enemy.shape("invader.gif")
    enemy.penup()
    enemy.speed(0)
    x = random.randint(-200,200)
    y = random.randint(100,250)
    enemy.setposition(x,y)
enemyspeed = 0.2

# Create the player's bullet

bullet = turtle.Turtle()
bullet.color("yellow")
bullet.shape("triangle")
bullet.penup()
bullet.speed(0)
bullet.setheading(90)
bullet.shapesize(0.5,0.5)
bullet.hideturtle()

bulletspeed = 2

# Define bullet state
# ready- ready to fire
# fire - bullet is firing
bulletstate = "ready"

# Move the player left and right

def move_left():
    player.speed = -15
    x = player.xcor() # x koordinatı
    x -= playerspeed
    if x < -280:
        x = -280
    player.setx(x)

def move_right():
    player.speed = 15
    x = player.xcor()
    x += playerspeed
    if x > 280:
        x = 280
    player.setx(x)

# def move_player():
#     player.speed = -15
#     x = player.xcor()
#     x -= player.speed
#     if x < -280:
#         x = -280
#     if x > 280:
#         x = 280    
#     player.setx(x)
       

def fire_bullet():
    # Declare bulletstate as a global if it needs changed
    global bulletstate
    if bulletstate == "ready":
        play_sound("laser.wav")
        bulletstate = "fire"
        # Move the bullet to the just above the player
        x = player.xcor()
        y = player.ycor() +10
        bullet.setposition(x,y)
        bullet.showturtle()
    
def isCollision(t1,t2):
    distance = math.sqrt(math.pow(t1.xcor()-t2.xcor(),2)+math.pow(t1.ycor()-t2.ycor(),2))
    if distance < 20:
        return True
    else:
        return False
       
def play_sound(sound_file,time=0):
    # Windows
    if platform.system == "Windows":
        winsound.PlaySound(sound_file,winsound.SND_ASYNC)

# Create keybord bindings

turtle.listen()
turtle.onkey(move_left, "Left")
turtle.onkey(move_right, "Right")
turtle.onkey(fire_bullet, "space")

# Main Game Loop
while True:
    sc.update()

    for enemy in enemies:
        # Move the enemy
        x = enemy.xcor()
        x += enemyspeed
        enemy.setx(x)
        
        # Move the enemy back and down
        if enemy.xcor() > 280:
            # Move all enemies down
            for e in enemies:
                y = e.ycor()
                y -= 40
                e.sety(y)
            # Change enemy direction
            enemyspeed *= - 1

        if enemy.xcor() < -280:
            # Move all enemies down
            for e in enemies:
                y = e.ycor()
                y -= 40
                e.sety(y)
            # Change enemy direction
            enemyspeed *= - 1
        
        # Check for a collision between the bullet and the enemy
        if isCollision(bullet,enemy):
            play_sound("explosion.wav")
            # Reset the bullet
            bullet.hideturtle()
            bulletstate = "ready"
            bullet.setposition(0,-400)
            # Reset the enemy
            x = random.randint(-200,200)
            y = random.randint(100,250)
            enemy.setposition(x,y)
            # Update Score
            score += 10
            scorestring = "Score: {}".format(score)
            score_pen.clear()
            score_pen.write(scorestring, False, align="left", font=("Arial",14,"normal"))
            
        if isCollision(player,enemy):
            play_sound("explosion.wav")
            player.hideturtle()
            for enemy in enemies:
                enemy.hideturtle()
            bullet.hideturtle()
            print("GAME OVER") 
            # GAME OVER
            game_over = turtle.Turtle()
            game_over.speed(0)
            game_over.color("white")
            game_over.penup()
            game_over.setposition(0,0)
            game_over.write("GAME OVER", False, align="center", font=("Arial",30,"normal"))
            game_over.hideturtle()
            # Write total score
            total_score = turtle.Turtle()
            total_score.speed(0)
            total_score.color("white")
            total_score.penup()
            total_score.setposition(0,-40)
            total_score.write(scorestring, False, align="center", font=("Arial",25,"normal"))
            total_score.hideturtle()
            break

    # Move the bullet
    if bulletstate == "fire":
        y = bullet.ycor()
        y += bulletspeed
        bullet.sety(y)
    # Check to see if the bullet has gone to the top
    if bullet.ycor() > 275:
        bullet.hideturtle()
        bulletstate = "ready"


