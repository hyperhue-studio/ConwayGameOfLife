import sys, pygame
import tkinter as tk
from tkinter import filedialog
from conway import ConWay

root = tk.Tk()
root.withdraw()

size = width, height = 1000, 564
black = (0, 0, 0)
white = (255, 255, 255)
gray = (92, 92, 92)

def mouse_click(world: ConWay, mouse_x: int, mouse_y: int) -> None:
    x = int(mouse_x / 10)
    y = int(mouse_y / 10)
    if world.read(x, y) == world.LIVE:
        world.write(x, y, world.DEAD)
    else:
        world.write(x, y, world.LIVE)

def ensure_extension(filename, extension):
    """Ensure that the file has the correct extension."""
    if not filename.lower().endswith(extension):
        filename += extension
    return filename

def main():
    pygame.init()
    pygame.font.init()
    world = ConWay()

    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("CONWAY'S LIFE GAME")

    play = pygame.image.load("play.png")
    play = pygame.transform.scale(play, (44, 44))
    playrect = play.get_rect()
    playrect = playrect.move(404, 510)

    pause = pygame.image.load("pause.png")
    pause = pygame.transform.scale(pause, (44, 44))
    pauserect = pause.get_rect()
    pauserect = pauserect.move(468, 510)

    clear = pygame.image.load("clear.png")
    clear = pygame.transform.scale(clear, (44, 44))
    clearrect = clear.get_rect()
    clearrect = clearrect.move(532, 510)

    load = pygame.image.load("load.png")
    load = pygame.transform.scale(load, (44, 44))
    loadrect = load.get_rect()
    loadrect = loadrect.move(596, 510)

    save = pygame.image.load("save.png")
    save = pygame.transform.scale(save, (44, 44))
    saverect = save.get_rect()
    saverect = saverect.move(660, 510)

    myfont = pygame.font.SysFont('Lucida Console', 30)
    smallfont = pygame.font.SysFont('Lucida Console', 14)

    running = False
    mouse_held = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("END.")
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if y <= 500:
                    mouse_click(world, x, y)
                else:
                    if playrect.collidepoint(x, y):
                        running = True
                    if pauserect.collidepoint(x, y):
                        running = False
                    if clearrect.collidepoint(x, y):
                        world.reset()
                    if loadrect.collidepoint(x, y):
                        file_path_string = filedialog.askopenfilename(
                            filetypes=(
                                ("Conway GoL files", "*.cgl"),
                                ("All files", "*.*")
                            ))
                        if file_path_string != "":
                            world.load(file_path_string)
                    if saverect.collidepoint(x, y):
                        file_path_string = filedialog.asksaveasfilename(
                            defaultextension=".cgl",
                            filetypes=(
                                ("Conway GoL files", "*.cgl"),
                                ("All files", "*.*")
                            ))
                        if file_path_string != "":
                            file_path_string = ensure_extension(file_path_string, ".cgl")
                            world.save(file_path_string)

                mouse_held = True

            elif event.type == pygame.MOUSEBUTTONUP:
                mouse_held = False

            elif event.type == pygame.MOUSEMOTION and mouse_held:
                x, y = pygame.mouse.get_pos()
                if y <= 500:
                    mouse_click(world, x, y)

        if running:
            world.update()

        screen.fill(black)
        world.draw(screen)
        screen.blit(play, playrect)
        screen.blit(pause, pauserect)
        screen.blit(clear, clearrect)
        screen.blit(load, loadrect)
        screen.blit(save, saverect)

        textsurface = myfont.render("RUNNING" if running else "PAUSE", True, white)
        screen.blit(textsurface, (100, 516))

        iterations_label = smallfont.render("Iterations:", True, white)
        screen.blit(iterations_label, (750, 490))
        screen.blit(myfont.render(str(world.iterations), True, white), (750, 516))

        livecells_label = smallfont.render("Live Cells:", True, white)
        screen.blit(livecells_label, (850, 490))
        screen.blit(myfont.render(str(world.livecells), True, white), (850, 516))

        pygame.display.flip()

if __name__ == "__main__":
    main()