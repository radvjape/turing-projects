import random

def main():
    board = new_board()

    white_piece = get_white_piece() #get piece and place
    change_board(board, white_piece, "w") #print on the board piece

    black_pieces = get_black_pieces(board) #get pieces and place
    for black_piece in black_pieces: #print all the piece on the board
        change_board(board, black_piece, "b") #print all the piece on the board

    #check if white can take any black piece/pieces
    white_piece_can_take = take_black_piece(board, white_piece)
    
    print_board(board, white_piece_can_take)


    if white_piece_can_take:
        print("The possible capture pieces marked with 'X'.")
    else:
        print("Sorry, no piece can be capture by white piece.")

    #print out the board with X marking pieces white can take
        #if nothing can be taken print out text "White piece can`t take any pieces"
#don`t work
def new_board():
   return [
        ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
        ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
        ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
        ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
        ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
        ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
        ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
        ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
    ]

def get_white_piece():
    #to  help check if they put in the correct piece name
    pieces_list = ["king", "queen", "rook", "bishop", "knight", "pawn"]
    #suggest 2 random pieces
    suggest = random.sample(pieces_list, k=2)

    while True:
        #getting input of white piece location
        white_piece_place = input(f"Please enter white piece name (e.g. {suggest[0]} or {suggest[1]}) and location: ").strip().lower()

        #checking input
        try:
            w_piece, place = white_piece_place.split(" ")
            if w_piece not in pieces_list:
                print("Please check if you put in the correct piece name.")
                continue

            elif place[0] not in "abcdefgh" or place[1] not in "12345678":
                print("Please check if you put in the correct location.")
                continue

            else:
                #converting place into number e.g. 11 not a1
                x = 8 - int(place[1])  # Convert row (1-8) to board index (7-0)
                y = ord(place[0]) - ord("a")  # Convert column (a-h) to index (0-7)
                return [w_piece, x, y]

        except ValueError:
            print("Invalid input format. Please separate piece and position by space.")

def get_black_pieces(board):
    pieces_list = ["king", "queen", "rook", "bishop", "knight", "pawn"]

    #this will help to see that the user is not going to put in to many pieces that are the same
    piece_counts = {"king": 0, "queen": 0, "rook": 0, "bishop": 0, "knight": 0, "pawn": 0}
    max_counts = {"king": 1, "queen": 1, "rook": 2, "bishop": 2, "knight": 2, "pawn": 8}
    black_pieces_list = []

    while len(black_pieces_list) <= 16:
        black_pieces_place = input("Please enter all black pieces and their loaction one by one (when you finished write 'done'): ").strip().lower()

        #break with done
        if black_pieces_place == "done":
            break

        #spliting input
        try:
            # splitting input
            b_piece, place = black_pieces_place.split(" ")
        except ValueError:
            print("Invalid format. Please make sure that you are entering the piece and location in the format 'piece place' (e.g. 'king b3').")
            continue

        #checking input
        if b_piece not in pieces_list:
            print("Please check if you put in the correct piece name.")
            continue

        elif place[0] not in "abcdefgh" or place[1] not in "12345678":
            print("Please check if you put in the correct location.")
            continue

        #counting how many piece, so there wouldn`t be too many of them.
        if piece_counts[b_piece] >= max_counts[b_piece]:
            print(f"Maximum number of {b_piece}s ({max_counts[b_piece]}) already placed.")
            continue

        #converting from a1 to 11 and change xy, so x would be row and y column
        x = 8 - int(place[1])  # Convert row (1-8) to board index (7-0)
        y = ord(place[0]) - ord("a")  # Convert column (a-h) to index (0-7)
        if board[x][y] != "  ":
            print("Invalid move. Please pick a free space.")
            continue

        black_pieces_list.append([b_piece, x, y])
        piece_counts[b_piece] += 1

    return black_pieces_list

def change_board(board, piece_info, player):
    piece, x, y = piece_info

    # Define a dictionary mapping pieces to single letters
    piece_dict = {
        "king": "K",
        "queen": "Q",
        "rook": "R",
        "bishop": "B",
        "knight": "N",
        "pawn": "P"
    }

    # Get the letter corresponding to the piece
    piece_letter = piece_dict.get(piece, "")

    # Update the board with the player and piece letter
    board[x][y] = f"{player}{piece_letter}"

def print_board(board, white_piece_can_take):
    board_lines = []

    # Print the border
    border = '---' * 9
    board_lines.append(border)

    # Print each row of the board
    for row in range(8):
        row_line = str(8 - row)  # Row labels (8 to 1)
        for col in range(8):
            cell = board[row][col]
            row_line += f'|{cell}'
        row_line += '|'
        board_lines.append(row_line)
        board_lines.append(border)
    
    # Print column labels
    board_lines.append('  a  b  c  d  e  f  g  h')

    # Print the entire board
    print("\n".join(board_lines))

def take_black_piece(board, white_piece):
    take_piece = []

    piece_move = {
        "king": king_move,
        "queen": queen_move,
        "rook": rook_move,
        "bishop": bishop_move,
        "knight": knight_move,
        "pawn": pawn_move
    }

    w_piece, x, y = white_piece
    move = piece_move.get(w_piece)
    possible_moves = move(board, x, y)

    for move_x, move_y in possible_moves:
            if board[move_x][move_y].startswith('b'):
                take_piece.append((move_x, move_y))
                board[move_x][move_y] = f"X{board[move_x][move_y]}"

    return take_piece

def king_move(board, x, y):
    take_piece = []

    directions = [
        (x + 1, y), (x - 1, y),
        (x, y - 1), (x, y + 1),
        (x + 1, y - 1), (x - 1, y - 1),
        (x + 1, y + 1), (x - 1, y + 1)
    ]

    for move_x, move_y in directions:
        if 0 <= move_x < 8 and 0 <= move_y < 8 and board[move_x][move_y].startswith("b"):
            take_piece.append((move_x, move_y))

    return take_piece

def queen_move(board, x, y):
    take_piece = []
    directions = [
        (1, 0), (-1, 0), (0, 1), (0, -1),
        (1, 1), (-1, -1), (1, -1), (-1, 1)
    ]
    for dx, dy in directions:
        step = 1
        while True:
            move_x = x + dx * step
            move_y = y + dy * step
            if 0 <= move_x < 8 and 0 <= move_y < 8:
                if board[move_x][move_y] != " ":
                    if board[move_x][move_y].startswith("b"):
                        take_piece.append((move_x, move_y))
                    break
                step += 1
            else:
                break
    return take_piece

def rook_move(board, x, y):
    take_piece = []
    directions = [
        (1, 0), (-1, 0), (0, 1), (0, -1)
    ]

    for dx, dy in directions:
        step = 1
        while True:
            move_x = x + dx * step
            move_y = y + dy * step
            if 0 <= move_x < 8 and 0 <= move_y < 8:
                if board[move_x][move_y] != " ":
                    if board[move_x][move_y].startswith("b"):
                        take_piece.append((move_x, move_y))
                    break
                step += 1
            else:
                break

    return take_piece

def bishop_move(board, x, y):
    take_piece = []

    directions = [
        (1, 1), (-1, -1), (1, -1), (-1, 1)
    ]

    for dx, dy in directions:
        step = 1
        while True:
            move_x = x + dx * step
            move_y = y + dy * step
            if 0 <= move_x < 8 and 0 <= move_y < 8:
                if board[move_x][move_y] != " ":
                    if board[move_x][move_y].startswith("b"):
                        take_piece.append((move_x, move_y))
                    break
                step += 1
            else:
                break

    return take_piece

def knight_move(board, x, y):
    take_piece = []

    directions = [
        (x + 2, y + 1), (x + 2, y - 1),
        (x - 2, y + 1), (x - 2, y - 1),
        (x + 1, y + 2), (x + 1, y - 2),
        (x - 1, y + 2), (x - 1, y - 2)
    ]

    for move_x, move_y in directions:
        if 0 <= move_x < 8 and 0 <= move_y < 8 and board[move_x][move_y].startswith("b"):
            take_piece.append((move_x, move_y))

    return take_piece

def pawn_move(board, x, y):
    take_piece = []

    directions = [
        (x - 1, y - 1), (x - 1, y + 1)
    ]
    for move_x, move_y in directions:
        if 0 <= move_x < 8 and 0 <= move_y < 8 and board[move_x][move_y].startswith("b"):
            take_piece.append((move_x, move_y))

    return take_piece



if __name__ == "__main__":
    main()