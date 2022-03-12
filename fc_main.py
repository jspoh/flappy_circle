# based on the flappy bird concept but no bird
# may add more walls in a single screen in the future

import pygame
import sys
import random
import PySimpleGUI as sg

pygame.init()

win_width = 600
win_height = 600

win = pygame.display.set_mode((win_width, win_height))
pygame.display.set_caption("Flappy circle")
clock = pygame.time.Clock()

c_yellow = (255, 255, 0)
c_green = (0, 255, 0)
c_blue = (100, 100, 255)
c_darkBlue = (0, 30, 100)
c_white = (255, 255, 255)
c_black = (0, 0, 0)
c_darkGreen = (0, 100, 30)

font = pygame.font.Font("freesansbold.ttf", 40)
small_font = pygame.font.Font("freesansbold.ttf", 12)
med_font = pygame.font.Font("freesansbold.ttf", 25)
help_font = pygame.font.Font("freesansbold.ttf", 18)
title_font = pygame.font.Font("lhandw.ttf", 55)  # lucinda handwriting

score = 0


class Draw(object):
    def __init__(self):
        self.circleX = 150
        self.circleY = 300
        self.radius = 20
        self.wallWidth = 50
        self.wallX = win_width - self.wallWidth
        self.twall_height = 0
        self.bwall_height = 0
        self.wallX_speed = 2
        self.bwallY = 0

    def circle(self):
        pygame.draw.circle(win, c_yellow, (self.circleX, self.circleY), self.radius)

    def walls(self, space):
        if self.wallX < 0-self.wallWidth:
            self.twall_height = 0
            self.bwall_height = 0
            self.wallX = win_width
        if self.twall_height == 0 and self.bwall_height == 0:
            self.twall_height = random.randint(self.radius*space, win_height - (2*self.radius*space))
            self.bwall_height = win_height - self.twall_height - self.radius*space
        # top wall
        pygame.draw.rect(win, c_green, (self.wallX, 0, self.wallWidth, self.twall_height))
        # bottom wall
        self.bwallY = self.twall_height+(2*self.radius*space)
        pygame.draw.rect(win, c_green, (self.wallX, self.bwallY,
                                        self.wallWidth, self.bwall_height))

        # wall movement
        self.wallX -= self.wallX_speed

    def button(self, colour, x, y, width, height):
        pygame.draw.rect(win, colour, (x, y, width, height))


draw = Draw()


class Physics(object):
    def __init__(self):
        self.ballY_change = 0
        self.acceleration = 0.35
        self.ball_terminal_velocity = 10
        self.jump_force = 7

    def jump(self):
        self.ballY_change = -self.jump_force

    def collision(self):
        global score
        if draw.circleY+draw.radius > win_height:
            draw.circleY = win_height-draw.radius
            game.over()
        elif draw.circleY-draw.radius < 0:
            draw.circleY = draw.radius
            game.over()
        elif draw.circleX in range(draw.wallX, draw.wallX+draw.wallWidth+1):
            if draw.circleY+draw.radius > draw.bwallY:
                game.over()
            elif draw.circleY-draw.radius < draw.twall_height:
                game.over()
            elif draw.circleX > draw.wallX:
                score += 0.04

    def gravity(self):
        if self.ballY_change < self.ball_terminal_velocity:
            self.ballY_change += self.acceleration
        draw.circleY += self.ballY_change


phy = Physics()


class Game(object):
    def __init__(self):
        self.difficulty = 0

    def difficulty_screen(self):
        select_difficulty = font.render("DIFFICULTY", True, c_white)
        easy = med_font.render("EASY", True, c_white)
        med = med_font.render("MEDIUM", True, c_white)
        hard = med_font.render("HARD", True, c_white)
        go = med_font.render("GO", True, c_white)
        help = help_font.render("HELP", True, c_white)
        title = title_font.render("Flappy Circle", True, c_black)

        cbutton_width = 120
        cbutton_height = 40
        ebutton_colour = c_darkBlue
        mbutton_colour = c_darkBlue
        hbutton_colour = c_darkBlue
        buttonY = 380

        while True:
            win.fill(c_blue)

            mouseX, mouseY = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if mouseX in range(521, 577) and mouseY in range(15, 46):
                        sg.popup_ok("Help text:", "Press [SPACE] to flap", "", "made by JS")
                    elif mouseX in range(66, 66+cbutton_width+1) and mouseY in range(
                            buttonY, buttonY+cbutton_height+1):
                        self.difficulty = 5
                    elif mouseX in range(238, 238+cbutton_width+1) and mouseY in range(
                            buttonY, buttonY+cbutton_height+1):
                        self.difficulty = 4
                    elif mouseX in range(410, 410+cbutton_width+1) and mouseY in range(
                            buttonY, buttonY+cbutton_height+1):
                        self.difficulty = 3
                    elif mouseX in range(268, 318+1) and mouseY in range(445, 475+1):
                        if self.difficulty != 0:
                            self.play()

            if self.difficulty == 5:
                ebutton_colour = c_darkGreen
                mbutton_colour = c_darkBlue
                hbutton_colour = c_darkBlue
            elif self.difficulty == 4:
                mbutton_colour = c_darkGreen
                ebutton_colour = c_darkBlue
                hbutton_colour = c_darkBlue
            elif self.difficulty == 3:
                hbutton_colour = c_darkGreen
                mbutton_colour = c_darkBlue
                ebutton_colour = c_darkBlue

            pygame.draw.circle(win, c_yellow, (300, 150), 120)

            draw.button(ebutton_colour, 66, buttonY, cbutton_width, cbutton_height)
            draw.button(mbutton_colour, 238, buttonY, cbutton_width, cbutton_height)
            draw.button(hbutton_colour, 410, buttonY, cbutton_width, cbutton_height)
            draw.button(c_darkBlue, 268.5, 445, 50, 30)
            draw.button(c_darkBlue, 521, 15, 55, 30)

            win.blit(select_difficulty, (180, 300))
            win.blit(easy, (92, 390))
            win.blit(med, (248, 390))
            win.blit(hard, (435, 390))
            win.blit(go, (275, 450))
            win.blit(title, (100, 120))
            win.blit(help, (525, 22.5))

            pygame.display.update()

    def over(self):
        global score
        game_over = font.render("GAME OVER", True, c_white)
        retry = small_font.render("Press [R] to retry", True, c_white)

        while True:
            show_score = font.render(f"Score: {int(score)}", True, c_white)
            win.fill(c_blue)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        draw.circleX, draw.circleY = 150, 300
                        draw.twall_height, draw.bwall_height = 0, 0
                        draw.wallX = win_width - draw.wallWidth
                        phy.ballY_change = 0
                        score = 0
                        game.play()

            draw.circle()
            draw.wallX += draw.wallX_speed  # to stop wall from moving
            draw.walls(self.difficulty)

            win.blit(game_over, (170, 275))
            win.blit(retry, (245, 320))
            win.blit(show_score, (220, 25))

            pygame.display.update()
            clock.tick(60)

    def play(self):
        while True:
            show_score = font.render(f"Score: {int(score)}", True, c_white)
            win.fill(c_blue)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        phy.jump()

            draw.circle()
            draw.walls(self.difficulty)

            phy.gravity()
            phy.collision()

            win.blit(show_score, (220, 25))

            pygame.display.update()
            clock.tick(60)


game = Game()
game.difficulty_screen()
