import pygame

class Sound:

    def __init__(self, path):
        self.path = path
        self.sound = pygame.mixer.Sound(path)

    def play(self):
        pygame.mixer.Sound.play(self.sound)
        
    def load(self):
        pygame.mixer.music.set_volume(0.2)
        pygame.mixer.music.load(self.path)
        pygame.mixer.music.play(-1)
    
    def pause(self):
        pygame.mixer.music.pause()
        
    def unpause(self):
        pygame.mixer.music.unpause()