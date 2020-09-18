import pygame


class Car(pygame.sprite.Sprite):
    """docstring for Car"""

    def __init__(self, speed = 0, angle = 0, engine_state = True):
        super().__init__()
        if speed > 11 :
            speed = 11
        elif speed < -11 :
            speed = -11
        self.speed = speed

        if angle > 45 :
            angle = 45
        elif angle < -45 :
            angle = -45
        self.angle = angle

        self.engine_state = engine_state


    def get_speed(self):
        return self.speed

    def get_angle(self):
        return self.angle

    def get_engine_state(self):
        return self.engine_state

    def set_speed(self, speed):
        if speed > 11 :
            speed = 11
        elif speed < -11 :
            speed = -11
        self.speed = speed

    def set_angle(self, angle):
        if angle > 45 :
            angle = 45
        elif angle < -45 :
            angle = -45
        self.angle = angle


    def reset_speed(self):
        self.speed = 0

    def reset_angle(self):
        self.angle = 0


    def change_engine_state(self):
        self.engine_state = not self.engine_state

