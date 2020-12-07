import java.io.File;
import java.io.FileNotFoundException;
import java.util.*;
import java.util.stream.Collectors;

public class CustomCustoms {
    private static final String FILENAME = "./input.txt";

    private static ArrayList<ArrayList<List<Character>>> parseClaimsFile() throws FileNotFoundException{
        // Alright this gets weird
        // We have a list of groups (ArrayList)
        // Each group has a list of people (ArrayList)
        // Each person has a list of claims (List<Character>)
        ArrayList<ArrayList<List<Character>>> customsClaims = new ArrayList<>();

        // Read in the file
        File inputFile = new File(FILENAME);
        Scanner scanner = new Scanner(inputFile);

        // The current group's list of claims
        ArrayList<List<Character>> currentGroupClaims = new ArrayList<>();
        while(scanner.hasNextLine()) {
            var line = scanner.nextLine();

            // If the line is just a new line, our current group is finished
            if(line.isEmpty()) {
                // Add it to the total list and start a new one
                customsClaims.add(currentGroupClaims);
                currentGroupClaims = new ArrayList<>();
            } else {
                // Otherwise, we need to add a new person's claims to the list
                currentGroupClaims.add(charListFrom(line));
            }
        }
        // Add the final claim
        customsClaims.add(currentGroupClaims);

        return customsClaims;
    }

    // Helper function, converts a string into a list of characters
    private static List<Character> charListFrom(String s) {
        return s.chars().mapToObj(e -> (char) e).collect(Collectors.toList());
    }

    // Takes the list of group claims and an operation to merge a set of claims with a line
    private static Integer getClaimsPerGroup(ArrayList<ArrayList<List<Character>>> claims, MergeOperation operation) {
        // Our list of sets of claims for each group
        int count = 0;

        // For each group, create a new set of claims, and initialize that set to the first person's claims
        for(ArrayList<List<Character>> claimsGroup: claims) {
            HashSet<Character> groupClaims = new HashSet<>(claimsGroup.get(0));

            // Add each new person's claims according to the merge operation.
            for(List<Character> claim: claimsGroup) {
                operation.parse(groupClaims, claim);
            }
            // Add the groups claims
            count += groupClaims.size();
        }
        // Count the claims in the set
        return count;
//        return claimsSet.stream().reduce(0, (acc, group) -> acc + group.size(), Integer::sum);
    }

    public static void main(String[] args){
        try {
            // Get a list of all the claims
            var claims = parseClaimsFile();

            System.out.println("--Part 1--");
            // Since we need to union the claims for part 1, our MergeOperation will be addAll
            var totalClaimsUnion = getClaimsPerGroup(claims, AbstractCollection::addAll);
            System.out.println("Total Number of Claims: " + totalClaimsUnion);

            System.out.println("--Part 2--");
            // Since we need to intersect the claims for part 2, our MergeOperation will be retainAll
            var totalClaimsIntersect = getClaimsPerGroup(claims, AbstractCollection::retainAll);
            System.out.println("Total number of Claims: " + totalClaimsIntersect);

        } catch(FileNotFoundException e) {
            System.out.println("File not found");
        }
    }
}

// Helper interface, allows us to pass lambda fuctions to getClaimsPerGroup
interface MergeOperation {
    void parse(HashSet<Character> set, List<Character> lineClaims);
}