from core.UI.BaseUI import BaseUI
from core.textures.Tileset import TileSet
from core.textures.load_image import load_image
from random import randrange, choice, random
from math import cos, sin, pi


class TorchSpike(BaseUI):
    def __init__(self, window, pos):
        super().__init__(window, pos, image=load_image('TorchSpark'))
        # direction horizontal
        self.ang = choice([0, 3*pi/4, pi/2, pi/4, pi])
        # const speed
        self.ver_speed = randrange(57, 60)
        self.hor_speed = randrange(15, 25)
        self.ang_speed = 3.14
        # const acceleration
        self.deceleration = 3

    def draw(self, pos=(0, 0)):
        pos = [self.pos[0] + pos[0], self.pos[1] + pos[1]]
        self.window.game.screen.blit(self.image, pos)

    def fixed_update(self):
        self.pos[1] -= self.ver_speed * self.window.game.delta
        self.pos[0] += self.hor_speed * cos(self.ang) * self.window.game.delta
        self.ang += self.ang_speed * self.window.game.delta
        self.ver_speed -= self.deceleration * self.window.game.delta
        if self.ver_speed < 52:
            self.parent.remove_child(self)


class AnimatedTorch(BaseUI):
    def __init__(self, window, pos):
        super().__init__(window, pos, size=[0, 0])
        self.tile_set = TileSet("Torch", (100, 100))
        self.frame = 0
        self.timer = 0
        self.time_to_next_frame = 0.25
        self.count_spikes = 5
        self.spawn_delta = 0.5
        self.timer_spawn = 0
        self.spike_dist = 10

    def draw(self, pos=(0, 0)):
        self.window.game.screen.blit(self.tile_set[self.frame], self.pos)

        for spike in self.child:
            spike.draw(self.pos)

    def fixed_update(self):
        self.timer += self.window.game.delta
        if self.timer > self.time_to_next_frame:
            self.timer = 0
            self.frame += 1
            if self.frame > 3:
                self.frame = 0

        if self.timer_spawn > 0:
            self.timer_spawn -= self.window.game.delta

        if len(self.child) < self.count_spikes and self.timer_spawn <= 0:
            ang = random() * pi
            self.add_child(TorchSpike(self.window, [self.spike_dist * cos(ang) + 48, self.spike_dist * -sin(ang) + 40]))
            self.timer_spawn = self.spawn_delta

        for spike in self.child:
            spike.fixed_update()
