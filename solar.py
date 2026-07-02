from OpenGL.GL import glBegin, glEnd, glVertex3f, GL_QUADS
import math


def draw_sphere(radius, slices, stacks):

    for i in range(stacks):
        lat0 = math.pi * (-0.5 + i / stacks)
        lat1 = math.pi * (-0.5 + (i + 1) / stacks)

        sin0 = math.sin(lat0)
        cos0 = math.cos(lat0)

        sin1 = math.sin(lat1)
        cos1 = math.cos(lat1)

        glBegin(GL_QUADS)

        for j in range(slices):
            lon0 = 2 * math.pi * j / slices
            lon1 = 2 * math.pi * (j + 1) / slices

            x00 = cos0 * math.cos(lon0)
            z00 = cos0 * math.sin(lon0)

            x01 = cos0 * math.cos(lon1)
            z01 = cos0 * math.sin(lon1)

            x10 = cos1 * math.cos(lon1)
            z10 = cos1 * math.sin(lon1)

            x11 = cos1 * math.cos(lon0)
            z11 = cos1 * math.sin(lon0)

            glVertex3f(radius * x00, radius * sin0, radius * z00)
            glVertex3f(radius * x01, radius * sin0, radius * z01)
            glVertex3f(radius * x10, radius * sin1, radius * z10)
            glVertex3f(radius * x11, radius * sin1, radius * z11)

        glEnd()
