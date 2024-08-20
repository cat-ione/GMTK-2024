from src.exe import pathof

import pygame

def load_image(file: str, scale: int = 1) -> pygame.SurfaceType:
    return pygame.transform.scale_by(pygame.image.load(pathof(f"assets/images/{file}")).convert_alpha(), scale)

class SpriteSheet(list):
    def __init__(self, path: str, height: int, scale: int = 1) -> None:
        self.image = load_image(path, scale)
        for i in range(self.image.get_height() // height):
            self.append(self.image.subsurface((0, i * height, self.image.get_width(), height)))

pygame.display.set_mode((1, 1), pygame.NOFRAME)
pygame.font.init()

# Load images
noise_image = load_image("noise.png")

# Load fonts
fonts = [pygame.font.SysFont("bahnschrift", size) for size in range(0, 200)]

# Load sounds
pygame.mixer.pre_init(44100, -16, 2, 32)
pygame.init()
pygame.mixer.quit()
pygame.mixer.init(22050, -16, 2, 32)

pygame.mixer.music.load(pathof("assets/sounds/noise.mp3"))
pin_hit = pygame.mixer.Sound(pathof("assets/sounds/pin_hit.wav"))
dialogue = [
    None,
    pygame.mixer.Sound(pathof("assets/sounds/1.wav")),
    pygame.mixer.Sound(pathof("assets/sounds/2.wav")),
    pygame.mixer.Sound(pathof("assets/sounds/3.wav")),
    pygame.mixer.Sound(pathof("assets/sounds/4.wav")),
    pygame.mixer.Sound(pathof("assets/sounds/5.wav")),
    pygame.mixer.Sound(pathof("assets/sounds/6.wav")),
    None,
    pygame.mixer.Sound(pathof("assets/sounds/8.wav")),
    pygame.mixer.Sound(pathof("assets/sounds/9.wav")),
    None,
    pygame.mixer.Sound(pathof("assets/sounds/11.wav")),
]
win_sound = pygame.mixer.Sound(pathof("assets/sounds/win.wav"))
win_sound.set_volume(0.6)
pin_break = pygame.mixer.Sound(pathof("assets/sounds/pin_break.wav"))
pin_break.set_volume(0.8)

pygame.display.quit()
