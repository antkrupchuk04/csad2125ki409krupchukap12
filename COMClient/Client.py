import tkinter as tk
from tkinter import messagebox
import serial
import time
import random

## Define global constants
SERIAL_PORT = None  ## Port for serial communication
BAUD_RATE = 9600    ## Baud rate for serial communication

## Dictionary for player moves
moves = {
    1: "Rock",        ## Rock move
    2: "Paper",       ## Paper move
    3: "Scissors"     ## Scissors move
}

## Dictionary for move emojis
move_emoji = {
    "Rock": "✊",     ## Emoji for Rock move
    "Paper": "✋",    ## Emoji for Paper move
    "Scissors": "✌️" ## Emoji for Scissors move
}

## Game mode and player moves
game_mode = "PvA"  ## Default mode: "PvA" (Player vs Arduino), "PvP" (Player vs Player), "AIvAI" (AI vs AI)
player1_move = None
player2_move = None

## Function to send the player's move to the Arduino
## @param move The move chosen by the player
def send_move_to_arduino(move):
    try:
        result_text.delete("1.0", tk.END)  ## Clear previous results
        
        ## Send the move to the Arduino through the serial connection
        ser.write((str(move) + '\n').encode())
        time.sleep(1)
        
        player_move, arduino_move, result = "", "", ""
        
        ## Read the response from Arduino
        while ser.in_waiting > 0:
            response = ser.readline().decode().strip()
            if "Player's Move" in response:
                player_move = response.replace("Player's Move:", "Player's Move: ")
            elif "Arduino's Move" in response:
                arduino_move = response.replace("Arduino's Move:", "Arduino's Move: ")
            elif "Result" in response:
                result = response

        ## Replace moves with corresponding emojis
        for move_name, emoji in move_emoji.items():
            player_move = player_move.replace(move_name, emoji)
            arduino_move = arduino_move.replace(move_name, emoji)

        ## Insert the results into the text box
        result_text.insert(tk.END, f"--- Game Result ---\n\n")
        result_text.insert(tk.END, f"{player_move}\n")
        result_text.insert(tk.END, f"{arduino_move}\n")

        if "Player Wins!" in result:
            result_text.insert(tk.END, f"{result}\n", "win")
        elif "Arduino Wins!" in result:
            result_text.insert(tk.END, f"{result}\n", "lose")
        else:
            result_text.insert(tk.END, f"{result}\n", "draw")

        result_text.insert(tk.END, "\n--------------------\n")
        
    except serial.SerialException:
        ## If there is a serial connection error, show an error message
        messagebox.showerror("Connection Error", f"Lost connection to Arduino on {SERIAL_PORT}.")
        root.quit()

## Function to play Player vs Player mode
def play_pvp():
    global player1_move, player2_move
    if player1_move and player2_move:
        result_text.delete("1.0", tk.END)

        ## Determine the result of the game
        if player1_move == player2_move:
            result = "It's a Draw!"
            tag = "draw"
        elif (player1_move == "Rock" and player2_move == "Scissors") or \
             (player1_move == "Paper" and player2_move == "Rock") or \
             (player1_move == "Scissors" and player2_move == "Paper"):
            result = "Player 1 Wins!"
            tag = "win"
        else:
            result = "Player 2 Wins!"
            tag = "lose"

        ## Display the results
        result_text.insert(tk.END, "--- PvP Game Result ---\n\n")
        result_text.insert(tk.END, f"Player 1 Move: {move_emoji[player1_move]}\n")
        result_text.insert(tk.END, f"Player 2 Move: {move_emoji[player2_move]}\n")
        result_text.insert(tk.END, f"{result}\n", tag)
        result_text.insert(tk.END, "\n--------------------\n")

        ## Reset moves for next game
        player1_move, player2_move = None, None

## Function to play AI vs AI mode
def play_aivai():
    global player1_move, player2_move
    result_text.delete("1.0", tk.END)

    ## Generate random moves for AI players
    player1_move = random.choice(["Rock", "Paper", "Scissors"])
    player2_move = random.choice(["Rock", "Paper", "Scissors"])

    ## Determine the result of the game
    if player1_move == player2_move:
        result = "It's a Draw!"
        tag = "draw"
    elif (player1_move == "Rock" and player2_move == "Scissors") or \
         (player1_move == "Paper" and player2_move == "Rock") or \
         (player1_move == "Scissors" and player2_move == "Paper"):
        result = "AI 1 Wins!"
        tag = "win"
    else:
        result = "AI 2 Wins!"
        tag = "lose"

    ## Display the results
    result_text.insert(tk.END, "--- AI vs AI Game Result ---\n\n")
    result_text.insert(tk.END, f"AI 1 Move: {move_emoji[player1_move]}\n")
    result_text.insert(tk.END, f"AI 2 Move: {move_emoji[player2_move]}\n")
    result_text.insert(tk.END, f"{result}\n", tag)
    result_text.insert(tk.END, "\n--------------------\n")

## Function to choose a move
## @param move The move chosen by the player
def choose_move(move):
    global player1_move, player2_move
    if game_mode == "PvA":
        send_move_to_arduino(move)
    elif game_mode == "PvP":
        if not player1_move:
            player1_move = moves.get(move)
            instruction_label.config(text="Player 2: Choose your move")
        else:
            player2_move = moves.get(move)
            play_pvp()
            instruction_label.config(text="Player 1: Choose your move")
    elif game_mode == "AIvAI":
        play_aivai()

## Function to toggle the game mode
def toggle_mode():
    global game_mode
    if game_mode == "PvA":
        game_mode = "PvP"
    elif game_mode == "PvP":
        game_mode = "AIvAI"
    else:
        game_mode = "PvA"
    mode_button.config(text="Mode: " + game_mode)
    reset_game()

## Function to reset the game
def reset_game():
    global player1_move, player2_move
    player1_move, player2_move = None, None
    instruction_label.config(text="Choose your move:" if game_mode == "PvA" else 
                             ("Player 1: Choose your move" if game_mode == "PvP" else "AI vs AI Mode"))
    result_text.delete("1.0", tk.END)
    if game_mode == "AIvAI":
        play_aivai()

## Main execution
if __name__ == "__main__":

    ## Prompt for serial port
    SERIAL_PORT = input("Enter the serial port (e.g., COM3 or /dev/ttyUSB0): ")

    try:
        ## Establish serial connection to Arduino
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
        time.sleep(2)
        print("Connected to Arduino on", SERIAL_PORT)
    except serial.SerialException:
        ## Error handling if serial connection fails
        print(f"Error: Could not open Serial port {SERIAL_PORT}.")
        exit()

    ## Initialize Tkinter window
    root = tk.Tk()
    root.title("Rock-Paper-Scissors Game")
    root.geometry("400x400")

    ## Label for instructions
    instruction_label = tk.Label(root, text="Choose your move:", font=("Helvetica", 14))
    instruction_label.pack(pady=10)

    ## Button frame for choosing moves
    button_frame = tk.Frame(root)
    button_frame.pack(pady=10)

    ## Buttons for each move
    rock_button = tk.Button(button_frame, text="Rock ✊", font=("Helvetica", 12), width=10, command=lambda: choose_move(1))
    rock_button.grid(row=0, column=0, padx=10)

    paper_button = tk.Button(button_frame, text="Paper ✋", font=("Helvetica", 12), width=10, command=lambda: choose_move(2))
    paper_button.grid(row=0, column=1, padx=10)

    scissors_button = tk.Button(button_frame, text="Scissors ✌️", font=("Helvetica", 12), width=10, command=lambda: choose_move(3))
    scissors_button.grid(row=0, column=2, padx=10)

    ## Label and text box for game results
    result_label = tk.Label(root, text="Game Result:", font=("Helvetica", 14))
    result_label.pack(pady=10)

    result_text = tk.Text(root, height=8, width=40, font=("Helvetica", 12))
    result_text.pack(pady=10)
    result_text.config(state="normal")

    ## Tag configurations for result display
    result_text.tag_config("win", foreground="green")
    result_text.tag_config("lose", foreground="red")
    result_text.tag_config("draw", foreground="gold")

    ## Button to toggle game modes
    mode_button = tk.Button(root, text="Mode: PvA", font=("Helvetica", 12), command=toggle_mode)
    mode_button.pack(pady=5)

    ## Handle window close event
    def on_closing():
        if ser.is_open:
            ser.close()
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_closing)

    ## Start the Tkinter main loop
    root.mainloop()
