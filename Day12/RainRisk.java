import java.io.File;
import java.io.FileNotFoundException;
import java.util.*;

public class RainRisk {
    private static final String FILENAME = "./input.txt";

    private static ArrayList<Instruction> parseInstructions() throws FileNotFoundException {
        // A list of instructions
        ArrayList<Instruction> instructions = new ArrayList<>();

        // Read in the file
        File inputFile = new File(FILENAME);
        Scanner scanner = new Scanner(inputFile);

        // Parse through the file and parse each instruction
        while (scanner.hasNextLine()) {
            var line = scanner.nextLine();
            String strAction = line.substring(0, 1);
            int value = Integer.parseInt(line.substring(1));

            // Convert the action to an enum
            Action action = switch (strAction) {
                case "N" -> Action.NORTH;
                case "E" -> Action.EAST;
                case "S" -> Action.SOUTH;
                case "W" -> Action.WEST;
                case "L" -> Action.LEFT;
                case "R" -> Action.RIGHT;
                case "F" -> Action.FORWARD;
                default -> throw new IllegalStateException("Unexpected value: " + strAction);
            };
            Instruction instruction = new Instruction(action, value);
            instructions.add(instruction);
        }

        return instructions;
    }

    // Runs the instructions for the given shipState
    private static int followInstructions(ArrayList<Instruction> instructions, AbstractShipState shipState) {
        instructions.forEach((shipState::followInstruction));
        return shipState.getManhattanDistance();
    }

    public static void main(String[] args) {
        try {
            var instructions = parseInstructions();

            System.out.println("--Part 1--");
            var manhattanDistancePart1 = followInstructions(instructions, new DirectedShipState());
            System.out.printf("Manhattan Distance: %d units\n", manhattanDistancePart1);

            System.out.println("--Part 2--");
            var manhattanDistancePart2 = followInstructions(instructions, new WaypointShipState());
            System.out.printf("Manhattan Distance: %d units\n", manhattanDistancePart2);
        } catch (FileNotFoundException e) {
            System.out.println(e.getMessage());
        }
    }
}

abstract class AbstractShipState {
    private final HashMap<Direction, Integer> distances;

    public AbstractShipState() {
        // Initialize our distances
        distances = new HashMap<>();
        distances.put(Direction.NORTH, 0);
        distances.put(Direction.EAST, 0);
        distances.put(Direction.WEST, 0);
        distances.put(Direction.SOUTH, 0);
    }

    // Updates the HashMap value for the given direction
    public void updateDirection(Direction direction, int value) {
        distances.put(direction, distances.get(direction) + value);
    }

    // Abstract followInstruction - should be implemented by classes extending this one
    public abstract void followInstruction(Instruction instruction);

    // Calculates the Manhattan distance for the hashMap
    public int getManhattanDistance() {
        int xDistance = Math.abs(distances.get(Direction.EAST) - distances.get(Direction.WEST));
        int yDistance = Math.abs(distances.get(Direction.NORTH) - distances.get(Direction.SOUTH));
        return xDistance + yDistance;
    }
}

// Directed ship state - the instructions all control the ship directly
class DirectedShipState extends AbstractShipState {
    private Direction currentFacing; // Where is the ship pointing?

    public DirectedShipState() {
        super();
        currentFacing = Direction.EAST;
    }

    private void getNextFacing(int value) {
        // Directions in order, so that we can find the next/previous direction
        List<Direction> directions = Arrays.asList(Direction.NORTH, Direction.EAST, Direction.SOUTH, Direction.WEST);
        int currentIndex = directions.indexOf(currentFacing); // Find our current index
        int offset = value / 90; // How many indexes are we moving
        currentFacing = directions.get((currentIndex + offset + 4) % 4);
    }

    public void followInstruction(Instruction instruction) {
        switch (instruction.getAction()) { // Follow the action
            case NORTH -> updateDirection(Direction.NORTH, instruction.getValue());
            case EAST -> updateDirection(Direction.EAST, instruction.getValue());
            case SOUTH -> updateDirection(Direction.SOUTH, instruction.getValue());
            case WEST -> updateDirection(Direction.WEST, instruction.getValue());
            case LEFT -> getNextFacing(instruction.getValue() * -1);
            case RIGHT -> getNextFacing(instruction.getValue());
            case FORWARD -> updateDirection(currentFacing, instruction.getValue());
        }
    }
}

// Waypoint ship state - the instructions mostly control a waypoint
class WaypointShipState extends AbstractShipState {
    private int waypointX;
    private int waypointY;

    public WaypointShipState() {
        super();
        waypointX = 10;
        waypointY = 1;
    }

    private void handleRotation(int value) {
        // if its a 90 degree change, (x, y) becomes (-y, x)
        if (value == 90 || value == -270) {
            int tmp = waypointX;
            waypointX = -waypointY;
            waypointY = tmp;
        }
        // If its a 180 degree change, (x, y) becomes (-x, -y)
        else if (value == 180 || value == -180) {
            waypointX = -waypointX;
            waypointY = -waypointY;
        }
        // If its a 270 degree change, (x, y) becomes (y, -x)
        else if (value == 270 || value == -90) {
            int tmp = waypointY;
            waypointY = -waypointX;
            waypointX = tmp;
        }
    }

    // Move the boat x times towards the waypoint
    private void moveTowardWaypoint(int times) {
        if (waypointX > 0) {
            updateDirection(Direction.EAST, waypointX * times);
        } else {
            updateDirection(Direction.WEST, -waypointX * times);
        }
        if (waypointY > 0) {
            updateDirection(Direction.NORTH, waypointY * times);
        } else {
            updateDirection(Direction.SOUTH, -waypointY * times);
        }
    }

    public void followInstruction(Instruction instruction) {
        switch (instruction.getAction()) { // Deal with the instructions
            case NORTH -> waypointY += instruction.getValue();
            case EAST -> waypointX += instruction.getValue();
            case SOUTH -> waypointY -= instruction.getValue();
            case WEST -> waypointX -= instruction.getValue();
            case LEFT -> handleRotation(instruction.getValue());
            case RIGHT -> handleRotation(-instruction.getValue());
            case FORWARD -> moveTowardWaypoint(instruction.getValue());
        }
    }
}

// Instruction class, helps store our input
class Instruction {
    private final Action action;
    private final int value;

    public Instruction(Action action, int value) {
        this.action = action;
        this.value = value;
    }

    public Action getAction() {
        return action;
    }

    public int getValue() {
        return value;
    }

    public String toString() {
        return action + ": " + value;
    }
}

// Actions that come from input.txt
enum Action {
    NORTH,
    EAST,
    SOUTH,
    WEST,
    RIGHT,
    LEFT,
    FORWARD
}

// Cardinal Directions
enum Direction {
    NORTH,
    EAST,
    SOUTH,
    WEST
}