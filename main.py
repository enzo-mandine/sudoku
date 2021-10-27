import sys
import time
import pygame
from re import split


class MyGui:
    def __init__(self):
        pygame.init()

        self.run = True
        self.H = 900
        self.W = 900
        self.clock = pygame.time.Clock()

        self.data = None
        self.file_content = None

        self.font = pygame.font.SysFont('Roboto', 48)
        self.screen = pygame.display.set_mode(size=(self.H, self.W), flags=0, depth=0, display=0, vsync=0)
        self.solver = SudokuSolver()

        self.colors = {
            'black': (0, 0, 0),
            'red': (255, 0, 0),
            'white': (255, 255, 255),
            'light': (200, 200, 200)
        }

        self.color_active = self.colors['white']
        self.color_passive = self.colors['black']

    def draw_solve(self):
        while self.run:
            for event in pygame.event.get():
                self.close_event(event)
                self.return_event(event)

            self.screen.fill(self.colors['light'])
            i, j = 0, 0
            for y in range(9):
                for x in range(9):
                    res = str(self.data[y][x])
                    if self.file_content[y][x] == res:
                        self.screen.blit(self.font.render(res, True, self.colors['black']), (i + 40, j + 40))
                    else:
                        self.screen.blit(self.font.render(res, True, self.colors['red']), (i + 40, j + 40))
                    i += 100
                j += 100
                i = 0

            i = 0
            while i <= 900:
                if i == 0:
                    pass
                if i == 900:
                    pygame.draw.rect(self.screen, self.colors['black'], (0, i - 5, self.H, 5))
                    pygame.draw.rect(self.screen, self.colors['black'], (i - 5, 0, 5, self.W))
                else:
                    pygame.draw.rect(self.screen, self.colors['black'], (0, i, self.H, 5))
                    pygame.draw.rect(self.screen, self.colors['black'], (i, 0, 5, self.W))
                i += 100
            pygame.display.update()

        pygame.quit()

    def draw_input(self):
        user_text = ''

        notice_text = 'Enter your file name:'
        notice = self.font.render(notice_text, True, self.colors['black'])
        notice_width, notice_height = self.font.size(notice_text)

        input_rect = pygame.Rect(
            notice_width + 20,
            10,
            2,
            notice_height
        )

        active = False
        while self.run:
            for event in pygame.event.get():
                self.close_event(event)

                # if a mouse button is clicked
                if event.type == pygame.MOUSEBUTTONDOWN:
                    active = input_rect.collidepoint(event.pos)

                # if a key is pressed down
                if event.type == pygame.KEYDOWN:

                    # block enter key
                    if event.key == pygame.K_RETURN:
                        if self.solver._set_file_content(user_text):
                            self.solver._set_underlying_data()
                            self.solver._solve()

                            self.data = self.solver.data
                            self.file_content = self.solver.file_content
                            self.draw_solve()
                            # pygame.display.update()
                            return True
                        else:
                            self.draw_input()

                    # handle backspace
                    if event.key == pygame.K_BACKSPACE:
                        user_text = user_text[:-1]
                    else:
                        user_text += event.unicode

            # fill the background
            self.screen.fill(self.colors['light'])

            # define the color of the input if active or not
            input_color = self.color_active if active else self.color_passive

            # render the notice
            self.screen.blit(notice, (10, 10))

            # init text input surface
            text_surface = self.font.render(user_text, True, self.colors['black'])

            # render the input
            self.screen.blit(text_surface, (input_rect.x + 5, input_rect.y))

            # update part of the screen
            pygame.display.flip()

            # set the refresh rate
            self.clock.tick(60)

        pygame.quit()

    def close_event(self, event) -> None:
        try:
            if event.type == pygame.QUIT:
                self.run = False
                sys.exit()
        except AttributeError:
            return False

    def return_event(self, event) -> None:
        try:
            if event.key == pygame.K_ESCAPE:
                self.draw_input()
        except AttributeError:
            return False
        return True


class SudokuSolver:
    def __init__(self):
        self.data = []
        self.file_content = None

    def _set_file_content(self, file_name: str) -> None:
        """ Open a text file and parse it to data """

        file_name = file_name.lower()
        try:
            file = open('./' + file_name, 'r')
            read = file.read()
            file.close()
            read = split(r"\n", read)
        except FileNotFoundError:
            return False

        self.file_content = read

        return True

    def _set_underlying_data(self) -> None:
        """ From the file previously parsed, create the underlying data structure + blocks """

        for y in range(9):
            self.data.append([])
            data = list(self.file_content[y])
            for x in range(9):
                if data[x] == "_":
                    self.data[y].append(0)
                else:
                    self.data[y].append(int(data[x]))
        return

    def _print_grid(self) -> None:
        """ print the grid row by row """

        s = ''
        for i in range(9):
            for j in range(9):
                s += ''.join(str(self.data[i][j]))
                if j == 2 or j == 5:
                    s += '|'
                if j == 8:
                    s += '\n'
            if i == 2 or i == 5:
                s += '-----------\n'
        print(s)
        return

    def _get_empty_space(self) -> tuple or None:
        """ return a position of the first empty space found """

        for y in range(9):
            for x in range(9):
                if self.data[y][x] == 0:
                    return y, x
        return None

    def _is_valid(self, n: int, coord: tuple) -> bool:
        """ check row/col/box to validate the int injected """

        y, x = coord
        for i in range(9):
            # if self.data[i][x] == n and y != i:
            if self.data[i][x] == n:
                return False
            # if self.data[y][i] == n and x != i:
            if self.data[y][i] == n:
                return False

        # sub divide array by 3
        bx = x // 3
        by = y // 3

        # add + 3 to account for the lack of the last occurrence in for loops
        # y
        for i in range(by * 3, by * 3 + 3):
            # x
            for j in range(bx * 3, bx * 3 + 3):

                # if the selected number is in the box return False
                if self.data[i][j] == n and (i, j) != coord:
                    return False

        return True

    def _get_possible_nbr(self, pos: tuple) -> list:
        """ get all possible int for a given position """

        y, x = pos
        in_board = []
        for i in range(9):
            if self.data[y][i] not in in_board:
                in_board.append(self.data[y][i])

        # cols
        for i in range(9):
            if self.data[i][x] not in in_board:
                in_board.append(self.data[i][x])

        # box
        by = y // 3
        bx = x // 3

        for i in range(by * 3, by * 3 + 3):
            for j in range(bx * 3, bx * 3 + 3):
                if self.data[i][j] not in in_board:
                    in_board.append(self.data[i][j])

        return list({1, 2, 3, 4, 5, 6, 7, 8, 9} - set(in_board))

    def _solve(self):
        """ solve recursively the board """

        selected = self._get_empty_space()

        # if selected is Null we are done
        if not selected:
            # return self._print_grid()
            return True
        else:

            # else use those coord
            y, x = selected

            # attempt to put an int at this coord
            # for i in range(1, 10):
            for i in self._get_possible_nbr((y, x)):

                # if the int isn't in the row/col/box
                if self._is_valid(i, (y, x)):

                    # put the int in it
                    self.data[y][x] = i

                    # call recursively previous step
                    if self._solve():
                        return True

                    # int wasn't the good one
                    self.data[y][x] = 0

            return False


def main():
    pygame = MyGui()
    pygame.draw_input()


if __name__ == "__main__":
    main()
