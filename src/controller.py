# https://gist.github.com/claymcleod/028386b860b75e4f5472


from math import copysign

import pygame
from rlbot.botmanager.bot_helper_process import BotHelperProcess
from rlbot.utils.structures.game_interface import GameInterface
from rlbot.utils.structures.bot_input_struct import PlayerInput
from rlbot.utils.logging_utils import get_logger


def deadzone(axis, transform=False):
    if transform:
        axis = (axis + 1) / 2
    return copysign(min(abs(axis), 1), axis) if abs(axis) >= 0.1 else 0


class Controller(BotHelperProcess):
    def __init__(self, agent_metadata_queue, quit_event, options):
        super().__init__(agent_metadata_queue, quit_event, options)

        # Controls.
        pygame.init()
        pygame.joystick.init()
        self.controller = pygame.joystick.Joystick(0)
        self.controller.init()
        self.axis_data = [0] * self.controller.get_numaxes()
        self.button_data = [False] * self.controller.get_numbuttons()

        # RLBot.
        self.index = options["index"]
        self.game_interface = GameInterface(get_logger(str(self.index)))

    def start(self):
        self.game_interface.load_interface()

        controls = PlayerInput()

        while not self.quit_event.is_set():
            for event in pygame.event.get():
                if event.type == pygame.JOYAXISMOTION:
                    self.axis_data[event.axis] = deadzone(
                        event.value, transform=event.axis > 3
                    )
                elif event.type == pygame.JOYBUTTONDOWN:
                    self.button_data[event.button] = True
                elif event.type == pygame.JOYBUTTONUP:
                    self.button_data[event.button] = False

            # Update controls.
            air_roll = self.button_data[0] or self.button_data[4]
            controls.throttle = self.axis_data[4] - self.axis_data[5]
            controls.steer = self.axis_data[0]
            controls.pitch = self.axis_data[1]
            controls.yaw = 0 if air_roll else self.axis_data[0]
            controls.roll = self.axis_data[0] if air_roll else 0
            controls.jump = self.button_data[1]
            controls.boost = self.button_data[2]
            controls.handbrake = self.button_data[4]
            self.game_interface.update_player_input(controls, self.index)
