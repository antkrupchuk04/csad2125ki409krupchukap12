// Rock-Paper-Scissors Game on Arduino using UART

// Constants for moves
/// Constant for Rock move
const int ROCK = 1;
/// Constant for Paper move
const int PAPER = 2;
/// Constant for Scissors move
const int SCISSORS = 3;

/**
 * @brief Initialize Serial communication and prompt user for input.
 * 
 * This function is called once when the Arduino is powered on. It sets up
 * the serial communication and sends a welcome message to the user, prompting
 * them to choose a move (1 for Rock, 2 for Paper, or 3 for Scissors).
 */
void setup() {
  // Initialize Serial communication at 9600 baud rate
  Serial.begin(9600);
  Serial.println("Welcome to Rock-Paper-Scissors Game!");
  Serial.println("Enter your move: 1 for Rock, 2 for Paper, 3 for Scissors.");
}

/**
 * @brief Main game loop where player input is processed.
 * 
 * This function continuously checks for incoming data from the Serial port.
 * When a valid move is entered by the player, the Arduino generates its own 
 * move and determines the game result, then sends the moves and the result 
 * back to the player via Serial.
 */
void loop() {
  // Check if there is data available to read from Serial
  if (Serial.available() > 0) {
    int playerMove = Serial.parseInt(); // Get the player's move from Serial
    if (playerMove >= ROCK && playerMove <= SCISSORS) {
      // Generate a random move for Arduino
      int arduinoMove = random(ROCK, SCISSORS + 1);
      
      // Determine the result
      String result = getResult(playerMove, arduinoMove);
      
      // Send moves and result back to Serial
      Serial.print("Player's Move: ");
      Serial.println(getMoveName(playerMove));
      Serial.print("Arduino's Move: ");
      Serial.println(getMoveName(arduinoMove));
      Serial.print("Result: ");
      Serial.println(result);
      Serial.println("Enter your next move (1 for Rock, 2 for Paper, 3 for Scissors):");
    } else {
      Serial.println("Invalid move. Please enter 1, 2, or 3.");
    }
  }
}

/**
 * @brief Get the name of the move based on the move identifier.
 * 
 * @param move The move identifier (1 for Rock, 2 for Paper, 3 for Scissors).
 * @return A string representing the name of the move.
 */
String getMoveName(int move) {
  if (move == ROCK) return "Rock";
  if (move == PAPER) return "Paper";
  if (move == SCISSORS) return "Scissors";
  return "Unknown";
}

/**
 * @brief Determine the result of the game between the player and Arduino.
 * 
 * This function compares the player's move and Arduino's move to determine the result.
 * 
 * @param playerMove The player's move (1 for Rock, 2 for Paper, 3 for Scissors).
 * @param arduinoMove The Arduino's randomly generated move (1 for Rock, 2 for Paper, 3 for Scissors).
 * @return A string indicating the result of the game: "Draw!", "Player Wins!", or "Arduino Wins!".
 */
String getResult(int playerMove, int arduinoMove) {
  if (playerMove == arduinoMove) return "Draw!";
  if ((playerMove == ROCK && arduinoMove == SCISSORS) ||
      (playerMove == PAPER && arduinoMove == ROCK) ||
      (playerMove == SCISSORS && arduinoMove == PAPER)) {
    return "Player Wins!";
  }
  return "Arduino Wins!";
}
