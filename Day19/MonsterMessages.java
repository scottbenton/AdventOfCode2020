import java.io.File;
import java.io.FileNotFoundException;
import java.util.*;
import java.util.regex.Pattern;
import java.util.stream.Collectors;

public class MonsterMessages {
    private static final String FILENAME = "./input.txt";

    private static FileReturn parseMessages() throws FileNotFoundException {
        // A list of instructions
        ArrayList<String> unparsedRules = new ArrayList<>();
        List<String> messages = new ArrayList<>();
        // Read in the file
        File inputFile = new File(FILENAME);
        Scanner scanner = new Scanner(inputFile);

        // Parse out each part into a list
        boolean isPart1 = true;
        while (scanner.hasNextLine()) {
            var line = scanner.nextLine();
            if(line.isEmpty()) isPart1 = false;
            else if(isPart1) unparsedRules.add(line);
            else messages.add(line);
        }

        // Parse rules into their Class, then into a map for easy access
        Map<Integer, FileRules> rules = unparsedRules.stream().map(FileRules::new).collect(Collectors.toMap(FileRules::getKey, (FileRules x) -> x));
//        rules.values().forEach(rule -> rule.collectPossibilities(rules));
        // Parse through the rules.
        return new FileReturn(rules, messages);
    }

    // For the given rule, count the valid messages
    private static Integer countValidMessagesForRule(Map<Integer, FileRules>ruleMap, Integer ruleKey, List<String> messages) {
        // Get the regex and compile it
        var regex = ruleMap.get(ruleKey).getRegex(ruleMap);
        var pattern = Pattern.compile(regex);
        // Check each message against our regular expression
        long count = messages.stream().filter(message -> pattern.matcher(message).find()).count();
        return (int) count;
    }

    public static void main(String[] args) throws FileNotFoundException {
        var rulesAndMessages = parseMessages();
        var rules = rulesAndMessages.rules;
        var messages = rulesAndMessages.messages;

        System.out.println("--Part 1--");
        var validMessagesPart1 = countValidMessagesForRule(rules, 0, messages);
        System.out.println(validMessagesPart1);

        // Make changes to data for part 2
        rules.put(8, new FileRules("8: 42 | 42 8"));
        rules.put(11, new FileRules("11: 42 31 | 42 11 31"));

        System.out.println("--Part 2--");
        var validMessagesPart2 = countValidMessagesForRule(rules, 0, messages);
        System.out.println(validMessagesPart2);
    }
}

// Helper class for part 1 return
class FileReturn {
    Map<Integer, FileRules> rules;
    List<String> messages;

    public FileReturn(Map<Integer, FileRules> rules, List<String> messages) {
        this.rules = rules;
        this.messages = messages;
    }
}

// Class for storing the Rules
class FileRules {
    private final Integer key; // The key of the rule
    private List<List<Integer>> rules; // List of rules, grouped
    private String character; // If it doesn't have rules, just a character
    private String regexChecker; // Regular expression for this FileRule

    // Constructor, parses a rule into the above fields
    public FileRules(String unparsedRule) {
        var keySplit = unparsedRule.split(": ");
        this.key = Integer.parseInt(keySplit[0]);
        var ruleGroups = keySplit[1].split("\\|");
        if(ruleGroups[0].equals("\"a\"") || ruleGroups[0].equals("\"b\"")) {
            character = ruleGroups[0].replaceAll("\"", "");
        } else {
            rules = Arrays.stream(ruleGroups)
                    .map(groupString -> Arrays.stream(groupString.split(" "))
                            .filter(str -> !str.isEmpty())
                            .map(Integer::parseInt)
                            .collect(Collectors.toList()))
                    .collect(Collectors.toList());
        }
    }

    // Creates a regular expression for the rule
    public String createRegex(Map<Integer, FileRules> rulesMap, int recursionDepth){
        // If this is just a character, return it
        if(character != null) {
            regexChecker = character;
            return character;
        }
        // Ok, lets build this regex
        else {
            StringBuilder regex = new StringBuilder();
            regex.append("(");
            // For each possible set of rules
            rules.forEach(ruleGroup -> {
                // Loop through each Rule in the list
                ruleGroup.forEach(ruleKey-> {
                    // For part 2, kinda hacky, but I set a max recursion length of 10
                    // Either way, it will call createRegex on the rule and add it.
                    if(ruleKey.equals(key) && recursionDepth < 10) {
                        regex.append(rulesMap.get(ruleKey).createRegex(rulesMap, recursionDepth + 1));
                    } else if(recursionDepth < 10) {
                        regex.append(rulesMap.get(ruleKey).createRegex(rulesMap, 0));
                    }
                });
                // Or our groups together
                regex.append("|");
            });
            // Remove the trailing or and add a )
            regex.deleteCharAt(regex.length()-1);
            regex.append(")");
            regexChecker = regex.toString();
            return regexChecker;
        }
    }

    public String getRegex(Map<Integer, FileRules> ruleMap) {
        // Create a regex, then return it.
        createRegex(ruleMap, 0);
        return "^" + regexChecker + "\\b";
    }

    // Return the key
    public Integer getKey(){
        return this.key;
    }

    public String toString() {
        return key + ": " + (character != null ? character : rules.toString()) + "\n";
    }
}