
import constant
from player import cop
from player import robber
from environment import make_environment
from decide_action import next_action
from calculation import calc
from decide_action import cop_simple_chase
from decide_action import robber_flee_complicatedly

import pygame
from pygame.locals import *
import sys


def draw_circle(screen, circle):
    pygame.draw.circle(screen, circle.get_color(), circle.get_position(), circle.get_radius(), 0)


def main():
    # animation
    pygame.init()
    screen = pygame.display.set_mode((constant.screen_size_x, constant.screen_size_y))
    pygame.display.set_caption("Cops and Robbers")
    # make first state.
    environment = make_environment.make_environment()
    cops_array = []
    robbers_array = []
    id = 1
    for i in range(constant.cops_number):
        cp = cop.Cop(environment, id)
        cops_array.append(cp)
        id += 1
    for i in range(constant.robbers_number):
        rob = robber.Robber(environment, id)
        robbers_array.append(rob)
        id += 1
    human_player = 0
    if constant.your_player == 'cop':
        cp = cop.Cop(environment, id)
        cops_array.append(cp)
        id += 1
        cp.set_human()
        human_player = cp
    elif constant.your_player == 'robber':
        rob = robber.Robber(environment, id)
        robbers_array.append(rob)
        id += 1
        rob.set_human()
        human_player = rob
    action_cop_class = cop_simple_chase.CopSimpleChase(environment)  # next_action.NextActionCop()
    action_robber_class = robber_flee_complicatedly.RobberFleeComp(environment, robbers_array)  # next_action.NextActionRobber()
    while True:
        # display the animation
        screen.fill((255, 255, 255, 8))  # background color
        environment.draw_environment(screen)
        for cp in cops_array:
            draw_circle(screen, cp.make_circle_me())
            draw_circle(screen, cp.make_eye_circle())
        for rob in robbers_array:
            draw_circle(screen, rob.make_circle_me())
            draw_circle(screen, rob.make_eye_circle())

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.update()
        # make state array. state has id, position, direction
        cops_state_array = []
        robbers_state_array = []
        for cp in cops_array:
            cops_state_array.append(cp.make_state())
        for rob in robbers_array:
            robbers_state_array.append(rob.make_state())
        # decide next action.move cops and robbers. and change to next state
        cops_action_array = action_cop_class.decide_next_action_cop(cops_state_array, robbers_state_array)
        robbers_action_array = action_robber_class.decide_next_action_robber(cops_state_array, robbers_state_array)
        for cp in cops_array:
            if not cp.human:
                for cp_action in cops_action_array:
                    if cp.id == cp_action[0]:
                        cp.move_cop(cp_action[1][0], cp_action[1][1], environment)
                        break
        for rob in robbers_array:
            if not rob.human:
                for rob_action in robbers_action_array:
                    if rob.id == rob_action[0]:
                        rob.move_robber(rob_action[1][0], rob_action[1][1], environment)
        if human_player != 0:
            # human play
            ratio_move = 0
            ratio_turn = 0
            if pygame.key.get_pressed()[K_s]:
                ratio_move = 0.5
            if pygame.key.get_pressed()[K_LEFT] and (pygame.key.get_pressed()[K_g] or pygame.key.get_pressed()[K_UP]):
                ratio_move = 0.5
                ratio_turn = -0.5
            elif pygame.key.get_pressed()[K_RIGHT] and (
                    pygame.key.get_pressed()[K_g] or pygame.key.get_pressed()[K_UP]):
                ratio_move = 0.5
                ratio_turn = 0.5
            elif pygame.key.get_pressed()[K_LEFT]:
                ratio_move = 0
                ratio_turn = -1
            elif pygame.key.get_pressed()[K_RIGHT]:
                ratio_move = 0
                ratio_turn = 1
            elif pygame.key.get_pressed()[K_g] or pygame.key.get_pressed()[K_UP]:
                # move to the direction.directionの方向に動く
                ratio_move = 1
                ratio_turn = 0
            if constant.your_player == 'cop':
                human_player.move_cop(ratio_move, ratio_turn, environment)
            elif constant.your_player == 'robber':
                human_player.move_robber(ratio_move, ratio_turn, environment)

        # check collision cops and robbers
        collision_robber_array = calc.collision_robbers_array(cops_array, robbers_array, environment)
        for rob in collision_robber_array:
            robbers_array.remove(rob)
            print("remove robber id = "+str(rob.id))


if __name__ == '__main__':
    main()
