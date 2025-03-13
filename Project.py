import pygame
from math import sqrt
from Circles import Circles
from Bonds import Bonds
from Params import *
from pygame.display import update as update_display

pygame.init()
display = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
Circles = Circles()
Bonds = Bonds()

def draw_line(color, start, end, width):
    pygame.draw.line(display, color, start, end, width)

# draw_line = lambda color, start, end, width: pygame.draw.line(display, color, start, end, width)

running = True
dynamic_mode = 0

mouse_state = 0, 0
space_state = 0
old_space_state = 0

lmb_pressed = 0
rmb_pressed = 0


lmb_hold = 0
rmb_hold = 0

lmb_released = 0
rmb_released = 0

x_delta = 0
y_delta = 0

bond_color = None

while running:
    pygame.time.delay(FRAME_DELAY)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    display.fill(BLACK)

    Contacted = None
    Uncontacted = []

    mouse_x, mouse_y = pygame.mouse.get_pos()

    old_mouse_state = mouse_state
    mouse_state = pygame.mouse.get_pressed()[0:3:2]

    lmb_pressed = mouse_state[0] > old_mouse_state[0]
    rmb_pressed = mouse_state[1] > old_mouse_state[1]

    lmb_released = mouse_state[0] < old_mouse_state[0]
    rmb_released = mouse_state[1] < old_mouse_state[1]

    for circle in Circles.list():
        coords = circle.get_coords()
        if sqrt((coords[0] - mouse_x) ** 2 + (coords[1] - mouse_y) ** 2) < CIRCLE_RADIUS:
            circle.set_state('Under_Cursor')
            Contacted = circle
            break
        else:
            circle.set_state('None')

    # if Contacted is not None:
    #     for bond in Bonds.list():

    if rmb_pressed:
        if Contacted is None:
            Circles.add(display, mouse_x, mouse_y)
        else:
            circle_coords = Contacted.get_coords()
            Connectable = None
            while not rmb_released:
                pygame.time.delay(FRAME_DELAY)

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                display.fill(BLACK)
                mouse_x, mouse_y = pygame.mouse.get_pos()

                Connectable = None

                for circle in Circles.list():
                    coords = circle.get_coords()
                    if sqrt((coords[0] - mouse_x) ** 2 + (coords[1] - mouse_y) ** 2) < 20 and circle != Contacted:
                        circle.set_state('Under_Cursor')
                        Connectable = circle
                        mouse_x, mouse_y = circle.get_coords()
                        bond_color = BOND_COLOR_2
                        break
                    else:
                        circle.set_state('None')
                        bond_color = BOND_COLOR_1

                old_mouse_state = mouse_state
                mouse_state = pygame.mouse.get_pressed()[0:3:2]
                rmb_released = mouse_state[1] < old_mouse_state[1]

                draw_line(BOND_OUTLINE_COLOR_2, circle_coords, (mouse_x, mouse_y), BOND_OUTLINE_WIDTH_2)
                draw_line(BOND_OUTLINE_COLOR_1, circle_coords, (mouse_x, mouse_y), BOND_OUTLINE_WIDTH_1)
                draw_line(bond_color, circle_coords, (mouse_x, mouse_y), BOND_WIDTH)

                Bonds.render()
                Circles.render()

                update_display()

            if Connectable is not None:
                Contacted.neighbors += [Connectable]
                Connectable.neighbors += [Contacted]
                Bonds.add(display, Contacted, Connectable)

    elif lmb_pressed:
        if Contacted is not None:
            Contacted.set_state('Captured')
            coords_x, coords_y = Contacted.get_coords()
            x_delta = mouse_x - coords_x
            y_delta = mouse_y - coords_y
            while not lmb_released:
                pygame.time.delay(FRAME_DELAY)

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                display.fill(BLACK)
                mouse_x, mouse_y = pygame.mouse.get_pos()

                old_mouse_state = mouse_state
                mouse_state = pygame.mouse.get_pressed()[0:3:2]
                lmb_released = mouse_state[0] < old_mouse_state[0]

                Contacted.set_coords(mouse_x - x_delta, mouse_y - y_delta)

                Bonds.render()
                Circles.render()

                update_display()
            Contacted.set_state('Under_Cursor')

    keys = pygame.key.get_pressed()
    space_state = keys[pygame.K_SPACE]
    dynamic_mode = space_state > old_space_state
    old_space_state = space_state

    while dynamic_mode and running:
        pygame.time.delay(FRAME_DELAY)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        display.fill(GRAY)

        Contacted = None

        keys = pygame.key.get_pressed()
        space_state = keys[pygame.K_SPACE]
        dynamic_mode = 0 if space_state > old_space_state else 1
        old_space_state = space_state

        old_mouse_state = mouse_state
        mouse_state = pygame.mouse.get_pressed()[0:3:2]
        lmb_pressed = mouse_state[0] > old_mouse_state[0]
        mouse_x, mouse_y = pygame.mouse.get_pos()
        for circle in Circles.list():
            coords = circle.get_coords()
            if pifagor_of4(coords[0], coords[1], mouse_x, mouse_y) < CIRCLE_RADIUS:
                circle.set_state('Under_Cursor')
                Contacted = circle
                break
            else:
                circle.set_state('None')
        if lmb_pressed:
            if Contacted is not None:
                Contacted.set_state('Captured')
                coords_x, coords_y = Contacted.get_coords()
                x_delta = mouse_x - coords_x
                y_delta = mouse_y - coords_y
                while not lmb_released and running:
                    pygame.time.delay(FRAME_DELAY)

                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            running = False
                    display.fill(GRAY)
                    mouse_x, mouse_y = pygame.mouse.get_pos()

                    old_mouse_state = mouse_state
                    mouse_state = pygame.mouse.get_pressed()[0:3:2]
                    lmb_released = mouse_state[0] < old_mouse_state[0]

                    Contacted.move(mouse_x - x_delta, mouse_y - y_delta)

                    for circle in Circles.list():
                        x, y = circle.x, circle.y
                        X, Y = circle.X, circle.Y
                        Neighbors = circle.neighbors
                        point_delta_x = X - x
                        point_delta_y = Y - y
                        point_delta = pifagor_of2(point_delta_x, point_delta_y)
                        point_force = point_delta * 2 * POINT_FORCE_KOEF
                        force_x = point_force * point_delta_x
                        force_y = point_force * point_delta_y
                        for neighgbor in Neighbors:
                            neighgbor_X = neighgbor.X
                            neighgbor_Y = neighgbor.Y
                            neighgbor_x = neighgbor.x
                            neighgbor_y = neighgbor.y
                            delta_x = neighgbor_x - x
                            delta_y = neighgbor_y - y
                            length_0 = pifagor_of4(X, Y, neighgbor_X, neighgbor_Y)
                            length_1 = pifagor_of4(x, y, neighgbor_x, neighgbor_y)
                            force = ((length_1 - length_0) + abs(length_1 - length_0)) / 2 * BOND_FORCE_KOEF
                            # force = (length_1 - length_0) * BOND_FORCE_KOEF
                            force_x += force * delta_x
                            force_y += force * delta_y
                        circle.forces = force_x, force_y
                    for circle in Circles.list():
                        if circle != Contacted:
                            circle.x += circle.forces[0]
                            circle.y += circle.forces[1]

                    Bonds.render()
                    Circles.render()

                    update_display()
                lmb_pressed = 0
                rmb_pressed = 0
                lmb_released = 0
                rmb_released = 0
                Contacted.set_state('Under_Cursor')

        for circle in Circles.list():
            x, y = circle.x, circle.y
            X, Y = circle.X, circle.Y
            Neighbors = circle.neighbors
            point_delta_x = X - x
            point_delta_y = Y - y
            point_delta = pifagor_of2(point_delta_x, point_delta_y)
            point_force = point_delta * 2 * POINT_FORCE_KOEF
            force_x = point_force * point_delta_x
            force_y = point_force * point_delta_y
            for neighgbor in Neighbors:
                neighgbor_X = neighgbor.X
                neighgbor_Y = neighgbor.Y
                neighgbor_x = neighgbor.x
                neighgbor_y = neighgbor.y
                delta_x = neighgbor_x - x
                delta_y = neighgbor_y - y
                length_0 = pifagor_of4(X, Y, neighgbor_X, neighgbor_Y)
                length_1 = pifagor_of2(delta_x, delta_y)
                force = ((length_1 - length_0) + abs(length_1 - length_0)) / 2 * BOND_FORCE_KOEF
                force_x += force * delta_x
                force_y += force * delta_y
            circle.forces = force_x, force_y

        for circle in Circles.list():
            circle.x += circle.forces[0]
            circle.y += circle.forces[1]

        Bonds.render()
        Circles.render()

        update_display()


    Bonds.render()
    Circles.render()

    lmb_pressed = 0
    rmb_pressed = 0
    lmb_released = 0
    rmb_released = 0
    update_display()
