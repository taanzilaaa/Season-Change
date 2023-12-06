from OpenGL.GL import *
from OpenGL.GLUT import *
import random
import math

W_Width, W_Height = 500, 500

# Global variables for weather
speed = 0.5
weather = []
direction = 0
background_color = (0.0, 0.0, 0.0)
season = "winter"
pause = False

sun_x, sun_y = 50, W_Height - 50  # Fixed position for the sun

car_x = 100
car_y = 100
car_width = 60
car_height = 30
car_speed = 1


def circ_point(x, y, a, b):
    glVertex2f(a + x, b + y)
    glVertex2f(a + y, b + x)
    glVertex2f(a + y, b - x)
    glVertex2f(a + x, b - y)
    glVertex2f(a - x, b - y)
    glVertex2f(a - y, b - x)
    glVertex2f(a - y, b + x)
    glVertex2f(a - x, b + y)


def midCircle(radius, a, b):
    d = 1 - radius
    x = 0
    y = radius

    glBegin(GL_POINTS)

    circ_point(x, y, a, b)

    while x < y:
        if d < 0:
            d = d + 2 * x + 3
        else:
            d = d + 2 * x - 2 * y + 5
            y -= 1
        x += 1
        circ_point(x, y, a, b)

    glEnd()

def draw_car(x, y):
    glColor3f(1.0, 0.0, 0.0)  # Car color (red)

    # Car body
    glBegin(GL_QUADS)
    glVertex2f(x, y)
    glVertex2f(x + car_width, y)
    glVertex2f(x + car_width, y + car_height)
    glVertex2f(x, y + car_height)
    glEnd()

    # Wheels
    glColor4f(0.5, 0.5, 0.5, 1.0)  # Wheel color (black)

    wheel_rad = car_height / 4.0
    wheel_y = y - wheel_rad / 2.0

    for i in range(2):
        wheel_x = x + (i + 1) * car_width / 3.0
        glBegin(GL_POLYGON)
        for j in range(360):
            angle = math.radians(j)
            glVertex2f(wheel_x + wheel_rad * math.cos(angle), wheel_y + wheel_rad * math.sin(angle))
        glEnd()

    # Window
    glColor3f(0.8, 0.8, 1.0)  # Window color (light blue)
    window_width = car_width / 3.0
    window_height = car_height / 2.0
    window_x = x + car_width / 3.0
    window_y = y + car_height / 4.0

    glBegin(GL_QUADS)
    glVertex2f(window_x, window_y)
    glVertex2f(window_x + window_width, window_y)
    glVertex2f(window_x + window_width, window_y + window_height)
    glVertex2f(window_x, window_y + window_height)
    glEnd()


def draw_sun(radius):
    global sun_x, sun_y
    glColor3f(1.0, 1.0, 0.0)  # Sun color (yellow)
    glBegin(GL_POLYGON)
    for i in range(360):
        angle = math.radians(i)
        glVertex2f(sun_x + radius * math.cos(angle), sun_y + radius * math.sin(angle))
    glEnd()


def draw_snowflake(x, y):
    glColor3f(1.0, 1.0, 1.0)  # Snowflake color (white)
    glPointSize(6.0)

    for i in range(6):
        angle = i * (360 / 6)
        sx = 1 * math.cos(math.radians(angle))
        sy = 1 * math.sin(math.radians(angle))
        midCircle(5, int(x + sx), int(y + sy))


def draw_raindrop(x, y):
    glColor3f(0.0, 0.1, 0.1)  # Raindrop color
    glPointSize(10.0)
    draw_line(x, y, x, y - 15)


def draw_road():
    glColor3f(0.4, 0.4, 0.4)  # Road color (gray)
    glBegin(GL_QUADS)
    glVertex2f(0, 0)
    glVertex2f(W_Width, 0)
    glVertex2f(W_Width, W_Height / 4)
    glVertex2f(0, W_Height / 4)
    glEnd()

    # White line in the middle of the road
    glColor3f(1.0, 1.0, 1.0)  # White color
    line_width = 5.0
    line_length = 20.0
    gap = 10.0

    lines = int(W_Width / (line_length + gap))

    for i in range(lines):
        if i % 2 == 0:
            glBegin(GL_QUADS)
            glVertex2f(i * (line_length + gap), W_Height / 8 - line_width / 2)
            glVertex2f((i + 1) * line_length + i * gap, W_Height / 8 - line_width / 2)
            glVertex2f((i + 1) * line_length + i * gap, W_Height / 8 + line_width / 2)
            glVertex2f(i * (line_length + gap), W_Height / 8 + line_width / 2)
            glEnd()


def draw_line(x1, y1, x2, y2):
    glBegin(GL_LINES)
    glVertex2f(x1, y1)
    glVertex2f(x2, y2)
    glEnd()


def iterate():
    glViewport(0, 0, 500, 500)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, 500, 0.0, 500, 0.0, 1.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glClearColor(*background_color, 1.0)
    glMatrixMode(GL_MODELVIEW)
    iterate()
    draw_road()

    if season == "winter":
        glColor3f(0.0, 0.1, 0.1)  # Snowflake color
        for x, y in weather:
            draw_snowflake(x, y)

    elif season == "summer":
        draw_sun(30)

    elif season == "rainy":
        glColor3f(0.0, 0.1, 0.1)  # Raindrop color
        for x, y in weather:
            draw_raindrop(x, y)

    draw_car(car_x, car_y)

    glutSwapBuffers()


def animate():
    global weather

    new_weather = [(x, y - 5) for x, y in weather if y - 5 > 0]
    if season == "winter":
        new_weather.extend([(random.uniform(0, 500), 500) for _ in range(5)])  # Add new snowflakes at the top
    elif season == "summer":
        pass  # Sun is fixed, no new suns
    elif season == "rainy":
        new_weather.extend([(random.uniform(0, 500), 500) for _ in range(5)])  # Add new raindrops at the top

    weather = new_weather

    # Car movement
    global car_x
    if not pause:
        car_x += car_speed
        if car_x > W_Width:
            car_x = -car_width

    glutPostRedisplay()


def keyboardListener(key, x, y):
    global background_color, season, pause
    if key == b'w':
        season = "winter"
        background_color = (0.0, 0.0, 0.0)
    elif key == b'r':
        season = "rainy"
        background_color = (1.0, 1.0, 1.0)
    elif key == b's':
        season = "summer"
        background_color = (0.5, 1.0, 1.0)
    elif key == b' ':
        pause = not pause

    glutPostRedisplay()


def mouseListener(button, state, x, y):
    global car_speed
    if button == GLUT_LEFT_BUTTON:
        if state == GLUT_DOWN:
            car_speed -= 2 
    elif button == GLUT_RIGHT_BUTTON:
        if state == GLUT_DOWN:
            car_speed += 2  

    glutPostRedisplay()


def init():
    glClearColor(0, 0, 0, 0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()


glutInit()
glutInitWindowSize(W_Width, W_Height)
glutInitWindowPosition(0, 0)
glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGB)
glutCreateWindow(b"Seasons")
init()

glutDisplayFunc(display)
glutIdleFunc(animate)
glutKeyboardFunc(keyboardListener)
glutMouseFunc(mouseListener)

glutMainLoop()






