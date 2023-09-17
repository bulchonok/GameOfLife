import pygame
import pygame_gui

from button import Button
from pygame_gui.elements import UIButton
from pygame_gui.windows import UIColourPickerDialog
from pygame_gui.elements import UITextEntryLine


def draw_blocks(rect):
    pygame.draw.rect(screen, block_Color, rect, 10)


def inc(values, center):
    arr = [1 for value in values if screen.get_at(value) == block_Color]
    counter = len(arr)
    return counter == 3 or (counter == 2 and screen.get_at(center) == block_Color)


def expand_blocks():
    newblocks = []
    for i in range(60):
        for k in range(25):
            x = i * 20 + 41
            y = k * 20 + 41
            if inc(
                    (
                            (x + 20, y + 20),
                            (x + 20, y),
                            (x, y + 20),
                            (x - 20, y - 20),
                            (x - 20, y),
                            (x, y - 20),
                            (x + 20, y - 20),
                            (x - 20, y + 20)
                    ),
                    (x, y)
            ):
                newblocks.append(pygame.Rect(i * 20 + 40, k * 20 + 40, 20, 20))
    return newblocks


def draw_text(text, font, x, y):
    img = font.render(text, True, (0, 0, 0))
    screen.blit(img, (x, y))


class Stage:
    def __init__(self):
        self.state = 'menu'

    def main_state(self):
        self.state = 'main'
        global expand, blocks, running, current_colour
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit(0)

            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                expand = not expand

            if event.type == CUSTOM and expand:
                blocks = expand_blocks()

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if x in range(600, 680) and y in range(600, 640):
                    expand = not expand
                xr = (x // 20) * 20
                yr = (y // 20) * 20

                if xr in range(20, 1240) and yr in range(20, 540):
                    rectang = pygame.Rect(xr, yr, 20, 20)
                    if rectang in blocks:
                        blocks.remove(rectang)
                    else:
                        blocks.append(rectang)

            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == menu2_button:
                    self.state = 'menu'
                elif event.ui_element == exit2_button:
                    exit(0)

            ui_manager.process_events(event)
        ui_manager.update(time_delta)

        screen.fill("grey")
        ui_manager.draw_ui(screen)

        for x in range(40, WINDOW_WIDTH - 40, blockSize):
            for y in range(40, WINDOW_HEIGHT - 180, blockSize):
                rect = pygame.Rect(x, y, blockSize, blockSize)
                pygame.draw.rect(screen, 'white', rect, 1)
        button = pygame.Rect(600, 600, 80, 40)
        pygame.draw.rect(screen, 'white', button, 2)

        if not expand:
            pygame.draw.polygon(screen, (100, 100, 100), ((630, 610), (650, 620), (630, 630)))
        else:
            pygame.draw.rect(screen, 'white', (630, 610, 5, 20))
            pygame.draw.rect(screen, 'white', (645, 610, 5, 20))
        for block in blocks:
            draw_blocks(block)
        if next_button.draw(screen):
            blocks = expand_blocks()
        if clear_button.draw(screen):
            blocks.clear()

        pygame.display.flip()

    def menu(self):
        self.state = 'menu'
        global running, current_colour
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit(0)
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == start_button:
                    self.state = 'main'
                if event.ui_element == settings_button:
                    self.state = 'settings'
                elif event.ui_element == exit_button:
                    exit(0)

            ui_manager.process_events(event)

        ui_manager.update(time_delta)
        screen.fill('grey')
        ui_manager.draw_ui(screen)
        pygame.display.flip()

    def settings(self):
        global block_Color, colour_picker, current_colour, text_entry, dT
        self.state = 'settings'
        global running
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame_gui.UI_BUTTON_PRESSED:

                if event.ui_element == menu_button:
                    self.state = 'menu'
                    try:
                        text_entry.kill()
                    except:
                        pass
                    try:
                        colour_picker.kill()
                    except:
                        pass

                if event.ui_element == colour_picker_button:
                    colour_picker = UIColourPickerDialog(pygame.Rect(160, 50, 420, 400),
                                                         ui_manager,
                                                         window_title="Change Colour...",
                                                         initial_colour=current_colour)
                    colour_picker_button.disable()
                if event.ui_element == change_speed_button:
                    text_entry = UITextEntryLine(pygame.Rect(160, 50, 100, 40),
                                                 ui_manager)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                text = text_entry.get_text()
                try:
                    speed_multiplier = float(text)
                    dT = 300 / speed_multiplier
                    pygame.time.set_timer(CUSTOM, int(dT))
                    change_speed_button.set_text('change speed {speed}'.format(speed=300 / dT))
                except:
                    text_entry.kill()
                    pygame.event.post(
                        pygame.event.Event(pygame_gui.UI_BUTTON_PRESSED, ui_element=change_speed_button))
                    return
                text_entry.kill()

            if event.type == pygame_gui.UI_COLOUR_PICKER_COLOUR_PICKED:
                block_Color = event.colour
            if event.type == pygame_gui.UI_WINDOW_CLOSE:
                colour_picker_button.enable()
                colour_picker = None

            ui_manager.process_events(event)

        ui_manager.update(time_delta)

        screen.fill('grey')

        ui_manager.draw_ui(screen)
        pygame.display.flip()


stage1 = Stage()
pygame.init()

expand = False
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
pygame.display.set_caption('Colour Picking App')
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

CUSTOM = pygame.USEREVENT + 2
dT = 300
pygame.time.set_timer(CUSTOM, dT)
blocks = list()
block_Color = (255, 0, 0, 255)
blockSize = 20

ui_manager = pygame_gui.UIManager((WINDOW_WIDTH, WINDOW_HEIGHT))

colour_picker_button = UIButton(relative_rect=pygame.Rect(-750, -600, 200, 50),
                                text='Pick Colour',
                                manager=ui_manager,
                                anchors={'left': 'right',
                                         'right': 'right',
                                         'top': 'bottom',
                                         'bottom': 'bottom'})
change_speed_button = UIButton(relative_rect=pygame.Rect(-750, -500, 200, 30),
                               text='change speed',
                               manager=ui_manager,
                               anchors={'left': 'right',
                                        'right': 'right',
                                        'top': 'bottom',
                                        'bottom': 'bottom'})
start_button = UIButton(relative_rect=pygame.Rect(-700, -600, 150, 30),
                        text='start',
                        manager=ui_manager,
                        anchors={'left': 'right',
                                 'right': 'right',
                                 'top': 'bottom',
                                 'bottom': 'bottom'})
settings_button = UIButton(relative_rect=pygame.Rect(-700, -550, 150, 30),
                           text='settings',
                           manager=ui_manager,
                           anchors={'left': 'right',
                                    'right': 'right',
                                    'top': 'bottom',
                                    'bottom': 'bottom'})
menu_button = UIButton(relative_rect=pygame.Rect(-700, -120, 150, 30),
                       text='menu',
                       manager=ui_manager,
                       anchors={'left': 'right',
                                'right': 'right',
                                'top': 'bottom',
                                'bottom': 'bottom'})
exit_button = UIButton(relative_rect=pygame.Rect(-700, -500, 150, 30),
                       text='exit',
                       manager=ui_manager,
                       anchors={'left': 'right',
                                'right': 'right',
                                'top': 'bottom',
                                'bottom': 'bottom'})
menu2_button = UIButton(relative_rect=pygame.Rect(200, -80, 150, 30),
                        text='menu',
                        manager=ui_manager,
                        anchors={'left': 'left',
                                 'right': 'left',
                                 'top': 'bottom',
                                 'bottom': 'bottom'})
exit2_button = UIButton(relative_rect=pygame.Rect(200, -100, 150, 30),
                        text='exit',
                        manager=ui_manager,
                        anchors={'left': 'left',
                                 'right': 'left',
                                 'top': 'bottom',
                                 'bottom': 'bottom'})

colour_picker = None
current_colour = pygame.Color(0, 0, 0)
picked_colour_surface = pygame.Surface((400, 400))
picked_colour_surface.fill(current_colour)

clock = pygame.time.Clock()

next_image = pygame.image.load('images/next.png').convert_alpha()
next_button = Button(700, 610, next_image, 0.2)

clear_image = pygame.image.load('images/clear.png').convert_alpha()
clear_button = Button(500, 610, clear_image, 0.2)


def disable_elements(*elements):
    for element in elements:
        element.hide()
        element.disable()


def enable_elements(*elements):
    for element in elements:
        element.show()
        element.enable()


while True:
    time_delta = clock.tick(60) / 1000
    if stage1.state == 'menu':
        disable_elements(exit2_button, colour_picker_button, change_speed_button, menu_button, menu2_button)
        enable_elements(settings_button, start_button, exit_button)
        stage1.menu()
    elif stage1.state == 'main':
        disable_elements(settings_button, start_button, exit_button, colour_picker_button, change_speed_button,
                         menu_button)
        enable_elements(exit2_button, menu2_button)
        stage1.main_state()
    elif stage1.state == 'settings':
        disable_elements(settings_button, start_button, exit_button, exit2_button, menu2_button)
        enable_elements(colour_picker_button, change_speed_button, menu_button)
        stage1.settings()

    clock.tick(60)
