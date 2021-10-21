from re import split
import pygame


class Grid:
    def __init__(self):
        self.data = []
        self.file_content = None

        # init
        self._get_file_content()
        self._set_underlying_data()
        # self._print_grid()

    def _get_file_content(self) -> None:
        """ Open a text file and parse it to data """

        while True:
            # file_name = str(input("Enter your file name (only *.txt files allowed):\n"))
            file_name = str(input("Enter your file name:\n"))
            # file_name = "sample.txt"
            try:
                file = open('./' + file_name, 'r')
                read = file.read()
                file.close()
                read = split(r"\n", read)
                if file and len(read) == 9 or len(read[0]) == 9:
                    break
            except FileNotFoundError:
                print("there is no such file, please try again")

        self.file_content = read

        return

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

    def gui(self):
        pygame.init()
        run = True
        screen = pygame.display.set_mode(size=(900, 900), flags=0, depth=0, display=0, vsync=0)
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = false
            screen.fill((255, 255, 255))
            i = 0
            while i <= 900:
                pygame.draw.rect(screen, (0, 0, 0), (i, 0, 5, 900))
                pygame.draw.rect(screen, (0, 0, 0), (0, i, 900, 5))
                i += 100
            pygame.display.update()
        pygame.quit()

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

    def solve(self):
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
                    if self.solve():
                        return True

                    # int wasn't the good one
                    self.data[y][x] = 0

            return False


if __name__ == "__main__":
    sudoku = Grid()
    sudoku.solve()
    sudoku.gui()
