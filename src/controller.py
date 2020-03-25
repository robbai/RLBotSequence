# https://gist.github.com/claymcleod/028386b860b75e4f5472


import pygame
from rlbot.botmanager.bot_helper_process import BotHelperProcess


class PS4Controller(BotHelperProcess):
    def __init__(self, agent_metadata_queue, quit_event, options):
        super().__init__(agent_metadata_queue, quit_event, options)

        pygame.init()
        pygame.joystick.init()
        self.controller = pygame.joystick.Joystick(0)
        self.controller.init()

        self.axis_data = {}
        self.button_data = {}
        for i in range(self.controller.get_numbuttons()):
            self.button_data[i] = False
        self.hat_data = {}
        for i in range(self.controller.get_numhats()):
            self.hat_data[i] = (0, 0)

    def start(self):
        while not self.quit_event.is_set():
            for event in pygame.event.get():
                if event.type == pygame.JOYAXISMOTION:
                    self.axis_data[event.axis] = round(event.value, 2)
                elif event.type == pygame.JOYBUTTONDOWN:
                    self.button_data[event.button] = True
                elif event.type == pygame.JOYBUTTONUP:
                    self.button_data[event.button] = False
                elif event.type == pygame.JOYHATMOTION:
                    self.hat_data[event.hat] = event.value

            print("\n".join([str(item) for item in [self.axis_data, self.button_data, self.hat_data]]))
