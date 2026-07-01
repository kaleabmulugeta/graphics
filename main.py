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

BODY_NAMES = (
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
MIN_SCALE = 0.1
MAX_SCALE = 8.0
ORBIT_SEGMENTS = 100
STAR_RANGE = 1500
STAR_COUNT = 400

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

scales = {body: 1.0 for body in BODY_NAMES}

keys = {}

cam_x, cam_y, cam_z = 0.0, 320.0, 720.0
cam_speed = 12.0
cam_zoom_speed = 20.0

spins = {body: 0.0 for body in BODY_NAMES}
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
        random.randint(-STAR_RANGE, STAR_RANGE),
        random.randint(-STAR_RANGE, STAR_RANGE),
        random.randint(-STAR_RANGE, STAR_RANGE),
    )
    for _ in range(STAR_COUNT)
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
    for i in range(ORBIT_SEGMENTS):
        a = 2 * math.pi * i / ORBIT_SEGMENTS
        glVertex3f(radius * math.cos(a), 0, radius * math.sin(a))
    glEnd()


def orbit(r, a):
    return (r * math.cos(a), 0, r * math.sin(a))


def clamp_scale(value):
    return max(MIN_SCALE, min(MAX_SCALE, value))


def adjust_camera_zoom(direction):
    dx = cam_x * direction
    dy = cam_y * direction
    dz = cam_z * direction
    dist = math.sqrt(dx * dx + dy * dy + dz * dz) or 1.0
    return (
        cam_x + (dx / dist) * cam_zoom_speed,
        cam_y + (dy / dist) * cam_zoom_speed,
        cam_z + (dz / dist) * cam_zoom_speed,
    )


def draw_body(name, radius, color, scale_name=None, slices=20, stacks=20):
    scale_key = scale_name or name
    glColor3f(*color)
    glRotatef(spins[name] % 360, 0, 1, 0)
    glScalef(scales[scale_key], scales[scale_key], scales[scale_key])
    draw_sphere(radius, slices, stacks)


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
        time_speed = max(MIN_SCALE, time_speed - 0.7)

    if keys.get(pygame.K_n):
        planet_keys = list(scales.keys())
        idx = planet_keys.index(selected_planet)
        selected_planet = planet_keys[(idx + 1) % len(planet_keys)]
    if keys.get(pygame.K_PERIOD):
        scales[selected_planet] = clamp_scale(scales[selected_planet] + 0.4)
    if keys.get(pygame.K_COMMA):
        scales[selected_planet] = clamp_scale(scales[selected_planet] - 0.4)

    if keys.get(pygame.K_j):
        cam_x -= cam_speed
    if keys.get(pygame.K_l):
        cam_x += cam_speed
    if keys.get(pygame.K_u):
        cam_y += cam_speed
    if keys.get(pygame.K_o):
        cam_y -= cam_speed
    if keys.get(pygame.K_i):
        cam_x, cam_y, cam_z = adjust_camera_zoom(-1)
    if keys.get(pygame.K_k):
        cam_x, cam_y, cam_z = adjust_camera_zoom(1)

    for planet in scales:
        scales[planet] = clamp_scale(scales[planet])

    for p in spins:
        spins[p] += spin_speeds.get(p, 0.5) * time_speed

    angle += 0.01 * time_speed * time_direction

    glClear(int(GL_COLOR_BUFFER_BIT) | int(GL_DEPTH_BUFFER_BIT))
    glLoadIdentity()

    gluLookAt(cam_x, cam_y, cam_z, 0, 0, 0, 0, 1, 0)

    draw_stars()

    # Sun
    glPushMatrix()
    draw_body("sun", 25, (1, 1, 0))
    glPopMatrix()

    # Mercury
    draw_orbit(50)
    glPushMatrix()
    x, y, z = orbit(50, angle * 4)
    glTranslatef(x, y, z)
    draw_body("mercury", 4, (0.6, 0.6, 0.6))
    glPopMatrix()

    # Venus
    draw_orbit(80)
    glPushMatrix()
    x, y, z = orbit(80, angle * 3)
    glTranslatef(x, y, z)
    draw_body("venus", 6, (1, 0.6, 0.2))
    glPopMatrix()

    # Earth and Moon
    draw_orbit(120)
    glPushMatrix()

    ex, ey, ez = orbit(120, angle * 2)
    glTranslatef(ex, ey, ez)

    draw_body("earth", 6, (0, 0, 1))

    glPushMatrix()
    mx, my, mz = orbit(15, angle * 6)
    glTranslatef(mx, my, mz)
    draw_body("moon", 2, (0.8, 0.8, 0.8))
    glPopMatrix()

    glPopMatrix()
    # Mars and Moons
    draw_orbit(160)
    glPushMatrix()

    x, y, z = orbit(160, angle * 1.8)
    glTranslatef(x, y, z)

    draw_body("mars", 5, (1, 0, 0))

    glPushMatrix()
    px, py, pz = orbit(8, angle * 8)
    glTranslatef(px, py, pz)
    draw_body("phobos", 1.5, (0.6, 0.6, 0.6), slices=10, stacks=10)
    glPopMatrix()

    glPushMatrix()
    dx, dy, dz = orbit(12, angle * 5)
    glTranslatef(dx, dy, dz)
    draw_body("deimos", 1.5, (0.5, 0.5, 0.5), slices=10, stacks=10)
    glPopMatrix()

    glPopMatrix()

    # Jupiter and Moons
    draw_orbit(220)
    glPushMatrix()

    x, y, z = orbit(220, angle * 1.2)
    glTranslatef(x, y, z)

    draw_body("jupiter", 12, (0.9, 0.7, 0.4))

    moons = [
        (18, 1, 1, 0),
        (22, 0.9, 0.9, 0.9),
        (26, 0.6, 0.6, 0.6),
        (30, 0.4, 0.4, 0.4),
    ]
    speeds = [7, 6, 5, 4]

    for m in range(4):
        glPushMatrix()
        ox, oy, oz = orbit(moons[m][0], angle * speeds[m])
        glTranslatef(ox, oy, oz)
        glColor3f(moons[m][1], moons[m][2], moons[m][3])
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
    draw_body("saturn", 10, (1, 0.9, 0.6))
    glPopMatrix()

    # Uranus
    draw_orbit(340)
    glPushMatrix()
    x, y, z = orbit(340, angle * 0.8)
    glTranslatef(x, y, z)
    draw_body("uranus", 8, (0.6, 0.9, 1))
    glPopMatrix()

    # Neptune
    draw_orbit(400)
    glPushMatrix()
    x, y, z = orbit(400, angle * 0.6)
    glTranslatef(x, y, z)
    glDisable(GL_DEPTH_TEST)
    draw_body("neptune", 8, (0.2, 0.2, 1))
    glEnable(GL_DEPTH_TEST)
    glPopMatrix()

    pygame.display.flip()
    clock.tick(60)
