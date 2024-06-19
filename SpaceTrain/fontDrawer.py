import pygame

class FontDrawer:

    def __init__(self, img):
        self.sheet = img

    def draw(self, window, text, x, y, size):
        sprite = pygame.Surface([6 * len(text), 7])

        for i in range(len(text)):
            if text.lower()[i] == ' ':
                continue
            index = self.CHARS[text.lower()[i]]
            sprite.blit(self.sheet, (i * 6, 0), (index * 5, 0, 5, 7))
        
        sprite.set_colorkey((0, 0, 0))   
        sprite = pygame.transform.scale(sprite, (len(text) * ((6 * size) / 7), size))
        window.blit(sprite, (x, y))

    CHARS = {
        'a': 0,
        'b': 1,
        'c': 2,
        'd': 3,
        'e': 4,
        'f': 5,
        'g': 6,
        'h': 7,
        'i': 8,
        'j': 9,
        'k': 10,
        'l': 11,
        'm': 12,
        'n': 13,
        'o': 14,
        'p': 15,
        'q': 16,
        'r': 17,
        's': 18,
        't': 19,
        'u': 20,
        'v': 21,
        'w': 22,
        'x': 23,
        'y': 24,
        'z': 25,
        '0': 26,
        '1': 27,
        '2': 28,
        '3': 29,
        '4': 30,
        '5': 31,
        '6': 32,
        '7': 33,
        '8': 34,
        '9': 35,
        '?': 36,
        '-': 37,
        ':': 38
    }