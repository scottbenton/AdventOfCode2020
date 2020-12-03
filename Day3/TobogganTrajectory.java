import java.io.File;
import java.io.FileNotFoundException;
import java.util.Arrays;
import java.util.Scanner;
import java.util.ArrayList;
import java.util.stream.Collectors;

// Helper Class. In a normal environment this would be a separate file, but...
class TobogganTestCase {
  // Starting coordinates
  private final int xStart;
  private final int yStart;
  // Velocities - over x down y
  private final int xVelocity;
  private final int yVelocity;

  public TobogganTestCase(int xStart, int yStart, int xVelocity, int yVelocity) {
    this.xStart = xStart;
    this.yStart = yStart;
    this.xVelocity = xVelocity;
    this.yVelocity = yVelocity;
  }

  public TobogganTestCase(int xVelocity, int yVelocity) {
    this.xVelocity = xVelocity;
    this.yVelocity = yVelocity;
    this.xStart = 0;
    this.yStart = 0;
  }

  public int getxStart() {
    return xStart;
  }

  public int getxVelocity() {
    return xVelocity;
  }

  public int getyStart() {
    return yStart;
  }

  public int getyVelocity() {
    return yVelocity;
  }
}

class TobogganTrajectory {

  // FileName of the input file
  private static final String FILENAME = "./Day3/input.txt";
  // What character in the file is a tree?
  private static final char TREE_CHAR = '#';

  // Test cases for part 2
  private static final ArrayList<TobogganTestCase> testCases = new ArrayList<>(Arrays.asList(
          new TobogganTestCase(1, 1),
          new TobogganTestCase(3, 1),
          new TobogganTestCase(5, 1),
          new TobogganTestCase(7, 1),
          new TobogganTestCase(1, 2)
  ));

  // Read in the file to an ArrayList
  private static ArrayList<String> readBoard() throws FileNotFoundException{
    ArrayList<String> board = new ArrayList<>();
    
    File inputFile = new File(FILENAME);
    Scanner scanner = new Scanner(inputFile);
    while(scanner.hasNextLine()) {
      board.add(scanner.nextLine());
    }
    return board;
  }

  // Wrapper to use TobogganTestCase class
  private static int countTreesInPath(ArrayList<String> board, TobogganTestCase testCase) {
    return countTreesInPath(board, testCase.getxStart(), testCase.getyStart(), testCase.getxVelocity(), testCase.getyVelocity());
  }

  // Given our board, starting coordinates, and velocities, how many trees will I hit?
  private static int countTreesInPath(ArrayList<String> board, int xStart, int yStart, int xVelocity, int yVelocity) {
    int treeCount = 0; // Counter

    int x = xStart; // Current x coord
    int y = yStart; // Current y coord

    for (int i = yStart; i < board.size(); i+= yVelocity) {
      if(isTree(board, x, y)) {
        treeCount++; // We found a tree
      }
      // Move the toboggan
      x += xVelocity;
      y += yVelocity;
    }
    return treeCount;
  }

  // Helper to check if the current position is a tree - also handles board looping through modulo
  private static boolean isTree(ArrayList<String> board, int x, int y) {
    int xVal = x % board.get(y).length();
    return board.get(y).charAt(xVal) == TREE_CHAR;
  }

  public static void main(String[] args) {
    try {
      var board = readBoard();
      System.out.println("--Part 1--");
      // Use the explicit values given in part 1
      var treeCountPart1 = countTreesInPath(board, 0, 0, 3, 1);
      System.out.println(treeCountPart1);

      System.out.println("--Part 2--");
      // Using our list of test cases given in part 2, count the trees, and then multiply those counts together
      testCases.stream()
              .map((TobogganTestCase testCase) -> countTreesInPath(board, testCase))
              .collect(Collectors.toList())
              .stream()
              .reduce((acc, curr) -> acc * curr)
              .ifPresent(System.out::println);

    } catch(FileNotFoundException e) {
      System.out.printf("File not found %s\n", e.getMessage());
    }
  }
}