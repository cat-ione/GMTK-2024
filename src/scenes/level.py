from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.core.game import Game

from src.sprites.blob import Blob, ParticleBlob, DragInducedBlob, BulletBlob, DragInducedAntiBlob
from src.core.glpg import Texture, Shader
from src.core.scene import Scene
from src.utils import Timer, Vec
from src.sprites.ink import Ink
import src.assets as assets

from math import cos, sin, exp2, pi, atan2, sqrt, degrees
from random import randint, uniform
import pygame

class Level(Scene):
    def __init__(self, game: Game) -> None:
        super().__init__(game)
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

        self.blob_shader = Shader(game.window, "assets/shaders/metaball.frag")
        surf = pygame.Surface(game.window.size, pygame.SRCALPHA)
        self.blob_texture = Texture(game.window, surf, self.blob_shader)

        self.blobs = []
        self.blob_count = 0
        self.orig_expand_speed = 0.03
        self.expand_speed = self.orig_expand_speed
        self.linear_radius = 4
        self.radius = exp2(self.linear_radius)
        self.main_blob = Blob(self, (400, 400), self.radius)
        self.blob_timer = Timer(lambda r: 6 / r if r < 80 else 2.5 / r, self.main_blob.radius)
        self.blob_timer.start()

        self.antiballs = []
        self.antiball_count = 0

        self.fractal_shader = Shader(game.window, "assets/shaders/fractal.frag")
        self.fractal_texture = Texture(game.window, assets.noise_image, self.fractal_shader)
        self.fractal_post_shader = Shader(game.window, "assets/shaders/fractal_post.frag")
        surf = pygame.Surface(game.window.size, pygame.SRCALPHA)
        self.fractal_post_texture = Texture(game.window, surf, self.fractal_post_shader)
        self.zoom = 0
        self.zoom_speed = 0

        self.bullet_timer = Timer(lambda r: 27 / r, self.main_blob.radius)
        self.bullet_timer.start()
        self.captured = False
        self.invulnerable_timer = Timer(lambda: 1.0)
        self.invulnerable_timer.start()

        self.texture: Texture = None

        self.win_end_timer = Timer(lambda: 3.0)
        self.lost_end_timer = Timer(lambda: 3.0)

    def update(self, dt: float) -> None:
        r = self.main_blob.radius
        for _ in range(self.blob_timer.ended_and_reset(r)):
            angle = uniform(0, 2 * pi)
            x, y = 400 + max(0, r - 20) * cos(angle), 400 + max(0, r - 20) * sin(angle)
            ParticleBlob(self, (x, y), (cos(angle + randint(-10, 10)), sin(angle + randint(-10, 10))), randint(2, 10))

        self.linear_radius += self.expand_speed * dt
        self.radius = exp2(self.linear_radius)
        self.main_blob.radius = self.radius / exp2(self.zoom)
        if self.linear_radius > 50:
            self.zoom_speed *= 0.9995
        elif self.linear_radius > 7.2:
            self.zoom_speed += (self.expand_speed - self.zoom_speed) * 0.02
        self.zoom += self.zoom_speed * dt

        self.summon_bullets()

        self.keep_out_of_main_blob()

        if self.main_blob.radius > 600:
            self.lost_end_timer.start()
        elif self.expand_speed <= 0:
            self.win_end_timer.start()

        self.blob_shader.send("u_metaballCount", self.blob_count)
        self.blob_shader.send("u_metaballs", [self.blobs[i].data if i < len(self.blobs) else (0, 0, 0) for i in range(400)])
        self.blob_shader.send("u_antiballCount", self.antiball_count)
        self.blob_shader.send("u_antiballs", [self.antiballs[i].data if i < len(self.antiballs) else (0, 0, 0) for i in range(100)])

        self.fractal_shader.send("u_zoom", self.zoom)

        self.sprite_manager.update(dt)

        if self.win_end_timer.ended():
            self.game.change_scene(levels[levels.index(self.__class__) + 1](self.game))
        if self.lost_end_timer.ended():
            self.game.change_scene(levels[levels.index(self.__class__)](self.game))

    def summon_bullets(self) -> None:
        if self.bullet_timer.ended_and_reset(self.main_blob.radius):
            angle = uniform(0, 2 * pi)
            BulletBlob(self, (cos(angle) * 600 + 400, sin(angle) * 600 + 400))

    def keep_out_of_main_blob(self) -> None:
        mpos = Vec(pygame.mouse.get_pos())
        if mpos.distance_to((400, 400)) < self.main_blob.radius and not self.captured:
            pygame.mouse.set_pos(mpos - (Vec(400, 400) - mpos) * 0.05)

    def draw(self, screen: pygame.Surface) -> None:
        self.fractal_post_texture.blit(self.fractal_texture, (0, 0))
        self.game.texture.blit(self.fractal_post_texture, (0, 0))
        if self.texture is not None:
            self.game.texture.blit(self.texture, (0, 0))
        self.game.texture.blit(self.blob_texture, (0, 0))

    def add_blob(self, blob: Blob) -> None:
        if blob.antiball:
            self.antiballs.append(blob)
            self.antiball_count += 1
        else:
            self.blobs.append(blob)
            self.blob_count += 1
        self.add(blob)

    def remove_blob(self, blob: Blob) -> None:
        if blob.antiball:
            self.antiballs.remove(blob)
            self.antiball_count -= 1
        else:
            self.blobs.remove(blob)
            self.blob_count -= 1
        self.remove(blob)

class Level1(Level):
    def __init__(self, game: Game) -> None:
        super().__init__(game)

        self.surface = pygame.Surface(game.window.size, pygame.SRCALPHA)
        self.texture = Texture(game.window, self.surface, Shader(game.window, "assets/shaders/ink.frag"))
        self.covered_angles = {i: 0 for i in range(-180, 180, 15)}
        self.angle_coverage = 0
        self.current_ink = None

    def update(self, dt: float) -> None:
        super().update(dt)
        if self.captured:
            if self.current_ink is not None and self.current_ink.drawing:
                self.remove(self.current_ink)
                self.current_ink = None
            return

        if self.game.events.get(pygame.MOUSEBUTTONDOWN):
            self.current_ink = Ink(self)
            self.add(self.current_ink)
        if all([val > self.angle_coverage // 24 for val in self.covered_angles.values()]):
            self.angle_coverage = sum(self.covered_angles.values())
            self.expand_speed = self.orig_expand_speed * 0.25 * (4 - self.angle_coverage // 24)

    def draw(self, screen: pygame.Surface) -> None:
        self.surface.fill((0, 0, 0, 0))
        self.sprite_manager.draw(self.surface)
        self.texture.update(self.surface)
        super().draw(screen)

class Level2(Level):
    def __init__(self, game: Game) -> None:
        super().__init__(game)

        self.dragging = False
        self.start_drag = Vec(0, 0)
        # list of blobs that was created by dragging
        # this does not include the main blob and other particle blobs
        self.drag_induced_blobs = []
        self.current_blob = None
        self.current_anti = None

    def update(self, dt: float) -> None:
        super().update(dt)
        if self.captured:
            self.dragging = False
            return

        mpos = Vec(pygame.mouse.get_pos())
        dist = sqrt((mpos.x - 400) ** 2 + (mpos.y - 400) ** 2)
        angle = degrees(atan2(mpos.y - 400, mpos.x - 400))

        anti_sum = sum([anti.radius if anti.radius > 10 else anti.radius / 2 for anti in self.antiballs])
        anti_sum -= sum([blob.radius if blob.radius > 10 else blob.radius / 2 for blob in self.drag_induced_blobs])
        if self.main_blob.radius + 5 - anti_sum * 0.3 < dist < self.main_blob.radius + 40 - anti_sum * 0.2:
            self.figure_out_angle(angle)

            if self.game.events.get(pygame.MOUSEBUTTONDOWN):
                self.dragging = True
                self.start_drag = Vec(mpos)
                self.current_blob = DragInducedBlob(self, mpos, 0)
                self.drag_induced_blobs.append(self.current_blob)
                self.current_anti = DragInducedAntiBlob(self, mpos, 0)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

        if self.game.events.get(pygame.MOUSEBUTTONUP):
            self.dragging = False
            if not (self.current_blob is None or self.current_anti is None):
                if self.current_blob.radius > self.current_anti.radius:
                    self.current_anti = None
                    self.expand_speed += self.current_blob.radius * 0.0001
                    self.current_blob.dragging = False
                else:
                    self.drag_induced_blobs.remove(self.current_blob)
                    self.current_blob = None
                    self.expand_speed -= self.current_anti.radius * 0.0001
                    self.current_anti.dragging = False

        if self.dragging:
            self.figure_out_angle(angle)

            dist1 = mpos.distance_to((400, 400))
            dist2 = self.start_drag.distance_to((400, 400))
            if dist1 < dist2: # drag in
                self.current_anti.radius = (dist2 - dist1) * 0.5
            elif dist1 > dist2: # drag out
                self.current_blob.radius = dist1 - dist2

    def keep_out_of_main_blob(self) -> None:
        # Don't keep out
        pass

    def figure_out_angle(self, angle: float) -> None:
        if angle < -157.5:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_SIZEWE)
        elif angle < -157.5 + 45:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_SIZENWSE)
        elif angle < -157.5 + 45 * 2:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_SIZENS)
        elif angle < -157.5 + 45 * 3:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_SIZENESW)
        elif angle < -157.5 + 45 * 4:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_SIZEWE)
        elif angle < -157.5 + 45 * 5:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_SIZENWSE)
        elif angle < -157.5 + 45 * 6:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_SIZENS)
        elif angle < -157.5 + 45 * 7:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_SIZENESW)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_SIZEWE)

class Level3(Level):
    def __init__(self, game: Game) -> None:
        super().__init__(game)
        print("Level 3")

    def update(self, dt: float) -> None:
        super().update(dt)

levels = [Level1, Level2, Level3]
