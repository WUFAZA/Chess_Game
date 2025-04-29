from Chess import *
import pygame as pg


# Initiate the pygame library
pg.init()

# Create the game screen
screen = pg.display.set_mode((780, 780))
pg.display.set_caption("Chess by Faaiz")
icon = pg.image.load(r"Img/chess.png")
pg.display.set_icon(icon)

# Create an image object for the board
board_img = pg.image.load(r"Img\board.png")

# Set the board image offset in the game screen
board_x = 15
board_y = 15


def show_state():
    # Background
    screen.fill((117, 117, 117))
    # Board
    screen.blit(board_img, (board_x, board_y))
    # Placing the pieces on the screen
    for t in game.player1.tools + game.player2.tools:
        if t.position is not None:
            screen.blit(t.icon, (t.x, t.y))
    # Show an indicator to the current player
    if current_player.team:
        pg.draw.rect(screen, (0, 0, 0), (0, 0, 10, 10))
    else:
        pg.draw.rect(screen, (255, 255, 255), (0, 0, 10, 10))
    # Update the board
    pg.display.update()


def handle_events():
    l = [True, False]
    for event in pg.event.get():
        if event.type == pg.QUIT:
            l[0] = False
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                l[1] = True
    return l


# Convert pixel to position on the game board
def convert(place):
    return [(place[1] - 14) // 94, (place[0] - 14) // 94]


game = Game()
play = True
current_player = game.player1
selected_pos = (0, 0)
selected = False
last_selected = (0, 0)
state = None

while play:
    play, click = handle_events()
    if click:
        selected_pos = convert(pg.mouse.get_pos())
        current_tools_at = [t.position for t in current_player.tools]
        # If the selected place on the board is move from or move to
        if selected:
            # If the selected tool needs to be switched
            if selected_pos in current_tools_at:
                last_selected = selected_pos
            # Try moving the selected tool
            else:
                # Save the piece we are moving to a variable
                try:
                    moved_piece = list(filter(lambda x: x.position == last_selected, current_player.tools))[0]
                except IndexError:
                    continue
                # Check if last_selected tool can move to selected_pos
                if moved_piece.valid_move(selected_pos) and moved_piece.is_legal_move(selected_pos):
                    moved_piece.move(selected_pos)
                    current_player = current_player.enemy
                    selected = False
                else:
                    print(moved_piece.name, "can't move to", selected_pos)
        # If this is a move-from than change last_position to the current selected
        elif selected_pos in current_tools_at:
            last_selected = selected_pos
            selected = True
        state = game.is_over()
        if state is not None:
            if state == "Tie":
                print("The game ends with a tie! Good Game!")
            else:
                print(state, "has won the game! Good Game!")
            play = False
        if game.player1.since_pawn_move >= 50 and game.player2.since_pawn_move >= 50:
            print("The game ended with a tie due to lack of pawn moves (50)")
            play = False
    show_state()
if state is None:
    print("Tie by choice! Good Game !")