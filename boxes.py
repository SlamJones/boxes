#!/usr/bin/env python3


import pygame
import random
from screeninfo import get_monitors




## Get the size of the main monitors screen
def get_screen_size():
    m = get_monitors()
    return(m[0].width,m[0].height)


def spawn_box(w,h):
    start_x = random.randrange(0,w)
    start_y = random.randrange(0,h)
    box = pygame.Rect(start_x,start_y,10,10)
    return(box)


def return_color(box,settings):
    if list(settings["color_set"].keys())[0] == "grayscale":
        return("gray{}".format(min(box.width,100)))
    for key in list(settings["color_set"].keys()):
            if box.width > int(key):
                return(settings["color_set"][key])
    return("pink")


def next_color_set(settings):
    settings["color_set"] = settings["color_sets"][0]
    
    color_set = settings["color_sets"][0]
    settings["color_sets"].remove(color_set)
    settings["color_sets"].append(color_set)
    return(settings)



def main():
    pygame.init()
    w,h = get_screen_size()
    h = h - 100 #Make screen narrower to avoid taskbar overlap
    screen = pygame.display.set_mode((w,h))
    clock = pygame.time.Clock()
    
    settings = {"frame_rate": 30, "color_set": {"grayscale": 0}, "color_shift_time": [0,0], "show_text": True,
        "color_sets": [
        {"grayscale": 0},
        {100: "red", 50: "orange", 0: "yellow"},
        {100: "light green", 50: "green", 0: "dark green"},
        {100: "aqua", 80: "sky blue", 60: "royal blue", 40: "slate blue", 20: "blue", 0: "navy blue"},
        {100: "red", 50: "crimson", 0: "dark red"},
        {100: "tan", 50: "sandy brown", 0: "saddle brown"},
        {100: "beige", 50: "khaki", 0: "dark goldenrod"},
        {100: "sky blue", 80: "cyan", 60: "royal blue", 40: "aquamarine", 20: "chartreuse", 0: "dark green"},]}
    
    dt = 1
    dt_hi = 0
    dt_low = 10000
    
    ## Player position text, which is overlaid onto player character object ##
    font = pygame.font.Font("freesansbold.ttf", 14)
    text = font.render("Test", True, "white")
    #textRect = text.get_rect()
    #textRect.center = start_pos
    
    ## FPS text, for debugging purposes ##
    fps_textRect = text.get_rect().copy()
    fps_textRect.center = (20,20)
    
    swap_textRect = text.get_rect().copy()
    swap_textRect.center = (w/2,20)
    
    
    boxes = []
    input_cd = [0,0]
    settings = next_color_set(settings)
    
    play = True
    while play:
        ## Clear screen ##
        screen.fill("black")
        
        ## Create a new box ##
        new_box = spawn_box(w,h)
        boxes.append(new_box)
        
        ## Process boxes ##
        for box in boxes.copy():
            box.inflate_ip(1,1)
            ## Remove box from list
            ## ## Otherwise it "collides" with itself
            boxes.remove(box)
            
            collision = pygame.Rect.collidelist(box, boxes)
            #print("collision = {}".format(collision))
            if collision == -1:
                ## If no collision, determine the color ##
                if settings["color_set"] == "grayscale":
                    if box.width < 100:
                        color = "gray{}".format(box.width)
                    else:
                        color = "white"
                else:
                    color = return_color(box,settings)
                ## If no collision, add box back into list and draw it ##
                boxes.append(box)
                pygame.draw.rect(screen, color, box)
        
        
        
        ## Screen frame rate and key text ##
        if dt != 1:
            dt_hi = max(dt_hi,dt*1000)
        dt_low = min(dt_low,dt*1000)
        if settings["show_text"]:
            fps_text = font.render(
                "{}ms\n{}ms (high)\n{}ms (low)\n{} boxes\nTap (w) to change color set\nTap (s) for auto color swap\nTap (d) to hide all text\nTap (esc) to quit".format(
                str(int(dt*1000)),str(dt_hi),str(dt_low),str(len(boxes))),True, "white")
            screen.blit(fps_text,fps_textRect)
        
        
        ## Process exit event, so player can quit game properly ##
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                play = False
                
                
        ## Check for auto color swap ##
        if settings["color_shift_time"] != [0,0]:
            if settings["show_text"]:
                swap_text = font.render("AUTO SWAP ON",True, "white")
                screen.blit(swap_text,swap_textRect)
            settings["color_shift_time"][0] += 1
            if settings["color_shift_time"][0] >= settings["color_shift_time"][1]:
                settings["color_shift_time"][0] = 0
                settings = next_color_set(settings)
            
                
        ## Get player input ##
        keys = pygame.key.get_pressed()
        
        if input_cd[1] > 0:
            input_cd[0] += 1
        elif input_cd[0] >= input_cd[1]:
            input_cd = [0,0]
        
        ## Process player input ##
        if keys[pygame.K_ESCAPE]:
            play = False
        if keys[pygame.K_w] and input_cd[0] >= input_cd[1]:
            input_cd = [0,10]
            settings = next_color_set(settings)
        if keys[pygame.K_s] and input_cd[0] >= input_cd[1]:
            input_cd = [0,10]
            if settings["color_shift_time"] == [0,0]:
                settings["color_shift_time"] = [0,60]
            else:
                settings["color_shift_time"] = [0,0]
        if keys[pygame.K_d] and input_cd[0] >= input_cd[1]:
            input_cd = [0,10]
            if settings["show_text"]:
                settings["show_text"] = False
            else:
                settings["show_text"] = True
            
    
        ## Update screen at 60fps as set in settings dict ##
        pygame.display.flip()
        dt = clock.tick(settings["frame_rate"]) / 1000
    
    return


main()
pygame.quit()
