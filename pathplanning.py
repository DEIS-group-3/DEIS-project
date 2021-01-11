import math
import time

import pygame
import json
from easytello import tello

"""
For converting pixels to cm
"""
MAP_SIZE_COEFF = 0.514



pygame.init()
screen  = pygame.display.set_mode([560, 500])
screen.fill((255, 255, 255))
running = True


class Background(pygame.sprite.Sprite):
    def __init__(self, image, location, scale):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image)
        self.image = pygame.transform.rotozoom(self.image, 0, scale)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location

def get_dist_btw_pos(pos0, pos1):
    """
    Getting distance between current and previous position
    """
    x = abs(pos0[0] - pos1[0])
    y = abs(pos0[1] - pos1[1])
    dist_px = math.hypot(x, y)
    dist_cm = dist_px * MAP_SIZE_COEFF
    return int(dist_cm), int(dist_px)

def get_angle_btw_line(pos0, pos1, posref):
    """
    Get angle between two lines repsective to position between 'posref'
    NOTE: using dot product
    """
    ax = posref[0] - pos0[0]
    ay = posref[1] - pos0[1]
    bx = posref[0] - pos1[0]
    by = posref[1] - pos1[1]

    _dot = (ax * bx) + (ay * by)
    _magA = math.sqrt(ax**2 + ay**2)
    _magB = math.sqrt(bx**2 + by**2)
    _rad = math.acos(_dot / (_magA * _magB))

    angle = (_rad * 180)/math.pi

    return int(angle)


"""
Main Capturing Program
"""
#Load background image
bground = Background('Overhead.png', [0, 0], 1.0)
screen.blit(bground.image, bground.rect)

path_wp = []
index = 0
while running:
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            running = False
        elif i.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            path_wp.append(mouse_pos)
            if index > 0:
                pygame.draw.line(screen, (255, 0, 0), path_wp[index-1], mouse_pos, 2)
            index += 1
        else:
            pass
    pygame.display.update()

"""
Compute the waypoints
"""
path_wp.insert(0, (path_wp[0][0], path_wp[0][1] - 10))

path_dist_cm = []
path_dist_px = []
path_angle = []

for index in range(len(path_wp)):
    if index > 1:
        dist_cm, dist_px = get_dist_btw_pos(path_wp[index - 1], path_wp[index])
        path_dist_cm.append(dist_cm)
        path_dist_px.append(dist_px)

    if index > 0 and index < (len(path_wp) - 1):
        angle = get_angle_btw_line(path_wp[index - 1], path_wp[index + 1], path_wp[index])
        path_angle.append(angle)

#Print the info
print('path_wp: {}'.format(path_wp))
print('dist_cm: {}'.format(path_dist_cm))
print('dist_px: {}'.format(path_dist_px))
print('angle: {}'.format(path_angle))

"""
Save waypoints
"""
waypoints = []
for index in range(len(path_dist_cm)):
    waypoints.append({
        "dist_cm": path_dist_cm[index],
        "dist_px": path_dist_px[index],
        "angle": path_angle[index]
    })

#save to json file
f = open('waypoint.json','w+')
path_wp.pop(0)
json.dump({
    "wp": waypoints,
    "pos": path_wp
}, f, indent=4)
f.close()

my_drone = tello.Tello()
my_drone.streamon()
time.sleep(4)
print(my_drone.get_battery())
time.sleep(1)
my_drone.takeoff()
time.sleep(2)
my_drone.down(25)
time.sleep(2)
print(my_drone.get_height())
for i in range(len(path_dist_cm)):
    my_drone.forward(path_dist_cm[i])
    time.sleep(2)
    my_drone.cw(path_angle[i])
    time.sleep(2)

my_drone.land()
time.sleep(1)
my_drone.streamoff()


