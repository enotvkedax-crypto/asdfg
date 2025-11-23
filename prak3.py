import os
import random
from datetime import datetime

statistics = "stats"
current_board = []
current_player = "X"
board_size = 3
game_mode = 1

def create_stats_directory():
    if not os.path.exists(statistics):
        os.makedirs(statistics)
        print(f"Создана директория {statistics} для статистики игр")

def save_result(result, size, mode):
    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    filename = f"{statistics}/game_results.txt"
    if mode == 2:
        mode_name = "Против робота"
    else:
        mode_name = "Друг против друга"
    try:
        with open(filename, "a", encoding="utf-8") as file:
            file.write(f"Дата: {time} | Размер: {size}x{size} | Режим: {mode_name} | Результат: {result}\n")
            print("Результат игры сохранен")
    except Exception as e:
        print(f"Ошибка при сохранении результата: {e}")

def get_board_size():
    while True:
        try:
            size = int(input("Введите размер игрового поля (не меньше 3): "))
            if size < 3:
                print("Размер поля должен быть не менее 3!")
            else:
                return size
        except ValueError:
            print("Ведите целое число")

def choose_game_mode():
    while True:
        print("\nВыберите режим игры:")
        print("1 - Игра против друга")
        print("2 - Игра против робота")
        try:
            choice = int(input("Ваш выбор (1 или 2): "))
            if choice in [1, 2]:
                return choice
            else:
                print("Введите число от 1 до 2")
        except ValueError:
            print("Введите число")

def create_board(size):
    board = []
    for i in range(size):
        row = []
        for j in range(size):
            row.append(' ')
        board.append(row)
    return board


def print_board(board):
    size = len(board)
    print("\n   " + "   ".join(str(i) for i in range(size)))
    for i in range(size):
        print(f"{i}  " + " | ".join(board[i]))
        if i < size - 1:
            print("  " + "---" * size)
    print()


def check_win(board):
    size = len(board)
    for row in board:
        if row[0] != ' ' and all(cell == row[0] for cell in row):
            return row[0]
    for column in range(size):
        column_cells = []
        for row in range(size):
            column_cells.append(board[row][column])
        if column_cells[0] != ' ' and all(cell == column_cells[0] for cell in column_cells):
            return column_cells[0]
    diagonal1 = []
    for i in range(size):
        diagonal1.append(board[i][i])
    if diagonal1[0] != ' ' and all(cell == diagonal1[0] for cell in diagonal1):
        return diagonal1[0]
    diagonal2 = []
    for i in range(size):
        diagonal2.append(board[i][size - 1 - i])
    if diagonal2[0] != ' ' and all(cell == diagonal2[0] for cell in diagonal2):
        return diagonal2[0]
    return None


def board_full(board):
    for row in board:
        if ' ' in row:
            return False
    return True


def player_mode(board, player):
    size = len(board)
    while True:
        try:
            print(f"Ход игрока {player}")
            row = int(input("Введите номер строки: "))
            column = int(input("Введите номер столбца: "))
            if 0 <= row < size and 0 <= column < size:
                if board[row][column] == ' ':
                    return row, column
                else:
                    print("Эта клетка уже занята. Выберите другую")
            else:
                print(f"Координаты должны быть от 0 до {size - 1}!")
        except ValueError:
            print("Введите числа")


def robot_mode(board):
    size = len(board)
    empty_cells = []
    for i in range(size):
        for j in range(size):
            if board[i][j] == ' ':
                empty_cells.append((i, j))
    return random.choice(empty_cells)


def first_player():
    players = ['X', 'O']
    return random.choice(players)


def play_single_game():
    global current_board, current_player, board_size, game_mode
    board_size = get_board_size()
    game_mode = choose_game_mode()
    current_player = first_player()
    print(f"\nПервым ходит игрок: {current_player}")
    current_board = create_board(board_size)
    game_over = False
    while not game_over:
        print_board(current_board)
        if game_mode == 2 and current_player == 'O':
            print("Робот делает ход...")
            row, column = robot_mode(current_board)
        else:
            row, column = player_mode(current_board, current_player)
        current_board[row][column] = current_player
        winner = check_win(current_board)
        if winner:
            print_board(current_board)
            print(f"Победил игрок {winner}!")
            result_text = f"Победил {winner}"
            save_result(result_text, board_size, game_mode)
            game_over = True
        elif board_full(current_board):
            print_board(current_board)
            print("Ничья!")
            save_result("Ничья", board_size, game_mode)
            game_over = True
        else:
            current_player = 'O' if current_player == 'X' else 'X'

def ask_play_again():
    while True:
        answer = input("\nХотите сыграть еще раз? (да/нет): ").lower()
        if answer in ['да', 'д', 'yes', 'y', '1']:
            return True
        elif answer in ['нет', 'н', 'no', 'n', '0']:
            return False
        else:
            print("Пожалуйста, введите 'да' или 'нет'")


def main():
    print("Игра крестики-нолики с сохранением статистики и разными режимами")
    create_stats_directory()
    while True:
        print("\n" + "=" * 40)
        play_single_game()
        if not ask_play_again():
            print("Спасибо за игру!")
            break

main()
