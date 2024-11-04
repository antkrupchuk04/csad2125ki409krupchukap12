import tkinter as tk
from tkinter import messagebox
import serial
import time

SERIAL_PORT = input("Enter the serial port (e.g., COM3 or /dev/ttyUSB0): ")
BAUD_RATE = 9600

try:
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    time.sleep(2)
    print("Connected to Arduino on", SERIAL_PORT)
except serial.SerialException:
    print(f"Error: Could not open Serial port {SERIAL_PORT}.")
    exit()

move_emoji = {
    "Rock": "✊",
    "Paper": "✋",
    "Scissors": "✌️"
}

def send_move(move):
    try:
        result_text.delete("1.0", tk.END)

        ser.write((str(move) + '\n').encode())
        time.sleep(1)

        player_move, arduino_move, result = "", "", ""
        while ser.in_waiting > 0:
            response = ser.readline().decode().strip()
            if "Player's Move" in response:
                player_move = response.replace("Player's Move:", "Player's Move: ")
            elif "Arduino's Move" in response:
                arduino_move = response.replace("Arduino's Move:", "Arduino's Move: ")
            elif "Result" in response:
                result = response

        for move_name, emoji in move_emoji.items():
            player_move = player_move.replace(move_name, emoji)
            arduino_move = arduino_move.replace(move_name, emoji)

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
        messagebox.showerror("Connection Error", f"Lost connection to Arduino on {SERIAL_PORT}.")
        root.quit()

root = tk.Tk()
root.title("Rock-Paper-Scissors Game")
root.geometry("400x320")

instruction_label = tk.Label(root, text="Choose your move:", font=("Helvetica", 14))
instruction_label.pack(pady=10)

button_frame = tk.Frame(root)
button_frame.pack(pady=10)

rock_button = tk.Button(button_frame, text="Rock ✊", font=("Helvetica", 12), width=10, command=lambda: send_move(1))
rock_button.grid(row=0, column=0, padx=10)

paper_button = tk.Button(button_frame, text="Paper ✋", font=("Helvetica", 12), width=10, command=lambda: send_move(2))
paper_button.grid(row=0, column=1, padx=10)

scissors_button = tk.Button(button_frame, text="Scissors ✌️", font=("Helvetica", 12), width=10, command=lambda: send_move(3))
scissors_button.grid(row=0, column=2, padx=10)

result_label = tk.Label(root, text="Game Result:", font=("Helvetica", 14))
result_label.pack(pady=10)

result_text = tk.Text(root, height=8, width=40, font=("Helvetica", 12))
result_text.pack(pady=10)
result_text.config(state="normal")

result_text.tag_config("win", foreground="green")
result_text.tag_config("lose", foreground="red")
result_text.tag_config("draw", foreground="gold")

def on_closing():
    if ser.is_open:
        ser.close()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)

root.mainloop()
