import pygame


class Motor(pygame.sprite.Sprite):
    """docstring for Car"""

    def __init__(self, speed = 0, engine_state = True):
        super().__init__()
        if speed > 11 :
            speed = 11
        if speed < -11 :
            speed = -11
        self.speed = speed
        self.engine_state = engine_state

    def get_speed(self):
        return self.speed

    def get_engine_state(self):
        return self.engine_state

    def set_speed(self, speed):
        if speed > 11 :
            speed = 11
        if speed < -11 :
            speed = -11
        self.speed = speed

    def reset_speed(self):
        self.speed = 0

    def change_engine_state(self):
        self.engine_state = not self.engine_state


class Steering(pygame.sprite.Sprite):

    def __init__(self, angle = 0, steering_state = True):
        super().__init__()
        if angle > 45 :
            angle = 45
        if angle < -45 :
            angle = -45
        self.angle = angle
        self.steering_state = steering_state

    def get_angle(self):
        return self.angle

    def get_steering_state(self):
        return self.steering_state

    def set_angle(self, angle):
        if angle > 45 :
            angle = 45
        if angle < -45 :
            angle = -45
        self.angle = angle

    def reset_angle(self):
        self.angle = 0

    def change_steering_state(self):
        self.steering_state = not self.steering_state