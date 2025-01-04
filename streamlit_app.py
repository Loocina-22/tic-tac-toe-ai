import streamlit as st

# Initialize session state variables
if "board" not in st.session_state:
    st.session_state.board = [[None for _ in range(3)] for _ in range(3)]
if "scores" not in st.session_state:
    st.session_state.scores = {'Player': 0, 'AI': 0}
if "player_turn" not in st.session_state:
    st.session_state.player_turn = True
if "game_over" not in st.session_state:
    st.session_state.game_over = False

# Draw the game board
def draw_board():
    for row in range(3):
        cols = st.columns(3)
        for col in range(3):
            cell_value = st.session_state.board[row][col]
            button_label = cell_value if cell_value else " "
            if cols[col].button(button_label, key=f"cell-{row}-{col}"):
                if not st.session_state.game_over and st.session_state.player_turn:
                    if st.session_state.board[row][col] is None:
                        st.session_state.board[row][col] = 'X'
                        if check_winner('X'):
                            st.success("You win!")
                            st.session_state.scores['Player'] += 1
                            st.session_state.game_over = True
                        elif is_draw():
                            st.warning("It's a draw!")
                            st.session_state.game_over = True
                        else:
                            st.session_state.player_turn = False

# Check for a winner
def check_winner(player):
    board = st.session_state.board
    for row in range(3):
        if board[row][0] == board[row][1] == board[row][2] == player:
            return True
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] == player:
            return True
    if board[0][0] == board[1][1] == board[2][2] == player:
        return True
    if board[0][2] == board[1][1] == board[2][0] == player:
        return True
    return False

# Check for a draw
def is_draw():
    for row in st.session_state.board:
        if None in row:
            return False
    return True

# Minimax algorithm with alpha-beta pruning
def minimax(board, depth, is_maximizing, alpha, beta):
    if check_winner('O'):
        return 10 - depth
    if check_winner('X'):
        return depth - 10
    if is_draw():
        return 0

    if is_maximizing:
        max_eval = -float('inf')
        for row in range(3):
            for col in range(3):
                if board[row][col] is None:
                    board[row][col] = 'O'
                    eval = minimax(board, depth + 1, False, alpha, beta)
                    board[row][col] = None
                    max_eval = max(max_eval, eval)
                    alpha = max(alpha, eval)
                    if beta <= alpha:
                        break
        return max_eval
    else:
        min_eval = float('inf')
        for row in range(3):
            for col in range(3):
                if board[row][col] is None:
                    board[row][col] = 'X'
                    eval = minimax(board, depth + 1, True, alpha, beta)
                    board[row][col] = None
                    min_eval = min(min_eval, eval)
                    beta = min(beta, eval)
                    if beta <= alpha:
                        break
        return min_eval

# AI move
def ai_move():
    best_score = -float('inf')
    best_move = None
    for row in range(3):
        for col in range(3):
            if st.session_state.board[row][col] is None:
                st.session_state.board[row][col] = 'O'
                score = minimax(st.session_state.board, 0, False, -float('inf'), float('inf'))
                st.session_state.board[row][col] = None
                if score > best_score:
                    best_score = score
                    best_move = (row, col)
    if best_move:
        st.session_state.board[best_move[0]][best_move[1]] = 'O'

# Restart the game
def restart_game():
    st.session_state.board = [[None for _ in range(3)] for _ in range(3)]
    st.session_state.player_turn = True
    st.session_state.game_over = False

# Game logic
if not st.session_state.player_turn and not st.session_state.game_over:
    ai_move()
    if check_winner('O'):
        st.error("AI wins!")
        st.session_state.scores['AI'] += 1
        st.session_state.game_over = True
    elif is_draw():
        st.warning("It's a draw!")
        st.session_state.game_over = True
    st.session_state.player_turn = True

# Display the game board
st.title("Tic Tac Toe AI with Minimax")
st.write("Player: X, AI: O")
draw_board()

# Display scores
st.sidebar.header("Scores")
st.sidebar.write(f"Player: {st.session_state.scores['Player']}")
st.sidebar.write(f"AI: {st.session_state.scores['AI']}")

# Restart button
if st.sidebar.button("Restart Game"):
    restart_game()
