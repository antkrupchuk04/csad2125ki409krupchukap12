// Rock-Paper-Scissors Game on Arduino using UART

// Constants for moves
const int ROCK = 1;
const int PAPER = 2;
const int SCISSORS = 3;

void setup() {
  // Initialize Serial communication at 9600 baud rate
  Serial.begin(9600);
  Serial.println("Welcome to Rock-Paper-Scissors Game!");
  Serial.println("Enter your move: 1 for Rock, 2 for Paper, 3 for Scissors.");
}

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
    }
  }
}

// Function to get move name
String getMoveName(int move) {
  if (move == ROCK) return "Rock";
  if (move == PAPER) return "Paper";
  if (move == SCISSORS) return "Scissors";
  return "Unknown";
}

// Function to determine the game result
String getResult(int playerMove, int arduinoMove) {
  if (playerMove == arduinoMove) return "Draw!";
  if ((playerMove == ROCK && arduinoMove == SCISSORS) ||
      (playerMove == PAPER && arduinoMove == ROCK) ||
      (playerMove == SCISSORS && arduinoMove == PAPER)) {
    return "Player Wins!";
  }
  return "Arduino Wins!";
}
