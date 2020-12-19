import java.io.File;
import java.io.FileNotFoundException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Scanner;
import java.util.stream.Collectors;

public class OperationOrder {
    private static final String FILENAME = "./input.txt";

    private static ArrayList<List<String>> parseHomework() throws FileNotFoundException {
        // A list of instructions
        ArrayList<List<String>> problems = new ArrayList<>();

        // Read in the file
        File inputFile = new File(FILENAME);
        Scanner scanner = new Scanner(inputFile);

        // Parse each
        while (scanner.hasNextLine()) {
            var line = scanner.nextLine();
            problems.add(Arrays.stream(line.split("")).filter(str -> !str.equals(" ")).collect(Collectors.toList()));
        }

        return problems;
    }

    private static Long solve(List<String>problem, Boolean deferMultiplication) {
        // Make a copy so that we can mutate this List
        var problemCopy = new ArrayList<>(List.copyOf(problem));

        // Get rid of parenthesis
        if(problemCopy.contains("(")) {
            int count = 0;
            // Loop through the array
            while (count < problemCopy.size()) {
                // Once we find an opening brace...
                if (problemCopy.get(count).equals("(")) {
                    int braceCount = 1;
                    int endIdx = -1;
                    int idx = count;
                    // Find the matching closing brace
                    while (endIdx == -1) {
                        idx++;
                        var ch = problemCopy.get(idx);
                        if (ch.equals("(")) {
                            braceCount++;
                        } else if (ch.equals(")")) {
                            braceCount--;
                        }
                        if (braceCount == 0) {
                            endIdx = idx;
                        }
                    }
                    // Call this function with the subarray to get the value inside the parenthesis
                    var subSolution = solve(problemCopy.subList(count + 1, endIdx), deferMultiplication);
                    // Replace the parenthesis with the value
                    problemCopy.subList(count, endIdx + 1).clear();
                    problemCopy.add(count, subSolution.toString());
                }
                count++;
            }
        }

        // Now that the parenthesis are gone...
        while(problemCopy.size() > 1){
            // Get the next number and operation
            var number = Long.valueOf(problemCopy.get(0));
            var op = problemCopy.get(1);

            // If we are adding or multiplying, and we aren't deferring multiplication
            if(op.equals("+") || (op.equals("*") && !deferMultiplication)) {
                var number2 = Long.valueOf(problemCopy.get(2));
                long total;
                if(op.equals("+")) total = number + number2;
                else total = number * number2;
                // Replace the start of the array with either the sum or product of the two numbers
                problemCopy.subList(0, 3).clear();
                problemCopy.add(0, Long.toString(total));
            }
            // If we are deferring multiplication
            else if(op.equals("*")) {
                // Solve everything else first, then multiply
                Long number2 = solve(problemCopy.subList(2, problemCopy.size()), true);
                long total = number * number2;
                // Replace the whole array with the product
                problemCopy.clear();
                problemCopy.add(0, Long.toString(total));
            }
        }
        // Return the total
        return Long.valueOf(problemCopy.get(0));
    }

    // Calls solve with each problem in the list.
    private static List<Long> solveProblemList(List<List<String>> problems, Boolean deferMultiplication) {
        return problems.stream().map(problem -> solve(problem, deferMultiplication)).collect(Collectors.toList());
    }

    public static void main(String[] args) {
        try {
            var problems = parseHomework();
            System.out.println("--Part 1--");
            var part1Solution = solveProblemList(problems, false).stream().reduce(Long::sum).orElseThrow();
            System.out.println("Sum = " + part1Solution.toString());

            System.out.println("--Part 2--");
            var part2Solution = solveProblemList(problems, true).stream().reduce(Long::sum).orElseThrow();
            System.out.println("Sum = " + part2Solution.toString());
        } catch(FileNotFoundException e) {
            System.out.println(e.getMessage());
        }
    }
}
