import java.io.File;
import java.io.FileNotFoundException;
import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;
import java.util.stream.Collectors;


public class SeatingSystem {
    private static final String FILENAME = "./input.txt";

    // Helper function, converts a string a list of our seat state enum
    private static List<SeatStates> parseSeatStatesFromString(String s) {
        return s.chars().mapToObj(e -> switch ((char) e) {
            case 'L' -> SeatStates.EMPTY;
            case '.' -> SeatStates.FLOOR;
            case '#' -> SeatStates.OCCUPIED;
            default -> null;
        }).collect(Collectors.toList());
    }

    private static ArrayList<List<SeatStates>> parseSeatingFile() throws FileNotFoundException {
        // A list of lists of seat states - a 2-D array of seats
        ArrayList<List<SeatStates>> seatingFile = new ArrayList<>();

        // Read in the file
        File inputFile = new File(FILENAME);
        Scanner scanner = new Scanner(inputFile);

        // Parse through the file and create our initial seating chart
        while (scanner.hasNextLine()) {
            var line = scanner.nextLine();
            seatingFile.add(parseSeatStatesFromString(line));
        }

        return seatingFile;
    }

    // Given a state, and a Visible seat counter, get the next state
    private static ArrayList<List<SeatStates>> getNextSeatStates(ArrayList<List<SeatStates>> currentState, VisibleSeatCounter counter) {
        // Initialize our next state
        ArrayList<List<SeatStates>> nextState = new ArrayList<>();

        // Loop through each current state, and find the next state
        for (int y = 0; y < currentState.size(); y++) {
            List<SeatStates> nextLine = new ArrayList<>();
            for (int x = 0; x < currentState.get(y).size(); x++) {
                var currentSeat = currentState.get(y).get(x);

                // Floor will never change
                if (currentSeat.equals(SeatStates.FLOOR)) {
                    nextLine.add(SeatStates.FLOOR);
                }
                // If a seat is empty, someone will sit there unless someone else is in their "view"
                else if (currentSeat.equals(SeatStates.EMPTY)) {
                    nextLine.add(counter.count(currentState, x, y) > 0 ? SeatStates.EMPTY : SeatStates.OCCUPIED);
                }
                // An occupied seat will stay occupied until more than counter.getTolerance() people are nearby
                else if (currentSeat.equals(SeatStates.OCCUPIED)) {
                    nextLine.add(counter.count(currentState, x, y) >= counter.getTolerance() ? SeatStates.EMPTY : SeatStates.OCCUPIED);
                }
            }
            // Add this line to our state
            nextState.add(nextLine);
        }
        return nextState;
    }
    // Finds the final state, and counts the seats that are filled
    private static int countFilledSeats(ArrayList<List<SeatStates>> startingState, VisibleSeatCounter counter) {
        ArrayList<List<SeatStates>> currentState = startingState;
        ArrayList<List<SeatStates>> nextState = getNextSeatStates(startingState, counter);
        // Keep looping until we hit a stable state
        while (!currentState.equals(nextState)) {
            currentState = nextState;
            nextState = getNextSeatStates(currentState, counter);
        }
        // Count the occupied seats
        int occupiedSeats = 0;
        for (List<SeatStates> row : currentState) {
            for (SeatStates state : row) {
                if (state.equals(SeatStates.OCCUPIED)) {
                    occupiedSeats++;
                }
            }
        }

        return occupiedSeats;
    }

    public static void main(String[] args) {
        try {
            var seatingChart = parseSeatingFile();

            System.out.println("--Part 1--");
            var occupiedSeatsPart1 = countFilledSeats(seatingChart, new Part1SeatCounter());
            System.out.println(occupiedSeatsPart1 + " occupied seats");

            System.out.println("--Part 2--");
            var occupiedSeatsPart2 = countFilledSeats(seatingChart, new Part2SeatCounter());
            System.out.println(occupiedSeatsPart2 + " occupied seats");
        } catch (FileNotFoundException e) {
            System.out.println("File not found: " + e.getMessage());
        }
    }
}

// Interface for classes for part 1 and part 2
abstract class VisibleSeatCounter {
    private final int tolerance;

    public VisibleSeatCounter(int tolerance) {
        this.tolerance = tolerance;
    }

    public int getTolerance(){
        return tolerance;
    }
    abstract int count(ArrayList<List<SeatStates>> state, int x, int y); // Count the people sitting around someone
}

class Part1SeatCounter extends VisibleSeatCounter{
    public Part1SeatCounter(){
        super(4);
    }

    // This counts the areas directly next to a seat in a square from (-1, -1), to (1, 1)
    public int count(ArrayList<List<SeatStates>> state, int x, int y) {
        int countSurroundingFilledSeats = 0;

        // Make sure we don't check outside of our bounds
        int yMin = y - 1 >= 0 ? y - 1 : y;
        int yMax = y + 1 < state.size() ? y + 1 : y;
        int xMin = x - 1 >= 0 ? x - 1 : x;
        int xMax = x + 1 < state.get(y).size() ? x + 1 : x;

        // Loop through our list, ignoring our current seat
        for (int yCheck = yMin; yCheck <= yMax; yCheck++) {
            for (int xCheck = xMin; xCheck <= xMax; xCheck++) {
                if (xCheck != x || yCheck != y) {
                    // If the seat is occupied, add one to the count
                    if (state.get(yCheck).get(xCheck).equals(SeatStates.OCCUPIED)) {
                        countSurroundingFilledSeats++;
                    }
                }
            }
        }
        return countSurroundingFilledSeats;
    }
}

class Part2SeatCounter extends VisibleSeatCounter{
    public Part2SeatCounter() {
        super(5);
    }

    // This checks like a queen moves in chess - diagonals & straight lines until it hits something
    public int count(ArrayList<List<SeatStates>> state, int x, int y) {
        // Our range of possible directions for x & y
        int[] range = new int[] {-1, 0, 1};

        int visibleSeatCount = 0;
        // Loop through our ranges to get our x and y directions - this will create all 9 possibilities.
        for(int yDir: range) {
            for(int xDir: range) {
                // Make sure the current direction isn't just 0, 0
                if(xDir != 0 || yDir != 0) {
                    // Create our next x and next y directions
                    int nextX = x + xDir;
                    int nextY = y + yDir;
                    // While we remain in the bounds...
                    while (nextY >= 0 && nextY < state.size() && nextX >= 0 && nextX < state.get(nextY).size()) {
                        // If our current position is an empty seat, we stop searching, but don't count it
                        if(state.get(nextY).get(nextX).equals(SeatStates.EMPTY)) {
                            break;
                        }
                        // If our current position is a filled seat, we stop searching, and increment our count
                        if(state.get(nextY).get(nextX).equals(SeatStates.OCCUPIED)){
                            visibleSeatCount++;
                            break;
                        }
                        // Update nextX and nextY
                        nextY += yDir;
                        nextX += xDir;
                    }
                }
            }
        }
        return visibleSeatCount;
    }
}

// Enumeration for the different seat states.
enum SeatStates {
    OCCUPIED,
    EMPTY,
    FLOOR
}
