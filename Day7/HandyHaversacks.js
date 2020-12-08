const fs = require("fs");
const readline = require("readline");

const FILENAME = "./input.txt"; // Our input file
const IMPORTANT_COLOR = "shiny gold"; // The color our problem revolves around

/*
Data structure definition 
{
  [bagColor]: {
    parents: ["parentColor1", "parentColor2"],
    rules: [
      {
        number: 4,
        color: "childColor1"
      },
      {
        number: 3,
        color: "childColor2"
      }
    ]
  }
}
*/

async function parseFile() {
  // Create a fileStream, and a line by line reader
  const fileStream = fs.createReadStream(FILENAME);
  const rl = readline.createInterface({
    input: fileStream,
    crlfDelay: Infinity,
  });

  // Push each line to the array.
  const lines = [];
  for await (const line of rl) {
    lines.push(line);
  }

  return lines;
}

// Removes the last word in a string. In the string "Lazy dog jumps over fox", the word "fox" will be removed
function removeLastWord(str) {
  const idx = str.lastIndexOf(" ");
  return str.substr(0, idx).trim();
}

// Splits "4 dirty brown" into {number: 4, color: "dirty brown"}
function splitNumberFromString(str) {
  // Index of the first space
  const idx = str.indexOf(" ");
  return {
    number: parseInt(str.substr(0, idx).trim()),
    color: str.substr(idx).trim(),
  };
}

// Parses a line from the file into an object
function parseRule(rule) {
  const splitter = new RegExp(" contain |,", "g");
  const splitRule = rule.split(splitter);

  const parentBag = removeLastWord(splitRule[0]);
  let rules = [];
  for (let i = 1; i < splitRule.length; i++) {
    if (!splitRule[i].includes("no other bags")) {
      rules.push(splitNumberFromString(removeLastWord(splitRule[i])));
    }
  }

  return { parent: parentBag, rules };
}

// Creates a map of all the different parents and rules for a given color
function createMapFromRules(unparsedRules) {
  let ruleMap = {};
  // For each unparsed rules
  unparsedRules.forEach((rule) => {
    // Parse out the rule
    const parsedRule = parseRule(rule);
    const { parent, rules } = parsedRule;
    // Add the rules to the rule map
    ruleMap[parent] = { ...ruleMap[parent], rules: rules };
    rules.forEach((parsedChildRule) => {
      const { color } = parsedChildRule;
      // Add the current color to the parents array of its children
      ruleMap[color] = {
        ...ruleMap[color],
        parents: [...(ruleMap[color]?.parents || []), parent],
      };
    });
  });
  return ruleMap;
}

// Gathers the count of all the bags that contain the passed in color
// Travel up the tree, child to parent
function gatherContainingBags(ruleMap, bagColor) {
  let containingBags = new Set(); // List of all the bags that contain the current color
  let queue = [bagColor]; // Queue of bags to check for parents

  // While there are bags left to check
  while (queue.length > 0) {
    // Grab the next bag and remove it from the queue
    const currentRule = ruleMap[queue[0]];
    queue.shift();

    // Loop through the bag's parents, if any exist
    (currentRule.parents || []).forEach((parentColor) => {
      // If the bag color hasn't already been checked, add it to the list of bags and the queue
      if (!containingBags.has(parentColor)) {
        containingBags.add(parentColor);
        queue.push(parentColor);
      }
    });
  }
  // Return the count of possible parent bags.
  return containingBags.size;
}

// Gathers the count of all the bags that our bag needs to contain
// Travels down the tree, parent to child
function gatherChildBags(ruleMap, bagColor) {
  // Count of total bags
  let count = 0;

  // The queue contains the bag color to check, and the number of bags we need for that color
  const queue = [{ color: bagColor, number: 1 }];

  // While there are still items in the queue
  while (queue.length > 0) {
    // Extract the current bag and remove it from the queue
    const currentQueueItem = queue[0];
    const { color, number } = currentQueueItem;
    const currentBag = ruleMap[color];
    queue.shift();

    // For each child of the current node, if any exist, add the correct number of them to the queue
    // (number of current bags * number of childBags)
    (currentBag.rules || []).forEach((rule) => {
      count += number * rule.number;
      queue.push({ color: rule.color, number: number * rule.number });
    });
  }
  // Return the count
  return count;
}

async function main() {
  const rules = await parseFile();
  const ruleMap = createMapFromRules(rules);

  console.log("--Part 1--");
  const containingCount = gatherContainingBags(ruleMap, IMPORTANT_COLOR);
  console.log(containingCount);

  console.log("--Part 2");
  const childCount = gatherChildBags(ruleMap, IMPORTANT_COLOR);
  console.log(childCount);
}

main();
