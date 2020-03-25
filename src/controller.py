# https://gist.github.com/claymcleod/028386b860b75e4f5472


import pygame


class PS4Controller():
    def __init__(self):
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

    def listen(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.JOYAXISMOTION:
                    self.axis_data[event.axis] = round(event.value,2)
                elif event.type == pygame.JOYBUTTONDOWN:
                    self.button_data[event.button] = True
                elif event.type == pygame.JOYBUTTONUP:
                    self.button_data[event.button] = False
                elif event.type == pygame.JOYHATMOTION:
                    self.hat_data[event.hat] = event.value


if __name__ == "__main__":
    ps4 = PS4Controller()
    ps4.listen()
