import pygame

class ConWay:
    WIDTH = 100
    HEIGHT = 50
    LIVE = 1
    DEAD = 0
    __world = []
    __next = []
    __born = []
    __alive = []
    __iterations = 0

    # Default pattern format 23/3
    def __init__(self, pattern: str = "23/3"):
        self.reset()
        self.__alive = [int(v) for v in pattern.split("/")[0]]
        self.__born = [int(v) for v in pattern.split("/")[1]]

    @property
    def iterations(self) -> int:
        return self.__iterations

    @property
    def livecells(self) -> int:
        return self.__world.count(1)

    def reset(self):
        self.__iterations = 0
        self.__world = [0] * (self.WIDTH * self.HEIGHT)
        self.__next = [0] * (self.WIDTH * self.HEIGHT)

    def read(self, x: int, y: int) -> int:
        if x >= self.WIDTH:
            x -= self.WIDTH
        elif x < 0:
            x += self.WIDTH
        if y >= self.HEIGHT:
            y -= self.HEIGHT
        elif y < 0:
            y += self.HEIGHT
        return self.__world[(y * self.WIDTH) + x]

    def write(self, x: int, y: int, value: int) -> None:
        self.__world[(y * self.WIDTH) + x] = value

    def update(self) -> None:
        self.__iterations += 1
        for y in range(self.HEIGHT):
            for x in range(self.WIDTH):
                neighbors = [self.read(x + 1, y - 1),
                             self.read(x, y - 1),
                             self.read(x - 1, y - 1),
                             self.read(x + 1, y),
                             self.read(x - 1, y),
                             self.read(x - 1, y + 1),
                             self.read(x, y + 1),
                             self.read(x + 1, y + 1),]
                alive_count = neighbors.count(self.LIVE)
                current = self.read(x, y)
                if current == self.LIVE:
                    if alive_count not in self.__alive:
                        current = self.DEAD
                else:
                    if alive_count in self.__born:
                        current = self.LIVE

                self.__next[(y * self.WIDTH) + x] = current

        for i in range(self.WIDTH * self.HEIGHT):
            self.__world[i] = self.__next[i]

    def draw(self, context: pygame.Surface) -> None:
        for y in range(self.HEIGHT):
            for x in range(self.WIDTH):
                current = self.read(x, y)
                if current == self.LIVE:
                    pygame.draw.rect(surface=context, color=(255, 255, 255), rect=(x * 10, y * 10, 10, 10))
                else:
                    pygame.draw.lines(surface=context, color=(64, 64, 64), closed=True, points=(
                        (x * 10, y * 10),
                        ((x + 1) * 10, y * 10),
                        ((x + 1) * 10, (y + 1) * 10),
                        (x * 10, (y + 1) * 10)), width=1)

    def save(self, filename: str) -> None:
        with open(filename, mode="w", encoding="utf-8") as fp:
            fp.write(str(self.__world))

    def load(self, filename: str) -> None:
        with open(filename, mode="r", encoding="utf-8") as fp:
            data = fp.read()[1:-1]
            self.__world = [int(v) for v in data.split(",")]

