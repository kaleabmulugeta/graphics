import pygame
from OpenGL.GL import (
    glMatrixMode,
    glLoadIdentity,
    glEnable,
    glClearColor,
    glPointSize,
    glBegin,
    glColor3f,
    glVertex3f,
    glEnd,
    glClear,
    glPushMatrix,
    glPopMatrix,
    glTranslatef,
    glRotatef,
    glScalef,
    glDisable,
    glEnable,
    GL_POINTS,
    GL_LINE_LOOP,
    GL_PROJECTION,
    GL_MODELVIEW,
    GL_DEPTH_TEST,
    GL_QUADS,
    GL_COLOR_BUFFER_BIT,
    GL_DEPTH_BUFFER_BIT,
)
from OpenGL.GLU import gluPerspective, gluLookAt
from solar import draw_sphere
import math
import random

pygame.init()

display = (1800, 1200)
pygame.display.set_mode(display, pygame.DOUBLEBUF | pygame.OPENGL)

glMatrixMode(GL_PROJECTION)
glLoadIdentity()
gluPerspective(45, display[0] / display[1], 0.1, 3000)
glMatrixMode(GL_MODELVIEW)

glEnable(GL_DEPTH_TEST)
glClearColor(0, 0, 0, 1)

clock = pygame.time.Clock()

angle = 0
time_speed = 1.0
time_direction = 1

scales = {
    "sun": 1.0,
    "mercury": 1.0,
    "venus": 1.0,
    "earth": 1.0,
    "moon": 1.0,
    "mars": 1.0,
    "phobos": 1.0,
    "deimos": 1.0,
    "jupiter": 1.0,
    "saturn": 1.0,
    "uranus": 1.0,
    "neptune": 1.0,
}

keys = {}

cam_x, cam_y, cam_z = 0.0, 320.0, 720.0
cam_speed = 12.0
cam_zoom_speed = 20.0

spins = {
    p: 0.0
    for p in (
        "sun",
        "mercury",
        "venus",
        "earth",
        "moon",
        "mars",
        "phobos",
        "deimos",
        "jupiter",
        "saturn",
        "uranus",
        "neptune",
    )
}
spin_speeds = {
    "sun": 0.05,
    "mercury": 1.5,
    "venus": 0.4,
    "earth": 1.0,
    "moon": 2.0,
    "mars": 0.8,
    "phobos": 2.5,
    "deimos": 2.0,
    "jupiter": 0.3,
    "saturn": 0.25,
    "uranus": 0.2,
    "neptune": 0.18,
}

selected_planet = "earth"

stars = [
    (
        random.randint(-1500, 1500),
        random.randint(-1500, 1500),
        random.randint(-1500, 1500),
    )
    for _ in range(400)
]


def draw_stars():
    glPointSize(1)
    glBegin(GL_POINTS)
    glColor3f(1, 1, 1)
    for s in stars:
        glVertex3f(*s)
    glEnd()


def draw_orbit(radius):
    glBegin(GL_LINE_LOOP)
    glColor3f(0.2, 0.2, 0.5)
    for i in range(100):
        a = 2 * math.pi * i / 100
        glVertex3f(radius * math.cos(a), 0, radius * math.sin(a))
    glEnd()


def orbit(r, a):
    return (r * math.cos(a), 0, r * math.sin(a))


while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

        if event.type == pygame.KEYDOWN:
            keys[event.key] = True
            if event.key == pygame.K_r:
                time_direction *= -1
        if event.type == pygame.KEYUP:
            keys[event.key] = False

    if keys.get(pygame.K_UP):
        time_speed = min(5.0, time_speed + 0.7)
    if keys.get(pygame.K_DOWN):
        time_speed = max(0.1, time_speed - 0.7)

    if keys.get(pygame.K_n):
        planet_keys = list(scales.keys())
        idx = planet_keys.index(selected_planet)
        selected_planet = planet_keys[(idx + 1) % len(planet_keys)]
    if keys.get(pygame.K_PERIOD):
        scales[selected_planet] = min(8.0, scales[selected_planet] + 0.4)
    if keys.get(pygame.K_COMMA):
        scales[selected_planet] = max(0.1, scales[selected_planet] - 0.4)

    if keys.get(pygame.K_j):
        cam_x -= cam_speed
    if keys.get(pygame.K_l):
        cam_x += cam_speed
    if keys.get(pygame.K_u):
        cam_y += cam_speed
    if keys.get(pygame.K_o):
        cam_y -= cam_speed
    if keys.get(pygame.K_i):
        dx = -cam_x
        dy = -cam_y
        dz = -cam_z
        dist = math.sqrt(dx * dx + dy * dy + dz * dz) or 1.0
        cam_x += (dx / dist) * cam_zoom_speed
        cam_y += (dy / dist) * cam_zoom_speed
        cam_z += (dz / dist) * cam_zoom_speed
    if keys.get(pygame.K_k):
        dx = cam_x
        dy = cam_y
        dz = cam_z
        dist = math.sqrt(dx * dx + dy * dy + dz * dz) or 1.0
        cam_x += (dx / dist) * cam_zoom_speed
        cam_y += (dy / dist) * cam_zoom_speed
        cam_z += (dz / dist) * cam_zoom_speed

    for planet in scales:
        scales[planet] = max(0.1, min(8.0, scales[planet]))

    for p in spins:
        spins[p] += spin_speeds.get(p, 0.5) * time_speed

    angle += 0.01 * time_speed * time_direction

    glClear(int(GL_COLOR_BUFFER_BIT) | int(GL_DEPTH_BUFFER_BIT))
    glLoadIdentity()

    gluLookAt(cam_x, cam_y, cam_z, 0, 0, 0, 0, 1, 0)

    draw_stars()

    # Sun
    glPushMatrix()
    glColor3f(1, 1, 0)
    glRotatef(spins["sun"] % 360, 0, 1, 0)
    glScalef(scales["sun"], scales["sun"], scales["sun"])
    draw_sphere(25, 20, 20)
    glPopMatrix()

    # Mercury
    draw_orbit(50)
    glPushMatrix()
    x, y, z = orbit(50, angle * 4)
    glTranslatef(x, y, z)
    glColor3f(0.6, 0.6, 0.6)
    glRotatef(spins["mercury"] % 360, 0, 1, 0)
    glScalef(scales["mercury"], scales["mercury"], scales["mercury"])
    draw_sphere(4, 20, 20)
    glPopMatrix()

    # Venus
    draw_orbit(80)
    glPushMatrix()
    x, y, z = orbit(80, angle * 3)
    glTranslatef(x, y, z)
    glColor3f(1, 0.6, 0.2)
    glRotatef(spins["venus"] % 360, 0, 1, 0)
    glScalef(scales["venus"], scales["venus"], scales["venus"])
    draw_sphere(6, 20, 20)
    glPopMatrix()

    # Earth and Moon
    draw_orbit(120)
    glPushMatrix()

    ex, ey, ez = orbit(120, angle * 2)
    glTranslatef(ex, ey, ez)

    glColor3f(0, 0, 1)
    glRotatef(spins["earth"] % 360, 0, 1, 0)
    glScalef(scales["earth"], scales["earth"], scales["earth"])
    draw_sphere(6, 20, 20)

    glPushMatrix()
    mx, my, mz = orbit(15, angle * 6)
    glTranslatef(mx, my, mz)
    glColor3f(0.8, 0.8, 0.8)
    glRotatef(spins["moon"] % 360, 0, 1, 0)
    glScalef(scales["moon"], scales["moon"], scales["moon"])
    draw_sphere(2, 20, 20)
    glPopMatrix()

    glPopMatrix()
    # Mars and Moons
    draw_orbit(160)
    glPushMatrix()

    x, y, z = orbit(160, angle * 1.8)
    glTranslatef(x, y, z)

    glColor3f(1, 0, 0)
    glRotatef(spins["mars"] % 360, 0, 1, 0)
    glScalef(scales["mars"], scales["mars"], scales["mars"])
    draw_sphere(5, 20, 20)

    glPushMatrix()
    px, py, pz = orbit(8, angle * 8)
    glTranslatef(px, py, pz)
    glColor3f(0.6, 0.6, 0.6)
    glRotatef(spins["phobos"] % 360, 0, 1, 0)
    glScalef(scales["phobos"], scales["phobos"], scales["phobos"])
    draw_sphere(1.5, 10, 10)
    glPopMatrix()

    glPushMatrix()
    dx, dy, dz = orbit(12, angle * 5)
    glTranslatef(dx, dy, dz)
    glColor3f(0.5, 0.5, 0.5)
    glRotatef(spins["deimos"] % 360, 0, 1, 0)
    glScalef(scales["deimos"], scales["deimos"], scales["deimos"])
    draw_sphere(1.5, 10, 10)
    glPopMatrix()

    glPopMatrix()

    # Jupiter and Moons
    draw_orbit(220)
    glPushMatrix()

    x, y, z = orbit(220, angle * 1.2)
    glTranslatef(x, y, z)

    glColor3f(0.9, 0.7, 0.4)
    glRotatef(spins["jupiter"] % 360, 0, 1, 0)
    glScalef(scales["jupiter"], scales["jupiter"], scales["jupiter"])
    draw_sphere(12, 20, 20)

    moons = [
        (18, 1, 1, 0),
        (22, 0.9, 0.9, 0.9),
        (26, 0.6, 0.6, 0.6),
        (30, 0.4, 0.4, 0.4),
    ]
    speeds = [7, 6, 5, 4]

    for i in range(4):
        glPushMatrix()
        ox, oy, oz = orbit(moons[i][0], angle * speeds[i])
        glTranslatef(ox, oy, oz)
        glColor3f(moons[i][1], moons[i][2], moons[i][3])
        glRotatef(spins["jupiter"] % 360, 0, 1, 0)
        glScalef(
            scales["jupiter"] * 0.2, scales["jupiter"] * 0.2, scales["jupiter"] * 0.2
        )
        draw_sphere(2, 10, 10)
        glPopMatrix()

    glPopMatrix()

    # Saturn
    draw_orbit(280)
    glPushMatrix()
    x, y, z = orbit(280, angle)
    glTranslatef(x, y, z)
    glColor3f(1, 0.9, 0.6)
    glRotatef(spins["saturn"] % 360, 0, 1, 0)
    glScalef(scales["saturn"], scales["saturn"], scales["saturn"])
    draw_sphere(10, 20, 20)
    glPopMatrix()

    # Uranus
    draw_orbit(340)
    glPushMatrix()
    x, y, z = orbit(340, angle * 0.8)
    glTranslatef(x, y, z)
    glColor3f(0.6, 0.9, 1)
    glRotatef(spins["uranus"] % 360, 0, 1, 0)
    glScalef(scales["uranus"], scales["uranus"], scales["uranus"])
    draw_sphere(8, 20, 20)
    glPopMatrix()

    # Neptune
    draw_orbit(400)
    glPushMatrix()
    x, y, z = orbit(400, angle * 0.6)
    glTranslatef(x, y, z)
    glColor3f(0.2, 0.2, 1)
    glDisable(GL_DEPTH_TEST)
    glRotatef(spins["neptune"] % 360, 0, 1, 0)
    glScalef(scales["neptune"], scales["neptune"], scales["neptune"])
    draw_sphere(8, 20, 20)
    glEnable(GL_DEPTH_TEST)
    glPopMatrix()

    pygame.display.flip()
    clock.tick(60)
