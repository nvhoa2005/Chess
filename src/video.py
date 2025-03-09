import cv2
import numpy as np
from const import *
import pygame

class Video:
    
    def __init__(self, path):
        self.path = path
        self.video = cv2.VideoCapture(path)
        self.clock = pygame.time.Clock()
        
    def play(self, screen):
        self.clock.tick(FPS)
        
        # Đọc frame từ video
        ret, frame = self.video.read()
        
        # Nếu video hết, chạy lại từ đầu
        if not ret:
            self.video.set(cv2.CAP_PROP_POS_FRAMES, 0)
            ret, frame = self.video.read()
            
        # Chuyển đổi frame từ OpenCV (BGR) sang Pygame (RGB)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # Resize khớp với màn hình
        frame = cv2.resize(frame, (WIDTH, HEIGHT)) 
        # Xoay frame 90 độ nếu bị lật ngược
        frame = np.rot90(frame) 
        # Chuyển thành Surface của Pygame
        frame = pygame.surfarray.make_surface(frame) 
        # Hiển thị frame lên màn hình
        screen.blit(frame, (0, 0))