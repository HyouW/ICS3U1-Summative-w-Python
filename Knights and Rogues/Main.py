"""
Neville Tsang, Huanyou Wei
May 17, 2017
ICS3U1-03, Mr. Cope
Knights and Rogues.py
A pygame game that includes a menu, a board game, instructions and highscores.
Uses tuples, lists, dictionaries and csv files

input: Mouse clicks
       Mouse hovering
       Arrow keys
output: Screen changes
        Buttons light up
        Player movement
"""
#import pygame, sys, random, and math modules
import pygame
from pygame.locals import *
import sys
import random
from math import *

#initialize pygame.mixer and pygame
pygame.mixer.init()
pygame.init()
#create a global clock with the pygame module to control iterations/frame per second
clock = pygame.time.Clock()#create a clock object to keep time

def text(font, str, colour):#create a function that renders a string with the font, string, and colour as parameters
    display = font.render(str, True, colour)#assign the rendered text to a variable called display
    return display#return display

def game_menu():#define the game menu function
    size = (800,640)#set size: 800 is length, 640 is height
    gameDisplay = pygame.display.set_mode(size)#make a screen with the size
    menu_pic = pygame.image.load('images/CastleMenuPicture.png').convert()#Load menu background image from the images folder

    title_font = pygame.font.Font("fonts/blackwood-castle.regular.ttf", 80)#load the title font with the ttf file in the fonts folder
    button_font = pygame.font.Font("fonts/blackwood-castle.regular.ttf", 60)#load the button font

    #set rgb values to their corresponding colour
    grey = (150,150,150)
    gold = (218,165,32)
    yellow = (255,255,0)

    title = text(title_font, 'Knights and Rogues', gold)#create a title text
    title_rect = title.get_rect()#get the rect of the title
    title_rect.center = (size[0]//2, size[1]//4)#set the center of the rect to the middle top of the screen

    play = text(title_font, 'Play', grey)#create a play button text
    play_rect = play.get_rect()#get the rect of the play button
    play_rect.center = (size[0]//2, size[1]//2)#set the center of the rect to the middle of the screen

    how_to_play = text(button_font, 'How to Play', grey)#create a how to play button text
    how_to_play_rect = how_to_play.get_rect()#get the rect of the how to play button
    how_to_play_rect.center = (size[0]//2, (size[1]//2)*1.25)#set the center of the rect under the play button

    high_score_rect = how_to_play.get_rect() # use how_to_play.get_rect() since the high_score.get_rect() is not centered
    high_score_rect.center = (size[0]//2, (size[1]//2)*1.5)#set the center of the rect under the how to play button

    quit_rect = play.get_rect() # use play.get_rect() since the quit.get_rect is not centered()
    quit_rect.center = (size[0]//2, (size[1]//2)*1.75)#set the center of the rect under the high score button

    pygame.mixer.music.load("sound/MenuMusic.ogg")#load the menu music file
    pygame.mixer.music.set_volume(0.4)#set the volume to 0.4
    pygame.mixer.music.play(-1)#play the music infinitely

    menu = True#set a flag called menu to true

    while menu:#while the menu flag is true

        clock.tick(15)#the clock counts 15 times per second (fps)
        for event in pygame.event.get():#for event in the pygame event list
            if event.type == QUIT:#if the event type is QUIT:
                menu = False#set the menu flag to false
                pygame.mixer.quit()#quit the pygame mixer
            elif event.type == MOUSEBUTTONDOWN:#if the event type is mouse button down (mouseclick):
                if play_rect.collidepoint(event.pos):#see if the mouse cursor is colliding with the play button
                    pygame.mixer.music.stop()#stop the music
                    board_event_loop(gameDisplay)#if it is, call the game_event_loop() function and give it gameDisplay
                    pygame.mixer.music.load("sound/MenuMusic.ogg") #if the game loop ends, play the menu music again
                    pygame.mixer.music.set_volume(0.4)#set the volume to 0.4
                    pygame.mixer.music.play(-1)#play the music infinitely
                elif how_to_play_rect.collidepoint(event.pos):#if the mouse clicks down on the how to play button
                    pygame.mixer.music.stop()#stop the music
                    how_to_play_display(gameDisplay)#call the how to play loop and give it gameDisplay
                    pygame.mixer.music.play(-1)#when the how to play loop is done, play the music again
                elif high_score_rect.collidepoint(event.pos):#if the mouse clicks on the highscore button
                    highscore_display(gameDisplay)#call the highscore loop and give it gameDisplay
                elif quit_rect.collidepoint(event.pos):#if the mouse clicks on the quit button
                    menu = False#set menu to false, ending the menu loop
                    pygame.mixer.quit()#quit the pygame mixer

        mouse_pos = pygame.mouse.get_pos()#set the mouse position to mouse_pos

        if play_rect.collidepoint(mouse_pos):#if the mouse cursor is colliding with the play button (and it's not a mouse click)
            play = text(button_font, 'Play', yellow)#change the colour of the text to yellow
        else:
            play = text(button_font, 'Play', grey)#otherwise, the playbutton is grey

        if how_to_play_rect.collidepoint(mouse_pos):#if the mouse collides with the how to play button, light it up (by changing colour)
            how_to_play = text(button_font, 'Instructions', yellow)
        else:#otherwise, it stays unlit (by changing colour to default)
            how_to_play = text(button_font, 'Instructions', grey)

        if high_score_rect.collidepoint(mouse_pos):#if the mouse hovers over the highscore button, light it up (by changing colour)
            high_score = text(button_font, 'High Scores', yellow)
        else:#otherwise, it stays unlit (by changing colour to default)
            high_score = text(button_font, 'High Scores', grey)

        if quit_rect.collidepoint(mouse_pos):##if the mouse collides with the quit button, light it up (by changing colour)
            quit = text(button_font, 'Quit', yellow)
        else:#otherwise, it stays grey
            quit = text(button_font, 'Quit', grey)

        gameDisplay.blit(menu_pic, (0,0))#blit the background image onto the screen at (0,0)
        gameDisplay.blit(title, title_rect)#blit the title at the title_rect
        gameDisplay.blit(play, play_rect)#blit the playbutton image onto the screen at the play button's rect
        gameDisplay.blit(how_to_play, how_to_play_rect)#blit the how to play button at its rect
        gameDisplay.blit(high_score, high_score_rect)#blit the highscore button at its rect
        gameDisplay.blit(quit, quit_rect)#blit the quit button at its rect
        pygame.display.update()#update the screen

def board_event_loop(gameDisplay):#define the board_event_loop function
    bigmap = pygame.image.load('images/template.png').convert()#from the images folder, load the board game template

    ###Player 1
    player1 = pygame.sprite.Sprite()#create a sprite object named player1
    player1.image = pygame.image.load('images/Knight.png').convert_alpha()#give the knight image to the player1 sprite object
    player1.rect = pygame.Rect((80, 1360), player1.image.get_size())#give the player1 object the player1 rect
    player1.dy = 0#give player1 a delta y value of 0
    player1.dx = 0#give player1 a delta x value of 0
    player1.launched = False#flag to see if player1 is shot by the cannon
    player1.falling = False#flag to see if player1 is falling (from pitfall)
    player1.room_number = 0#player1's room number, used to determine position on board
    player1.room_index = 0#player1's room index, used to determine if player1 needs to go back (number exceeds 100)
    player1.been_there = False#player1's flag to determine if it was at 100
    player1.turn_count = 0#player1's turn count
    player1.flip = False#flag to see if player1 needs to be flipped

    ###Player 2
    player2 = pygame.sprite.Sprite()#create a sprite object named player2
    player2.image = pygame.image.load('images/Rogue.png').convert_alpha()#give the rogue image to the player2 sprite object
    player2.rect = pygame.Rect((120, 1360), player2.image.get_size())#give the player2 object the player1 rect
    player2.dy = 0#player2's delta y value
    player2.dx = 0#player2's delta x value
    player2.launched = False#flag to see if player2 was launched
    player2.falling = False#flag to see if player2 fell in a pitfall
    player2.room_number = 0#player2's room number, determines position in castle
    player2.room_index = 0#player2's room index, used to determine if player2 needs to go back (number exceeds 100)
    player2.been_there = False#player2's flag to determine if it was at 100
    player2.turn_count = 0#turn count for player2
    player2.flip = False#flag to see if player2 needs to be flipped

    size = (800, 640)#the size of the screen
    half_width = int(size[0]/2)#half the width of the screen
    half_height = int(size[1]/2)#half the height of the screen

    rooms = []#initialize room list to hold room rects
    up = []#initialize up list to hold rooms at the very side where the user moves up to go to the next floor

    room_image_list = []#create a room image list to have a variety of room images
    for n in range(1, 5):#in the range 1 to 5, iterate and append the room corresponding to the number into the image list
        room_image_list.append(pygame.image.load('images/Room{0:d}.png'.format(n)).convert())
    room_size = room_image_list[0].get_size()#get the size of one room

    rooms.append(Rect((80, 1360), room_size))#append the rect of the first room into the room list, right and bottom determined by room size

    #get the rects for the first block of the castle (10 x 5)
    for y in range(1360, 960, -80):#use y to iterate from 1360 to 860, with steps of -80
        if y % 160 == 0:#if y is divisible by 160, loop from 880 to 80 with steps of -80 (floor will go from right to left)
            for x in range(880, 80, -80):
                rooms.append(Rect((x, y), room_size))#create a rect with x, y and the room size, append it into the room list
        else:#if y is not divisible by 160, loop from 160 to 960, with steps of 80 (floor goes from left to right)
            for x in range(160, 960, 80):
                rooms.append(Rect((x, y), room_size))#create a rect with x, y and the room size, append it into the room list
        up.append(Rect((x, y), room_size))#append the rooms at the side into up list

    #get the rects for the second block of the castle (7 x 4)
    for y in range(960, 640, -80):#use y to iterate from 960 to 640, with steps of -80
        if y % 160 == 0:#if y is loop backwards with steps of -80 (floor will go from right to left)
            for x in range(760, 200, -80):
                rooms.append(Rect((x, y), room_size))#create a rect with x, y and the room size, append it into the room list
        else:#if y is not divisible by 160, loop forwards with steps of 80 (floor goes from left to right)
            for x in range(280, 840, 80):
                rooms.append(Rect((x, y), room_size))#create a rect with x, y and the room size, append it into the room list
        up.append(Rect((x, y), room_size))

    #get the rects for the third block of the castle (5 x 3)
    for y in range(640, 400, -80):
        if y % 160 == 0:#if y is loop backwards with steps of -80 (floor will go from right to left)
            for x in range(680, 280, -80):#if y is loop backwards with steps of -80 (floor will go from right to left)
                rooms.append(Rect((x, y), room_size))#create a rect with x, y and the room size, append it into the room list
        else:#if y is not divisible by 160, loop forwards with steps of 80 (floor goes from left to right)
            for x in range(360, 760, 80):
                rooms.append(Rect((x, y), room_size))#create a rect with x, y and the room size, append it into the room list
        up.append(Rect((x, y), room_size))

    #get the rects for the fifth block of the castle (3 x 2)
    for y in range(400, 240, -80):
        if y % 160 == 0:#if y is loop backwards with steps of -80 (floor will go from right to left)
            for x in range(600, 360, -80):#if y is loop backwards with steps of -80 (floor will go from right to left)
                rooms.append(Rect((x, y), room_size))#create a rect with x, y and the room size, append it into the room list
        else:
            for x in range(440, 680, 80):#if y is not divisible by 160, loop forwards with steps of 80 (floor goes from left to right)
                rooms.append(Rect((x, y), room_size))#create a rect with x, y and the room size, append it into the room list
        up.append(Rect((x, y), room_size))

    hundredth_room = Rect(((1120/2-40), 240), room_size)#create a rect for the 100th room
    #append it into the rooms and up list
    rooms.append(hundredth_room)
    up.append(hundredth_room)

    #create a random room list by copying the room list, will randomize rooms to provide variety
    random_rooms = rooms.copy()
    #shuffle the random room list
    random.shuffle(random_rooms)

    camera_state = Rect(0, 800, 1120, 1440)#create a camera rect, will be used to scrolls creen

    dice_dict = {}#create dice_dict to hold the dice pictures
    for n in range(1, 7):#iterate from 1 to 7 and append the corresponding dice images into the dice dict
        dice_dict[n] = pygame.image.load('images/D{0:d}.png'.format(n)).convert_alpha()#convert_alpha() to maintain transparency values
    dice_rect = Rect((32,100), (dice_dict[1].get_size()))#create a dice rect for all the dice pictures
    index = 1#set the dice index to 1
    frame_count = 0#set the frame_count to 0, used for pitfall

    switch = pygame.image.load('images/switch.png').convert_alpha()#load the switch image (non lit) and convert transparency values
    switchLit = pygame.image.load('images/switchLit.png').convert_alpha()#load the lit switch image, convert transparency values
    switch_rect = Rect((702,100), (switch.get_size()))#set the switch rect

    cannon_image = pygame.image.load('images/cannon.png').convert_alpha()#load the cannon image
    pitfall_image = pygame.image.load('images/pitfall.png').convert_alpha()#load the pitfall image

    cannon_list = [12, 24, 34, 40, 51, 71, 79, 92]#create a cannon list to determine the location of the cannons
    pitfall_list = [19, 28, 44, 59, 81, 96]#create a pitfall list to determine to pitfall locations
    #create a cannon and pitfall dict to see if the room the player is in contains either a cannon or a pitfall
    cannons = {}
    pitfalls = {}
    for x in range(0, 101):#with x, iterate from 1 to 100
        if x in cannon_list:#if x is in the cannon list set the corresponding value to True, 90 and the cannon image
            cannons[x] = [True, 90, cannon_image]
        else:#otherwise, set the value to false and the angle to 0 (necessary for list indices)
            cannons[x] = [False, 0]
        if x in pitfall_list:#if x is in the pitfall list set the corresponding value to True
            pitfalls[x] = True
        else:#otherwise, set the value to False
            pitfalls[x] = False

    #create a left and right list that has the room numbers of the rooms at the outer edge (prevents player from flying out)
    left_list = [1, 20, 21, 40, 41, 57, 58, 71, 72, 83, 84, 93, 94, 99, 100]
    right_list = [10, 11, 30, 31, 50, 51, 64, 65, 78, 79, 88, 89, 96, 97, 100]

    #iterate from 0 to the length of the left list (length is same as right list)
    #set the element of that index to the value of the element in rooms list (ie. left_list[2] = rooms[21])
    for n in range(0, len(left_list)):
        left_list[n] = rooms[left_list[n]]
        right_list[n] = rooms[right_list[n]]

    #create a top list containing the numbers of the rooms at the top (prevents player from flying out)
    top_list = [41, 50, 72, 78, 89, 93, 97, 99, 100]

    #iterate from 0 to the length of the top list
    #set the element of that index to the value of the element in rooms list
    for t in range(0, len(top_list)):
        top_list[t] = rooms[top_list[t]]

    #a flag to see if the player has clicked on the dice, set to true to allow clicking
    click = True

    #set the default player_turn to 1 so player1 goes first
    player_turn = 1
    #set the player_rect to player1.rect, used for player view
    player_rect = player1.rect

    #create a font using the blackwood castle font with a size of 40
    my_font = pygame.font.Font("fonts/blackwood-castle.regular.ttf", 40)

    #assign rgb values to their corresponding colour
    red = (255,0,0)
    gold = (218,165,32)
    blue = (0,0,255)
    yellow = (255,255,0)

    #make a turn text displaying 'Player 1 Turn' in red with the font (call text function), signifying player turn
    turn = text(my_font, 'Player 1 Turn', red)
    #make a turn text displaying 'Player 1 View' in red, determining player view
    view = text(my_font, 'Player 1 View', red)
    #make a roll again text in gold, telling the player to roll again
    roll_again = text(my_font, 'You got 6, Roll again', gold)

    #a flag to see if the player has rolled a 6
    six = False

    #create a gold menu button, get its rect and set the center to the middle top of the screen
    menu = text(my_font, 'Menu', gold)
    menu_rect = menu.get_rect()
    menu_rect.center = (size[0]//2, size[1]//16)

    #load the board game music, set vol to 0.4 and play infinitely
    pygame.mixer.music.load("sound/BoardGameMusic.ogg")
    pygame.mixer.music.set_volume(0.4)
    pygame.mixer.music.play(-1)

    #load the boom sound for when the cannon fires
    boom = pygame.mixer.Sound(file="sound/boom.ogg")
    #load the falling sound for when the player hits the ground
    falling_sound = pygame.mixer.Sound(file="sound/FallingSound.ogg")
    #load the roll six sound for when the player rolls a six
    roll_six = pygame.mixer.Sound(file="sound/RollSix.ogg")

    #a flag that keeps the while loop going
    board = True

    while board:#while board is true
        dt = clock.tick(60)#set the framerate to 60 and assign the time, in milliseconds, to dt or delta time

        for event in pygame.event.get():#for event in the pygame event list
            if event.type == QUIT:#if the event type is QUIT
                pygame.mixer.quit()#quit the pygame mixer
                pygame.quit();sys.exit()#quit pygame and the module
            elif event.type == MOUSEBUTTONDOWN:#if the event type is MOUSEBUTTONDOWN
                if switch_rect.collidepoint(event.pos):#if the mouse is colliding with the switch view rect
                    if player_rect == player1.rect:#if the player_rect is player1, set it to player 2 (switches to player2 view)
                        player_rect = player2.rect
                        view = text(my_font, 'Player 2 View', blue)#change the view text to player2 and blue
                    else:#if it's in player2 view, set the view back to player1
                        player_rect = player1.rect
                        view = text(my_font, 'Player 1 View', red)#change the view text to player1 and red
                elif menu_rect.collidepoint(mouse_pos):#if the mouse is colliding with the menu button rect
                    board = False#set the board flag to False
                    pygame.mixer.music.stop()#stop the music
            elif event.type == MOUSEBUTTONUP:#if the event type is MOUSEBUTTONUP
                if click:#if the click flag is True
                    if dice_rect.collidepoint(event.pos):#if the mouse is colliding with the dice rect
                        if player_turn == 1:#if the player turn is 1, call on the room_counter function and pass it player1 and the index
                            room_counter(player1, index)
                        else:#otherwise, if the player turn is 2, pass room_counter player2 and the index
                            room_counter(player2, index)
                        click = False#set the click flag to False

        mouse_pos = pygame.mouse.get_pos()#create a variable for the mouse position

        #if the mouse is hovering over the switch view rect, change the image
        #if not, keep it the same or change it back
        if switch_rect.collidepoint(mouse_pos):
            switch_image = switchLit
        else:
            switch_image = switch

        #if the mouse is hovering over the menu button, change the color
        #if not, change it back or keep it the same
        if menu_rect.collidepoint(mouse_pos):
            menu = text(my_font, 'Menu',  yellow)
        else:
            menu = text(my_font, 'Menu', gold)

        #if the click flag is True, call the dice_roll function and get the index/dice number
        if click:
            index = dice_roll(index, dice_rect)
            #if index isn't equal to 6, set the six flag to False
            if index != 6:
                six = False

        #if the click flag is False
        else:
            #if the index is equal to 6
            #play the roll six sound
            #set the click and six flags to True
            if index == 6:
                roll_six.play()
                click = True
                six = True
            #if the player1 room number is not in the cannon or pitfall list (prevents you from not firing if landing in one of those rooms)
            #and if the player1 rect bottomleft is equal to the room number bottom left
            #and if the player turn is 1
            #set the player turn to 2, click to True, and add 1 to the player1 turn count
            #change the turn text to player2 and blue
            elif player1.room_number not in cannon_list and player1.room_number not in pitfall_list and player1.rect.bottomleft == rooms[player1.room_number].bottomleft and player_turn == 1:
                player_turn = 2
                click = True
                player1.turn_count += 1
                turn = text(my_font, 'Player 2 Turn', blue)
            #if the player2 room number is not in the cannon or pitfall list (prevents you from not firing if landing in one of those rooms)
            #and if the player2 rect bottomright is equal to the room number bottomright
            #and if the player turn is 2
            #set the player turn to 1, click to True, and increment to the player22 turn count
            #change the turn text to player1 and red
            elif player2.room_number not in cannon_list and player2.room_number not in pitfall_list and player2.rect.bottomright == rooms[player2.room_number].bottomright and player_turn == 2:
                player_turn = 1
                click = True
                player2.turn_count += 1
                turn = text(my_font, 'Player 1 Turn', red)

        #if the player1 rect bottom left is equal to the room 100 bottomleft
        #stop the music
        #call the win_display function and give it the player number, the gameDisplay, the turn count, and player 1 and 2 room numbers
        if player1.rect.bottomleft == rooms[100].bottomleft and player1.room_number == 100:
            pygame.mixer.music.stop()
            board = win_display('1', gameDisplay, board, player1.turn_count, player1.room_number, player2.room_number)
        #otherwise, if the player2 rect bottom right is equal to the room 100 bottom right
        #stop the music
        #call the win_display function and give it the player number, the gameDisplay, the turn count, and player 1 and 2 room numbers
        elif player2.rect.bottomright == rooms[100].bottomright and player2.room_number == 100:
            pygame.mixer.music.stop()
            board = win_display('2', gameDisplay, board, player2.turn_count, player1.room_number, player2.room_number)

        #if the player_turn is equal to 1
        if player_turn == 1:
            #check if the player1 rect is inside a cannon room
            #if it is, set click to False
            #get the key list with pygame.key.get_pressed() to poll key down events
            if cannons[player1.room_number][0] == True and player1.rect.bottomleft == rooms[player1.room_number].bottomleft:
                click = False
                key = pygame.key.get_pressed()

                #if the player presses the left key, rotate the cannon counterclockwise
                if key[K_LEFT]: # rotate conterclockwise
                    cannons = angle_change_counterclockwise(player1, cannons, cannon_image)

                #if the player presses the right key, rotate the cannon clockwise
                if key[K_RIGHT]: # rotate clockwise
                    cannons = angle_change_clockwise(player1, cannons, cannon_image)

                #if the player presses the spacebar, launch the player (launched flag is set to True)
                #play the boom sound
                if key[K_SPACE]:
                    boom.play()
                    t, v0 = launcher(player1, cannons)

            #check if the player is in a pitfall room
            #check if the frame_count is evenly divided by 10 (used to let the player fall, otherwise, the player would stay in the same place)
            #call the dropper function to initialize the time and velocity, and set the falling flag to true
            elif pitfalls[player1.room_number] == True and player1.rect.bottomleft == rooms[player1.room_number].bottomleft:
                if frame_count % 10 == 0:
                    click = False
                    t, v0, bot = dropper(player1, player1, player2, rooms)

            #if the player is launched, call the projectile motion function to launch the player
            #use the player collision function to see if the player is colliding with a wall (prevents player from flying out of the castle)
            #use the room detection function to set the player room number to the new rect
            if player1.launched:
                t, vm, last = projectile_motion(player1, dt, t, v0)
                player_collision(player1, rooms, last, left_list, right_list, top_list, player1, player2)
                room_detection(player1, rooms)

            #if the player is falling, call the gravity function to drop the player
            #use the room detection function to set the player room number to the new rect
            elif player1.falling:
                t, vm = gravity(player1, dt, t, v0, bot, player1, player2, falling_sound)
                room_detection(player1, rooms)

            #otherwise, if the player is not launched or falling
            #call the player_flip function to flip the player1 image
            #determine the up room corresponding to the player (room where player moves to the next floor)
            #call on the player update function to animate the player
            else:
                player_flip(player1, rooms)
                for rect in up:
                    if player1.rect.bottom == rect.bottom:
                        up_room = rect
                player_update(player1, rooms, player1.room_number, up_room, player1.room_index, up_room.left, rooms[player1.room_number].left, player1.rect.left,
                            player1.rect.bottomleft, rooms[player1.room_number].bottomleft, rooms[96].left, rooms[97].left, rooms[99].left, rooms[100].left)

        #otherwise, if the player turn is equal to 2
        else:
            #check if the player2 rect is inside a cannon room
            #if it is, set click to False
            #get the key list with pygame.key.get_pressed() to poll key down events
            if cannons[player2.room_number][0] == True and player2.rect.bottomright == rooms[player2.room_number].bottomright:
                click = False
                key = pygame.key.get_pressed()

                #if the player presses the left key, rotate the cannon counterclockwise
                if key[K_LEFT]: # rotate conterclockwise
                    cannons = angle_change_counterclockwise(player2, cannons, cannon_image)

                #if the player presses the right key, rotate the cannon clockwise
                if key[K_RIGHT]: # rotate clockwise
                    cannons = angle_change_clockwise(player2, cannons, cannon_image)

                #if the player presses the spacebar, launch the player (launched flag is set to True)
                #play the boom sound
                if key[K_SPACE]:
                    boom.play()
                    t, v0 = launcher(player2, cannons)

            #check if the player is in a pitfall room
            #check if the frame_count is evenly divided by 10 (used to let the player fall, otherwise, the player would stay in the same place)
            #call the dropper function to initialize the time and velocity, and set the falling flag to true
            elif pitfalls[player2.room_number] == True and player2.rect.bottomright == rooms[player2.room_number].bottomright:
                if frame_count % 10 == 0:
                    click = False
                    t, v0, bot = dropper(player2, player1, player2, rooms)

            #if the player is launched, call the projectile motion function to launch the player
            #use the player collision function to see if the player is colliding with a wall (prevents player from flying out of the castle)
            #use the room detection function to set the player room number to the new rect
            if player2.launched:
                t, vm, last = projectile_motion(player2, dt, t, v0)
                player_collision(player2, rooms, last, left_list, right_list, top_list, player1, player2)
                room_detection(player2, rooms)

            #if the player is falling, call the gravity function to drop the player
            #use the room detection function to set the player room number to the new rect
            elif player2.falling:
                t, vm = gravity(player2, dt, t, v0, bot, player1, player2, falling_sound)
                room_detection(player2, rooms)

            #otherwise, if the player is not launched or falling
            #call the player_flip function to flip the player2 image
            #determine the up room corresponding to the player (room where player moves to the next floor)
            #call on the player update function to animate the player
            else:
                player_flip(player2, rooms)
                for rect in up:
                    if player2.rect.bottom == rect.bottom:
                        up_room = rect
                player_update(player2, rooms, player2.room_number, up_room, player2.room_index, up_room.right, rooms[player2.room_number].right, player2.rect.right,
                              player2.rect.bottomright, rooms[player2.room_number].bottomright, rooms[96].right, rooms[97].right, rooms[99].right, rooms[100].right)

        #call the camera scroll function to move the camera rect with the player rect
        camera_state = camera_scroll(camera_state, player_rect, half_width, half_height, size[0], size[1])

        #get a subsurface of the background with the camera_state rects to scroll around the background template
        bground = bigmap.subsurface(-(camera_state.left), -(camera_state.top), size[0],size[1]) # take snapshot of bigmap
        #blit the background (subsurface) at (0,0)
        gameDisplay.blit(bground, (0,0))

        #set the counter to 0 to count the elements in the random room list
        counter = 0
        #iterate through the random room list with room_pos
        #if the counter is smaller than 26, then set the room image to Room1 (list was shuffled)
        #if the counter is smaller than 51, then set the image to Room2
        #if the counter is smaller than 76, set the image to Room3
        #if the counter is smaller than 101, set the image to Room4
        #increment the counter by 1
        for room_pos in random_rooms:
            if counter < 26:
                gameDisplay.blit(room_image_list[0], apply(camera_state, room_pos))
            elif counter < 51:
                gameDisplay.blit(room_image_list[1], apply(camera_state, room_pos))
            elif counter < 76:
                gameDisplay.blit(room_image_list[2], apply(camera_state, room_pos))
            elif counter < 101:
                gameDisplay.blit(room_image_list[3], apply(camera_state, room_pos))
            counter += 1

        #loop through the pitfalls dictionary keys
        #if the value corresponding to the key is True, blit the pitfall image at that room's rect
        for pfalls in pitfalls:
            if pitfalls[pfalls] == True:
                gameDisplay.blit(pitfall_image, apply(camera_state, rooms[pfalls]))

        #blit the player 1 and 2 images at the player 1 and 2 rects
        gameDisplay.blit(player1.image, apply(camera_state, player1.rect))
        gameDisplay.blit(player2.image, apply(camera_state, player2.rect))

        #loop through the cannons dictionary keys
        #if the 0th element (of the value) corresponding to the key is True, blit the cannon image at that room location
        for cannon in cannons:
            if cannons[cannon][0] == True:
                gameDisplay.blit(cannons[cannon][2], apply(camera_state, rooms[cannon]))

        #if the six flag is True, blit the roll_six text on the left side of the screen
        if six:
            gameDisplay.blit(roll_again, (32, 164))

        gameDisplay.blit(menu, menu_rect)#blit the menu button at the menu rect (in the top middle of the screen)
        gameDisplay.blit(view, (545, 32))#blit the view text to the right of the menu button
        gameDisplay.blit(switch_image, switch_rect)#blit the view button under the view text
        gameDisplay.blit(turn, (32,32))#blit the turn text to the left of the menu button
        gameDisplay.blit(dice_dict[index], dice_rect)# the dice button under the turn text
        pygame.display.update()#update the display
        frame_count += 1#increment the frame_count by 1

#apply function, moves the target_rect (rooms and other rects) to the position of the camera_state
def apply(state, target_rect):
    return target_rect.move(state.topleft)

#camera_scroll function, takes target_rect (player rects), half_width, half_height, width, height
#moves the screen along with the player
def camera_scroll(state, target_rect, half_width, half_height, width, height):
    l, t, _, _ = target_rect
    _, _, w, h = state
    l, t, _, _ = -l+half_width, -t+half_height, w, h # center player

    l = min(0, l)# stop scrolling at the left edge
    l = max(-(state.width-width), l)# stop scrolling at the right edge
    t = max(-(state.height-height), t)# stop scrolling at the bottom
    t = min(0, t)# stop scrolling at the top

    return Rect(l, t, w, h)#return the rect of (l, t, w, h)

#player_update function, animates the player moving through the castle
#takes player object, room list, room number, up_room, and the sides and locations of the rects corresponding to the player
#player1 = bottomleft, player2 = bottomright
def player_update(player, rooms, number, up_room, room_index, up_side, room_side, player_side, player_location, room_location, side_96, side_97, side_99, side_100):
    #if the player rect's bottom is colliding with the room bottom, room100 bottom, or room99 bottom, set the delta y value to 0
    #prevents the player from flying off
    if player.rect.bottom == rooms[number].bottom or player.rect.bottom == rooms[100].bottom or player.rect.bottom == rooms[99].bottom:#If statement to prevent the player from flying off into space
        player.dy = 0

    #if the room_number is equal to room_index (checks if the player needs to go back or not)
    #delta y values being set to 0 prevent the player from flying off
    if number == room_index:
        #check if the up side is to the right of the room side
        #check if their y values is the same
        if up_side > room_side and up_room.top == rooms[number].top:
            #if the player side is to the left of the room side, move the player right
            #set delta x value to 8 (moves player right)
            if player_side < room_side:
                player.dx = 8
                player.dy = 0
            #otherwise, if the player side is equal to the room side, set the delta x value to 0 (stops horizontal player movement)
            else:
                player.dx = 0
        #check if the up side is to the left of the room side and the
        #check if their y values are the same
        elif up_side < room_side and up_room.top == rooms[number].top:
            #if the player side is to the right of the room side, move the player left
            #set delta x value to -8 (moves player left)
            if player_side > room_side:
                player.dx = -8
                player.dy = 0
            #else, if the player side is to the left of the room side, move the player right
            #set delta x value to 8 (fixes bug)
            elif player_side < room_side:
                player.dx = 8
                player.dy = 0
            #otherwise, if the player side is equal to the room side, set the delta x value to 0
            else:
                player.dx = 0
        #check if the up_side is the same as the room_side
        #check is their y values are the same
        elif up_side == room_side and up_room.top == rooms[number].top:
            #if the player side is to the left of the room side
            #set the delta x value to 8
            if player_side < room_side:
                player.dx = 8
                player.dy = 0
            #if the player side is to the right of the room side
            #set the delta x value to -8
            elif player_side > room_side:
                player.dx = -8
                player.dy = 0
            #otherwise, if the player side is equal to the room side, set the delta x value to 0
            else:
                player.dx = 0
        #check if the up_side is to the right of the room_side
        #check is the up_room.top is below the room_number.top
        elif up_side > room_side and up_room.top > rooms[number].top:
            #if the player_side is to the left of the up_side
            #set the delta x value to 8
            if player_side < up_side:
                player.dx = 8
                player.dy = 0
            #if the player_side is equal to the up_side
            #set the delta y value to -8 (moves player up)
            #it will stop when it reaches the bottom rect of the room number bottom
            elif player_side == up_side:
                player.dy = -8
                player.dx = 0
        #check if the up_side is to the left of the room_side
        #check is the up_room.top is below the room_number.top
        elif up_side < room_side and up_room.top > rooms[number].top:
            #if the player_side is to the right of the up_side
            #set the delta x value to 8
            if player_side > up_side:
                player.dx = -8
                player.dy = 0
            #if the player_side is equal to the up_side
            #set the delta y value to -8 (it will stop when it reaches the bottom rect of the room number bottom)
            elif player_side == up_side:
                player.dy = -8
                player.dx = 0
        #check if the up_side is to the equal to the room_side
        #check is the up_room.top is below the room_number.top
        elif up_side == room_side and up_room.top > rooms[number].top:
            #if the player_side is to the left of the room_side
            #set the delta x value to 8
            if player_side < room_side:
                player.dx = 8
                player.dy = 0
            #if the player_side is to the left of the room_side
            #set the delta x value to -8
            elif player_side > room_side:
                player.dx = -8
                player.dy = 0
            #otherwise, if the player side is equal to the room side, set the delta x value to 0
            #set the delta y value to -8
            else:
                player.dx = 0
                player.dy = -8
    #if the room_number is not equal to room_index (room_index will exceed 100)
    elif number < room_index:
        #if the been there flag is False and the player is in the room (corresponding to the room number)
        if not player.been_there and not player.rect.colliderect(rooms[number]):
            #if the player_side is to the left of room 96 and the bottom values are equal
            #set the delta x value to 8 so the player can move right to room 96
            if player_side < side_96 and player.rect.bottom == rooms[96].bottom:
                player.dx = 8
            #if the player side is equal to the room 96 side and the bottom value of the player is smaller than the room 97 bottom (player is below room 97)
            #set the delta y value to -8, moves player up to room 97
            elif player_side == side_96 and player.rect.bottom > rooms[97].bottom:
                player.dx = 0
                player.dy = -8
            #if the player_side is to the right of room 99 and bottom values are equal
            #set the delta x value to -8, moving the player left to room 99
            elif player_side > side_99 and player.rect.bottom == rooms[99].bottom:
                player.dy = 0
                player.dx = -8
            #if the player_side is equal to the room 99 side and the player is below room 100
            #set the delta y value to -8, moves player up to the y value of room 100
            elif player_side == side_99 and player.rect.bottom > rooms[100].bottom:
                player.dx = 0
                player.dy = -8
            #if the player_side is to the left of the room 100 side and the bottom values are equal
            #set the delta x value to 8, moving the player right to room 100
            elif player_side < side_100 and player.rect.bottom == rooms[100].bottom:
                player.dy = 0
                player.dx = 8
            #if the player side is equal to the room 100 side and the bottom values are equal
            #set the delta x value to 0
            #set the been_there flag to True
            elif player_side == side_100 and player.rect.bottom == rooms[100].bottom:
                player.dx = 0
                player.been_there = True
        #otherwise, if the been_there flag is true
        #will move the player down after it goes to room 100
        else:
            #if the player side is to the right of room 99 and the player bottom is equal to room 100's bottom
            #set the delta x value to -8, moving the player left to the room 99 left
            if player_side > side_99 and player.rect.bottom == rooms[100].bottom:
                player.dx = -8
            #if the player side is equal to the side of room 99 and the player is above room 99
            #set the delta y value to 8, moving the player down to room 99
            elif player_side == side_99 and player.rect.bottom < rooms[99].bottom:
                player.dx = 0
                player.dy = 8
            #if the player_side is to the left of the room side and the bottom values are equal
            #set the delta x value to 8, moving the player to the room
            elif player_side < room_side and player.rect.bottom == rooms[number].bottom:
                player.dx = 8
            #if the player location is equal to the room location (ie. player.bottomleft == room.bottomleft)
            #set the delta x value to 0, to stop the player's horizontal movement
            elif player_location == room_location:
                player.dx = 0
                player.been_there = False
            #if the player side is to the left of the side of room 97 and the bottom values are the same and room is smaller or equal to 97
            #set the delta x value to 8 and move the player to room 97
            elif player_side < side_97 and player.rect.bottom == rooms[97].bottom and number <= 97:
                player.dx = 8
            #if the player side is equal to the side of room 97 and the player is above the room
            #set the delta y value to 8, moving the player down to the same floor as the room
            #set the delta x value to 0 so the player stops moving horizontally
            elif player_side == side_97 and player.rect.bottom < rooms[number].bottom:
                player.dx = 0
                player.dy = 8
            #if the player side is to the right of the room side and to bottom values are equal
            #set the delta y value to 0 so the player doesn't keep moving down
            #set the delta x value to -8 so the player moves left to the room
            elif player_side > room_side and player.rect.bottom == rooms[number].bottom:
                player.dy = 0
                player.dx = -8

    #increment the left of the player rect with the delta x value
    #increment the top of the player rect with the delta y value
    player.rect.left += player.dx
    player.rect.top += player.dy

#dice_roll function rolls the dice and takes the index and dice_rect
    #sees if the mouse is clicking and colliding with the dice_rect
        #set index to a random number between 1 to 6
    #return index
def dice_roll(index, dice_rect):
    if pygame.mouse.get_pressed()[0] and dice_rect.collidepoint(pygame.mouse.get_pos()):
        index = random.randint(1, 6)
    return index

#projectile_motion function launches the player
#takes player, delta time, time and initial velocity
def projectile_motion(player, dt, t, v0):
    last = player.rect.copy()#copy the player position, before velocity and acceleration are applied

    t = t + dt/250.0 # updated time
    a = (0.0, 10.0) # acceleration
    v = (v0[0] + a[0]*t, v0[1] + a[1]*t)#velocity
    vm = sqrt(v[0]*v[0] + v[1]*v[1])#initial speed
    s0 = player.last_pos # initial position
    #add the correspondonding intial velocity x time and 1/2 x accekeration x time^2 to the corresponding element of the intial player position
    player.rect.topleft = (s0[0] + v0[0]*t + a[0]*t*t/2, s0[1] + v0[1]*t + a[1]*t*t/2)

    #return the updated time, the initial speed, and the player position before movement
    return t, vm, last

#gravity function, makes player fall down
#takes player, delta time, time, initial velocity, the bottom room, player 1 and 2, and the falling sound
def gravity(player, dt, t, v0, bot, player1, player2, falling_sound):
    last = player.rect.copy()#copy the player position, before velocity and acceleration are applied

    t = t + dt/250.0 # updated time
    a = (0.0, 10.0) # acceleration
    v = (v0[0] + a[0]*t, v0[1] + a[1]*t) # velocity
    vm = sqrt(v[0]*v[0] + v[1]*v[1])#initial speed
    s0 = player.last.topleft # initial position
    #add the correspondonding intial velocity x time and 1/2 x accekeration x time^2 to the corresponding element of the intial player position
    player.rect.topleft = (s0[0] + v0[0]*t + a[0]*t*t/2, s0[1] + v0[1]*t + a[1]*t*t/2)


    new = player.rect#the player position after movement
    if player.rect.colliderect(bot):#if the player rect collides with the bottom room
        falling_sound.play()#play the falling sound
        #check if the last rect bottom is smaller or equal to the bottom of the bot room
        #and if the new rect bottom is larger than the bottom of the bot room
            #if it is, set the falling flag to false
            #call the player_set function to set the player_position
        if last.bottom <= bot.bottom and new.bottom > bot.bottom:
            player.falling = False
            player_set(player, player1, player2, bot)

    #return time and initial speed
    return t, vm

#rot_center function, rotates an image
#takes the image and the angle
def rot_center(image, angle):
    #rotate an image while keeping its center and size
    orig_rect = image.get_rect()#get the rect of the image
    rot_image = pygame.transform.rotate(image, angle)#rotate the image with the angle
    rot_rect = orig_rect.copy()#copy the original rect with .copy(), will be unaffected by changes to orig rect
    rot_rect.center = rot_image.get_rect().center#set the center of rot_rect to the center of the image, rotate around the center of the image
    rot_image = rot_image.subsurface(rot_rect).copy()#set the image to the subsurface of rot_rect
    return rot_image#return the rotated image

#room_counter function, increments and decrements the room number and room index
#takes the player object and index as parameters
    #set the room_index to the room_number plus the index
    #increment the room_number with the index
    #if the room_number is greater than 100
        #subtract the difference between the room_number and 100 from 100 (excess from max)
def room_counter(player, index):
    player.room_index = player.room_number + index
    player.room_number += index
    if player.room_number > 100:
        player.room_number = 100 - (player.room_number - 100)

#angle_change_counterclockwise function, changes the angle of the cannon counterclockwise
#takes the player object, cannon dict, and the cannon_image
    #(if the player presses left) add 2 to the angle value of the room_number key (1st element of the value)
        #if the angle is greater than 180, set the angle to 180
    #call on the rot_center function to rotate the image with its corresponding angle
    #return the cannon dict
def angle_change_counterclockwise(player, cannons, cannon_image):
    cannons[player.room_number][1] += 2
    if cannons[player.room_number][1] > 180:
        cannons[player.room_number][1] = 180
    cannons[player.room_number][2] = rot_center(cannon_image,  cannons[player.room_number][1])

    return cannons

#angle_change_clockwise, changes the angle clockwise
#takes the player object, cannon dict, and the cannon_image
    #(if the player presses left) subtract 2 to the angle value of the room_number key (1st element of the value)
        #if the angle is smaller than 0, set the angle to 0
    #call on the rot_center function to rotate the image with its corresponding angle
    #return the cannon dict
def angle_change_clockwise(player, cannons, cannon_image):
    cannons[player.room_number][1] -= 2
    if cannons[player.room_number][1] < 0:
        cannons[player.room_number][1] = 0
    cannons[player.room_number][2] = rot_center(cannon_image,  cannons[player.room_number][1])

    return cannons

#launcher function, initializes the time, and intial velocity
#takes the player object and cannon dict
    #set the last pos of the player to the topleft of the player rect
    #set the time to 0
    #set the initial speed to 65
    #set the initial velocity to the speed times the direction (corresponding elements in a tuple)
    #set the player launched flag to True
    #return time and initial velocity
def launcher(player, cannons):
    player.last_pos = player.rect.topleft # space
    t = 0 # time
    vm = 65 # initial speed
    v0 = (vm*cos(radians(cannons[player.room_number][1])), -vm*sin(radians(cannons[player.room_number][1]))) #initial velocity
    player.launched = True

    return t, v0

#dropper function, initializes the time, initial velocity, and bot room
#takes the player object, player 1 and 2 objects, and the rooms list
def dropper(player, player1, player2, rooms):
    player.last = player.rect.copy() # space
    t = 0#time is 0
    vm = 0#initial speed is 0, player will fall
    v0 = (vm*cos(radians(270)), -vm*sin(radians(270)))#initial velocity
    player.falling = True#set the falling flag to True
    for room in rooms:#use room to iterate through the room list
        #check if the room bottom is equal to the player bottom plus
        #the minimum values of the room number floor divided by 10 or 3 (sets the maximum floor fall to 3) and multiply by 80 (80 x 80 px per room)
        if room.bottom == player.rect.bottom + min((player.room_number//10), 3)*80:
            #if the player is player 1
            if player.rect == player1.rect:
                #if the left side of the room is equal to player1's left side (if rooms align)
                    #bot is equal to the room
                if room.left == player.rect.left:
                    bot = room
                #if the left side of the room is equal to player1's left side subtracted by 40 (if rooms don't align)
                    #bot is equal to the room
                elif room.left == player.rect.left - 40:
                    bot = room
            #if the player is player 2
            elif player.rect == player2.rect:
                #if the right side of the room is equal to player2's right side (if rooms align)
                    #bot is equal to the room
                if room.right == player.rect.right:
                    bot = room
                #if the right side of the room is equal to player1's right side plus 40 (if rooms don't align)
                    #bot is equal to the room
                elif room.right == player.rect.right + 40:
                    bot = room

    #return the time, the initial velocity, and the bottom room
    return t, v0, bot

#player_collision function, prevents the player from flying out of the castle
#takes the player object, the room list, the player's rect before movement (last), the left, right and top lists, and the player 1 and 2 objects
def player_collision(player, rooms, last, left, right, top, player1, player2):
    new = player.rect#get the current player rect
    #loop through the room list and get the index of the rect colliding with the player
        #set b to the rect of b
        #if the bottom of last is smaller or equal to the bottom of b
        #and if the new bottom is larger than the b's bottom
            #set the launched flag to False
            #call the player set function and give it player, player 1 and 2, and the rect
    for b in player.rect.collidelistall(rooms):
        b = rooms[b]
        if last.bottom <= b.bottom and new.bottom > b.bottom:
            player.launched = False
            player_set(player, player1, player2, b)

    #loop through the left list and get the index of the outer left rect colliding with the player
        #set lf to the rect of lf
        #if the bottom of last is larger or equal to the bottom of lf
        #and if the new bottom is smaller than the lf's bottom
            #set the launched flag to False
            #call the player set function and give it player, player 1 and 2, and the rect
    for lf in player.rect.collidelistall(left):
        lf = left[lf]
        if last.left >= lf.left and new.left < lf.left:
            player.launched = False
            player_set(player, player1, player2, lf)

    #loop through the right list and get the index of the outer right rect colliding with the player
        #set rg to the rect of rg
        #if the bottom of last is smaller or equal to the bottom of rg
        #and if the new bottom is larger than the rg's bottom
            #set the launched flag to False
            #call the player set function and give it player, player 1 and 2, and the rect
    for rg in player.rect.collidelistall(right):
        rg = right[rg]
        if last.right <= rg.right and new.right > rg.right:
            player.launched = False
            player_set(player, player1, player2, rg)

    #loop through the top list and get the index of the top rect colliding with the player
        #set tp to the rect of tp
        #if the bottom of last is larger or equal to the bottom of tp
        #and if the new bottom is smaller than the tp's bottom
            #set the launched flag to False
            #call the player set function and give it player, player 1 and 2, and the rect
    for tp in player.rect.collidelistall(top):
        tp = top[tp]
        if last.top >= tp.top and new.top < tp.top:
            player.launched = False
            player_set(player, player1, player2, tp)

#player_set function, sets the player rect to the location of the room
#takes the player object, the player 1 and 2 object, and the cell that collides with the player
    #if the player is player 1
        #set the bottomleft of the player to the bottomleft of the cell
    #if the player is player 2
        #set the bottomright of the player to the bottomright of the cell
def player_set(player, player1, player2, cell):
    if player.rect == player1.rect:
        player1.rect.bottomleft = cell.bottomleft
    elif player.rect == player2.rect:
        player2.rect.bottomright = cell.bottomright

#room_detection function, sets the room number to the number of the rect it's in
#takes the player object and the rooms list
    #iterate through the rooms list with room
        #if room collides with the topleft of the player rect
            #the room number is equal to the index of that rect
    #set the room index to the room number
def room_detection(player, rooms):
    for room in rooms:
        if room.collidepoint(player.rect.topleft):
            player.room_number = rooms.index(room)
    player.room_index = player.room_number

#player_flip function, flips the player depending on floor and direction of movement
#takes player object
def player_flip(player, rooms):
    if (player.rect.bottom // 80) % 2 == 0 and player.rect.bottom == rooms[player.room_number].bottom:#see if the floor is even and if the player is on the floor
        if player.flip:#flag to see if the image was flipped
            player.image = pygame.transform.flip(player.image, True, False)#flip horizontally
            player.flip = False#set to False so picture won't flip if on an even floor
    elif (player.rect.bottom // 80) % 2 != 0 and player.rect.bottom == rooms[player.room_number].bottom:#see if the floor is odd and if the player is on the floor
        if not player.flip:#flag to see if the image was not flipped
            player.image = pygame.transform.flip(player.image, True, False)#flip horizontally
            player.flip = True#set to True so picture won't flip if on an odd floor

#def win_display, the victory screen display when a player reaches room 100
#takes the game_winner (1 or 2), gameDisplay, board flag, turn number, player 1 and 2 room numbers
def win_display(game_winner, gameDisplay, board, turns, number1, number2):
    size = (800,640)#size of the screen

    title_font = pygame.font.Font("fonts/blackwood-castle.regular.ttf", 80)#font for the title
    button_font = pygame.font.Font("fonts/blackwood-castle.regular.ttf", 60)#font for the buttons
    word_font = pygame.font.Font("fonts/blackwood-castle.regular.ttf", 50)#font for the words

    if game_winner == '1':#if the game_winner is '1' (player 1)
        background = pygame.image.load('images/KnightBackground.png').convert()#set the background image to the knight background
        colour = (255,69,0)#set the color to red
    else:#otherwise, if the game_winner is '2' (player 2)
        background = pygame.image.load('images/RogueBackground.png').convert()#set the background image to the rogue background
        colour = (169,169,169)#set the color to grey

    #set rgb values to their corresponding colour
    grey = (150,150,150)
    yellow = (255,255,0)

    winner = text(title_font, 'Player ' + game_winner + ' Wins', colour)#use the text function to create the winner/title text
    winner_rect = winner.get_rect()#get the rect of the winner text
    winner_rect.center = (size[0]//2, size[1]//4)#set the center to the middle top of the screen

    menu = text(button_font, 'Menu', grey)#create a menu button
    menu_rect = menu.get_rect()#get the rect of the menu button
    menu_rect.center = (size[0]//2, size[1]//1.05)#set the center to the bottom middle of the screen

    greater, lesser = greater_and_lesser(number1, number2)#using the greater lesser function, finder the greater and lesser numbers
                                                          #give number1 and number 2 (player 1 and 2 room numbers)
    room_diff = greater - lesser#get the room difference

    if turns == 0:#prevents unidentified
        turns = 1
    score = int(room_diff/turns*10000)#calculate the score
                                      #highscore is directly proportional to room_diff
                                      #highscore is inversely proportional to turns

    turn_display = text(word_font, 'Turns Taken: ' + str(turns), colour)#create the turn text
    turn_display_rect = turn_display.get_rect()#get the rect of the turn text
    turn_display_rect.center = (size[0]//2, size[1]//2.5)#set the center of the turn text above the middle of the screen

    diff_display = text(word_font, 'Room Difference: ' + str(room_diff), colour)#create the difference text
    diff_display_rect = diff_display.get_rect()#get the rect of the difference text
    diff_display_rect.center = (size[0]//2, size[1]//2.1)#set the center of the difference text to the middle of the screen

    score_display = text(button_font, 'Score: ' + str(score), colour)#create the score text
    score_display_rect = score_display.get_rect()#get the rect of the score text
    score_display_rect.center = (size[0]//2, size[1]//1.75)#set the center of the score text to below the difference text

    prompt = text(word_font, 'Enter Your Name:', colour)#create a name prompt
    prompt_rect = prompt.get_rect()#get the rect of the prompt
    prompt_rect.center = (size[0]//2, size[1]/1.5)#center the prompt to under the score display

    name = ''#initialize the name string
    player_name = text(word_font, '▯▯▯▯', colour)#create a name text with 'boxes'
    name_rect = player_name.get_rect()#get the rect of the name text
    name_rect.center = (size[0]//2, size[1]/1.25)#set the center of the rect to under the prompt

    victory = pygame.mixer.Sound(file='sound/VictoryMusic.ogg')#load the victory music file
    victory.play()#play the victory music

    win = True#set a win flag to True

    while win:#while the win flag is True
        clock.tick(30)#set the fps to 30

        for event in pygame.event.get():#for event in the pygame event list
            if event.type == QUIT:#if the event type is QUIT
                pygame.mixer.quit()#quit the pygame mixer
                pygame.quit();sys.exit()#quit pygame and the module
            elif event.type == MOUSEBUTTONDOWN:#if the event type is MOUSEBUTTONDOWN
                if menu_rect.collidepoint(event.pos):#if the mouse clicks on the menu button
                    board = False#set the board flag to False so the board_game_loop ends
                    win = False#set the win flag to False so the win loop ends
            elif event.type == KEYDOWN:#if the event type is KEYDOWN
                if event.key == K_BACKSPACE and len(name) > 0:#if the user presses backspace
                    name = name[:-1] #cut off last character
                elif (event.unicode.isalnum()) and len(name) < 4:#if the user presses a unicode key, add it to the string
                    name += event.unicode #adds character value of key
                player_name = text(word_font, name, colour)#change the player name

        if menu_rect.collidepoint(pygame.mouse.get_pos()):#if the mouse hovers over the menu button, change the colour to yellow
            menu = text(button_font, 'Menu', yellow)
        else:#otherwise, leave it or change it back to grey
            menu = text(button_font, 'Menu', grey)

        gameDisplay.blit(background, (0,0))#blit the background at (0,0)
        gameDisplay.blit(winner, winner_rect)#blit the winner text at the top
        gameDisplay.blit(turn_display, turn_display_rect)#blit the turn text under the title
        gameDisplay.blit(diff_display, diff_display_rect)#blit the diff text under the turn text
        gameDisplay.blit(score_display, score_display_rect)#blit the score text under the diff text
        gameDisplay.blit(prompt, prompt_rect)#blit the prompt under the score
        gameDisplay.blit(player_name, name_rect)#blit the name under the prompt
        gameDisplay.blit(menu, menu_rect)#blit the menu button at the bottom
        pygame.display.update()#update the screen

    saving_highscore(game_winner, name, score)#call the saving high_score function and pass it the game_winner and score

    return board#return the board flag

#def how_to_play_display, shows instructions and takes gameDisplay
def how_to_play_display(gameDisplay):
    size = (800, 640)#size of the screen
    word_font = pygame.font.SysFont("garamond", 30)#font for words
    button_font = pygame.font.Font("fonts/blackwood-castle.regular.ttf", 50)#font for buttons

    #set rgb values to their corresponding colour
    yellow = (255,215,0)
    moon = (232,248,192)
    teal = (48,136,120)

    next =  text(button_font, 'Next', moon)#create next button
    next_rect = next.get_rect()#get the rect of the next button
    next_rect.center = ((size[0]//2)*1.5, (size[1]//2)*1.75)#set the center to the bottom right of the screen

    previous = text(button_font, 'Previous', moon)#create previous button
    previous_rect = previous.get_rect()#get the rect of the previous button
    previous_rect.center = (size[0]//4, (size[1]//2)*1.75)#set the center to the bottom left of the screen

    menu = text(button_font, 'Menu', moon)#create menu button
    menu_rect = menu.get_rect()#get the rect of the previous button
    menu_rect.center = (size[0]//2, (size[1]//2)*1.75)#set the center to the bottom middle of the screen

    title = text(button_font, 'How to Play', (218,165,32))#create the title text
    title_rect = title.get_rect()#get the rect of the title text
    title_rect.center = (size[0]//2, size[1]//8)#set the center to the middle top of the screen

    #create the first page text
    first_text1 = text(word_font, 'Both players will get the chance to roll the dice alternatively.', moon)
    first_text2 = text(word_font, 'On your turn, roll the dice and your player will travel the distance.', moon)
    dice = pygame.image.load('images/D4.png').convert_alpha()#load the dice picture
    dice_rect = dice.get_rect()#get the rect of the dice
    dice_rect.center = (size[0]//2, size[1]//1.75)#set the center to the middle of the screen

    #create second page text
    second_text = text(word_font, 'You can change the player view with the switch view button.', moon)
    switch_view = pygame.image.load('images/switchLit.png').convert_alpha()#load the switch picture
    switch_view_rect = switch_view.get_rect()#get the rect of the switch
    switch_view_rect.center = (size[0]//2, size[1]//2)#set the center to the middle of the screen

    #create third page text
    third_text1 = text(word_font, 'If you enter a room with a cannon, you can launch yourself up to', moon)
    third_text2 = text(word_font, 'another room using projectile motion by pressing the SPACEBAR.', moon)
    cannon = pygame.image.load('images/cannon.png').convert_alpha()#load the cannon picture
    cannon_rect = cannon.get_rect()#get the rect of the cannon
    cannon_rect.center = (size[0]//2, size[1]//2)#set the center to the middle of the screen

    spacebar = pygame.image.load('images/Spacebar.png').convert_alpha()#load the spacebar picture
    spacebar_rect = spacebar.get_rect()#get the rect of the spacebar
    spacebar_rect.center = (size[0]//2, size[1]//1.5)#set the center to under the cannon

    #create fourth page text
    fourth_text1 = text(word_font, 'Furthermore, you can rotate the cannon with the left and right', moon)
    fourth_text2 = text(word_font, 'arrow keys to determine the direction you want to go.', moon)
    arrow_keys = pygame.image.load('images/ArrowKeys.png').convert_alpha()#load the arrow keys picture
    arrow_keys_rect = arrow_keys.get_rect()#get the arrow keys rect
    arrow_keys_rect.center = (size[0]//2, size[1]//1.75)#set the center to the middle of the screen

    #create fifth page text
    fifth_text1 = text(word_font, 'If you enter a room with a pitfall sign, you will fall down', moon)
    fifth_text2 = text(word_font, 'one, two, or three levels. You must then start again from the', moon)
    fifth_text3 = text(word_font, 'room you just fell into.', moon)
    pitfall = pygame.image.load('images/pitfall.png').convert_alpha()#load the pitfall sign picture
    pitfall_rect = pitfall.get_rect()#get the pitfall sign rect
    pitfall_rect.center = (size[0]//2, size[1]//1.75)#set the center to the middle of the screen

    #create sixth page text
    sixth_text = text(word_font, 'Each time you roll a 6, you will get an extra turn.', moon)
    dice6 = pygame.image.load('images/D6.png').convert_alpha()#load the dice 6 picture
    dice6_rect = dice6.get_rect()#get the dice 6 rect
    dice6_rect.center = (size[0]//2, size[1]//2)#set the center to the middle of the screen

    #create seventh page text
    seventh_text = text(word_font, 'The first one to reach the 100th room in the castle wins.', moon)
    room100 = pygame.image.load('images/room100.png').convert()#load the room 100 picture
    room100_rect = room100.get_rect()#get the room 100 rect
    room100_rect.center = (size[0]//2, size[1]//1.75)#set the center to the middle of the screen

    page = 1#set a counter called page to True
    instruction = True#set a flag called instruction to True

    while instruction:#while instruction is True
        clock.tick(30)#set the clock to 30 fps

        for event in pygame.event.get():#for event in the pygame event list
            if event.type == QUIT:#if event type is QUIT
                pygame.mixer.quit()#quit the pygame mixer
                pygame.quit();sys.exit()#quit pygame and the module
            elif event.type == MOUSEBUTTONDOWN:#if event type is MOUSEBUTTONDOWN
                if next_rect.collidepoint(mouse_pos):#if the mouse clicks the next button
                    page += 1#increment page
                    page = min(7, page)#don't let page exceed 7
                elif previous_rect.collidepoint(mouse_pos):#if mouse clicks the previous button
                    page -= 1#decrement page
                    page = max(1, page)#don't let page go below 1
                elif menu_rect.collidepoint(mouse_pos):#if mouse clicks the menu button
                    instruction = False#set the instruction flag to False

        mouse_pos = pygame.mouse.get_pos()#set the mouse position to mouse_pos

        if next_rect.collidepoint(mouse_pos):#if the mouse hovers over the next button, change the colour to yellow
            next = text(button_font, 'Next', yellow)
        else:#otherwise, leave it or change it back to grey
            next = text(button_font, 'Next', moon)

        if previous_rect.collidepoint(mouse_pos):#if the mouse hovers over the previous button, change it to yellow
            previous = text(button_font, 'Previous', yellow)
        else:#otherwise, leave it or change the colour back to grey
            previous = text(button_font, 'Previous', moon)

        if menu_rect.collidepoint(mouse_pos):#if the mouse hovers over the menu button, the colour becomes yellow
            menu = text(button_font, 'Menu', yellow)
        else:#otherwise, the color becomes grey
            menu = text(button_font, 'Menu', moon)

        gameDisplay.fill(teal)#fill the gameDisplay with teal

        if page == 1:#if page is equal to 1, blit the contents of the first page onto the gameDisplay
            gameDisplay.blit(first_text1, (16, size[1]//3.5))
            gameDisplay.blit(first_text2, (16, size[1]//3))
            gameDisplay.blit(dice, dice_rect)
        elif page == 2:#if page is equal to 2, blit the contents of the second page onto the gameDisplay
            gameDisplay.blit(second_text, (16, size[1]//3.5))
            gameDisplay.blit(switch_view, switch_view_rect)
        elif page == 3:#if page is equal to 3, blit the contents of the third page onto the gameDisplay
            gameDisplay.blit(third_text1, (16, size[1]//3.5))
            gameDisplay.blit(third_text2, (16, size[1]//3))
            gameDisplay.blit(cannon, cannon_rect)
            gameDisplay.blit(spacebar, spacebar_rect)
        elif page == 4:#if page is equal to 4, blit the contents of the fourth page onto the gameDisplay
            gameDisplay.blit(fourth_text1, (16, size[1]//3.5))
            gameDisplay.blit(fourth_text2, (16, size[1]//3))
            gameDisplay.blit(arrow_keys, arrow_keys_rect)
        elif page == 5:#if page is equal to 5, blit the contents of the fifth page onto the gameDisplay
            gameDisplay.blit(fifth_text1, (16, size[1]//3.5))
            gameDisplay.blit(fifth_text2, (16, size[1]//3))
            gameDisplay.blit(fifth_text3, (16, size[1]//2.6))
            gameDisplay.blit(pitfall, pitfall_rect)
        elif page == 6:#if page is equal to 6, blit the contents of the sixth page onto the gameDisplay
            gameDisplay.blit(sixth_text, (16, size[1]//3.5))
            gameDisplay.blit(dice6, dice6_rect)
        else:#if page is equal to 7, blit the contents of the seventh page onto the gameDisplay
            gameDisplay.blit(seventh_text, (16, size[1]//3.5))
            gameDisplay.blit(room100, room100_rect)

        gameDisplay.blit(title, title_rect)#blit the title onto the gameDisplay at the middle top
        if page < 7:#if the page is smaller than 7, blit the next button
            gameDisplay.blit(next, next_rect)
        if page > 1:#if page is greater than 1, blit the previous button
            gameDisplay.blit(previous, previous_rect)
        gameDisplay.blit(menu, menu_rect)#blit the menu button at the bottom middle
        pygame.display.update()#update the display


#greater_and_lesser function, gets the greater and lesser number out of 2 numbers
#takes number1 and number2
    #if number1 is greater than number2
        #greater is equal to number1
        #lesser is equal to number2
    #if number1 is smaller than number2
        #greater is equal to number2
        #lesser is equal to number1
    #return greater and lesser
def greater_and_lesser(number1, number2):
    if number1 > number2:
        greater = number1
        lesser = number2
    elif number1 < number2:
        greater = number2
        lesser = number1
    return greater, lesser

#def saving_highscore, saves score onto csv file
#takes the game_winner (1 or 2), player name, and the score
    #open the 'HighScore.csv' file in append mode
    #create a string called score and separate the contents with commas and add a new line character at the end
    #write score into the file
    #close the file
    #call the organize function and give it the file name
def saving_highscore(game_winner, name, highscore):
    scoreFile = open('HighScore.csv','a')
    score = game_winner + ',' + name + ',' + str(highscore) + ',\n'
    scoreFile.write(score)
    scoreFile.close()

    organize('HighScore.csv')

#organize, organizes contents of the csv file by score from greatest to least
#takes the file name
def organize(file):
    highscore = ''#create an empty string to contain the data on the file
    scoreDict = {}#create an empty dict used to organize the data
    scoreFile = open(file, 'r')#open the file in read mode

    for line in scoreFile:#for line in the file
        line = line.split(',')#split the line by commas
        line[2] = int(line[2])#set the first element of the line to an integer
        scoreDict[line[2]] = line#append the line into the dict, the key is the first element in the list list
        scoreDict[line[2]].remove('\n')#remove the newline character from the list

    scoreFile.close()#close the file

    for key in sorted(scoreDict, reverse=True):#for key in the scoreDict, sorted and reverse = True, sorts from greatest to least
        for element in scoreDict[key]:#for element in the value of the key
            highscore += str(element) + ','#add the element, set to string, to the highscore, add commas after every element
        highscore += '\n'#end the line with a newline character

    scoreFile = open(file, 'w')#open the file in write mode
    scoreFile.write(highscore)#write the high score into the file
    scoreFile.close()#close the file

#highscore_display, displays the top ten highscores
#takes gameDisplay
def highscore_display(gameDisplay):
    size = (800,640)#size of the screen
    title_font = pygame.font.Font("fonts/blackwood-castle.regular.ttf", 60)#font for the tile
    button_font = pygame.font.Font("fonts/blackwood-castle.regular.ttf", 40)#font for the buttons and words

    background = pygame.image.load('images/CastleMenuPicture.png').convert()#load the background image
    background = pygame.transform.scale(background, (900, 700))#scale it to (900, 700) to provide some dynamics

    image_list = ['images/Knight.png','images/Rogue.png']
    for image in range(0,2):
        image_list[image] = pygame.image.load(image_list[image]).convert_alpha()#load the knight and rogue
        image_list[image] = pygame.transform.scale(image_list[image], (24, 48))#scale it to (24, 48) so it can fit on the screen

    #set rgb values to their corresponding colour
    red = (255,140,0)
    grey = (150,150,150)
    yellow = (255,255,0)

    highscore_title = text(title_font, 'High Scores', red)#create the highscore title
    highscore_rect = highscore_title.get_rect()#get the rect of the highscore title
    highscore_rect.center = (size[0]//2, size[1]//16)#set the center of the rect to the middle top of the screen

    player = text(button_font, 'Player', red)#create the player heading
    player_rect = player.get_rect()#get the rect of the player heading
    player_rect.center = (size[0]//8, size[1]//6)#set the center of the rect to the topleft of the screen, under the menu button

    score = text(button_font, 'Score', red)#create the score heading
    score_rect = score.get_rect()#get the rect of the score heading
    score_rect.center = ((size[0]//2)*1.75, size[1]//6)#set the center of the rect to the topright of the screen, under the menu button

    menu = text(button_font, 'Menu', grey)#create the menu button
    menu_rect = menu.get_rect()#get the rect of the menu button
    menu_rect.center = (size[0]//8, size[1]//16)#set the center of the rect to the topleft of the screen

    scoreFile = open('HighScore.csv', 'a')#initialize the 'HighScore.csv' file
    scoreFile.close()

    scoreFile = open('HighScore.csv', 'r')#open the 'HighScore.csv' in read mode
    line_count = 0#create a counter equal to 0
    rank = {}#create an empty dict for the rank (top ten)
    score_dict = {}#create an empty dict for the score
    image_dict = {}#create an empty dict for the image
    y = 128#set the default y value
    for line in scoreFile:#with line, loop through the scoreFile
        line_count += 1#increment the line_count by 1
        if line_count > 10:#if line count is greater than 10, break the loop. Makes it so only top 10 scores are shown
            break
        line = line.split(',')#split the string with commas
        #set the values of the line_count key in rank to the line_count and the player name in a string, and the coords of the rank using (32, y)
        rank[line_count] = [text(button_font, '{0:d}. {1:s}'.format(line_count, line[1]), (255,140,0)), (32, y)]
        #set the values of the line_count key in score_dict to the score in a string, and the coords of the rank using (640, y)
        score_dict[line_count] = [text(button_font, '{0:s}'.format(line[2]), (255,140,0)), (640, y)]
        #set the values of the line_count key in image_dict to the player image and the coords using (160, y)
        image_dict[line_count] = [image_list[int(line[0])-1], (160, y)]
        y += 48#increment y by 48 so the next rank is under the previous one

    scoreFile.close()#close the file

    highscore = True#set the highscore flag to True

    while highscore:#while the highscore flag is True
        clock.tick(30)#set the clock to 30fps

        for event in pygame.event.get():#for event in the pygame event list
            if event.type == QUIT:#if the event type is QUIT
                pygame.mixer.quit()#quit the pygame mixer
                pygame.quit();sys.exit()#quit pygame and the module
            elif event.type == MOUSEBUTTONDOWN:#if the event type is MOUSEBUTTONDOWN
                if menu_rect.collidepoint(event.pos):#if the mouse clicks on the menu button
                    highscore = False#set the highscore flag to False, ending the highscore loop

        if menu_rect.collidepoint(pygame.mouse.get_pos()):#if the mouse hovers over the menu button, change the colour to yellow
            menu = text(button_font, 'Menu', yellow)
        else:#otherwise, leave it or change it back to grey
            menu = text(button_font, 'Menu', grey)

        gameDisplay.blit(background, (0,0))#blit the background at (0,0)
        for key in rank:#for key in rank (keys will be the same for both dicts)
            gameDisplay.blit(rank[key][0], rank[key][1])#blit the rank and player at the rect
            gameDisplay.blit(image_dict[key][0], image_dict[key][1])#blit the player image at the rect
            gameDisplay.blit(score_dict[key][0], score_dict[key][1])#blit the score at the rect
        gameDisplay.blit(highscore_title, highscore_rect)#blit the highscore title at the middle top
        gameDisplay.blit(player, player_rect)#blit the player heading at the player_rect
        gameDisplay.blit(score, score_rect)#blit the score heading at the score_rect
        gameDisplay.blit(menu, menu_rect)#blit the menu button at the menu_rect
        pygame.display.update()#update the display

if __name__ == '__main__':
    game_menu()#call the game_menu() function
    pygame.quit();sys.exit()#quit pygame and the module
