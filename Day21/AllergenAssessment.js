const fs = require("fs");
const FILENAME = "./input.txt";

// Food item class
class FoodItem {
  // Constructs from an input file line
  constructor(line) {
    let splitLine = line.split("(");
    // Split out each ingredient, filtering empty strings
    this.ingredients = splitLine[0]
      .split(" ")
      .filter((ingredient) => !!ingredient);
    // Filter out the allergens
    this.allergens = splitLine[1].replace(/contains |\)/g, "").split(", ");
  }

  // Returns an allergen map which maps each allergen to each ingredient
  get allergenMap() {
    let map = {};
    this.allergens.forEach((allergen) => {
      map[allergen] = this.ingredients;
    });
    return map;
  }
}

function parseFile() {
  const foodItems = [];
  // Read in the input file
  const fileContent = fs.readFileSync(FILENAME, {
    encoding: "utf-8",
    flag: "r",
  });
  // Split into lines, parse each line into a food item
  fileContent.split("\n").map((line) => {
    if (line) foodItems.push(new FoodItem(line));
  });

  return foodItems;
}

// Unions maps, upon key overlaps intersects the arrays to filter out the allergens
function filterAllergenMap(foodItems) {
  let globalMap = {};

  foodItems.forEach((item) => {
    const itemMap = item.allergenMap;
    // Union keys, intersect overlapping values
    Object.keys(itemMap).forEach((itemKey) => {
      if (globalMap[itemKey]) {
        // Intersect two arrays
        let newAllergenArr = globalMap[itemKey].filter((ingredient) =>
          itemMap[itemKey].includes(ingredient)
        );
        globalMap[itemKey] = newAllergenArr;
      } else {
        // Union if not exists
        globalMap[itemKey] = itemMap[itemKey];
      }
    });
  });

  return globalMap;
}
// Turns allergen: [allPossibleIngredients] to ingredient: [allPossibleAllergens]
function invertAllergenMap(allergenMap) {
  let ingredientMap = {};
  Object.keys(allergenMap).forEach((allergenKey) => {
    allergenMap[allergenKey].forEach((ingredient) => {
      if (ingredientMap[ingredient]) {
        ingredientMap[ingredient].push(allergenKey);
      } else {
        ingredientMap[ingredient] = [allergenKey];
      }
    });
  });
  return ingredientMap;
}

// Counts all ingredients that can't be allergens
function countNonAllergens(foodItems, allergenMap) {
  let count = 0;
  const ingredientMap = invertAllergenMap(allergenMap);
  // If the item isn't in the allergen list add one to the count
  foodItems.forEach((item) => {
    count += item.ingredients.filter((ingredient) => !ingredientMap[ingredient])
      .length;
  });

  return count;
}

// Narrows down our allergens and ingredients until we can map 1:1
function findAllergenIngredients(allergenMap) {
  let allergenCopy = { ...allergenMap };
  let finalAllergens = {};
  // While we haven't found all our allergens yet...
  while (
    Object.keys(finalAllergens).length !== Object.keys(allergenCopy).length
  ) {
    // Go through our allergens
    Object.keys(allergenCopy).forEach((allergenKey) => {
      const allergenArr = allergenCopy[allergenKey];
      // If our allergen is only 1 long, add it to the finalAllergens
      if (allergenArr.length === 1) {
        finalAllergens[allergenArr[0]] = allergenKey;
        allergenCopy[allergenKey] = [];
      }
      // Make sure we filter out all used allergens
      else {
        allergenCopy[allergenKey] = allergenArr.filter(
          (ingredient) => !finalAllergens[ingredient]
        );
      }
    });
  }
  return finalAllergens;
}

// For part 2, prints all allergen ingredients sorted alphabetically by the english name
function allergenString(finalAllergenMap) {
  return Object.keys(finalAllergenMap)
    .sort((a, b) => finalAllergenMap[a].localeCompare(finalAllergenMap[b]))
    .join(",");
}

function main() {
  let foodItems = parseFile();
  let allergenMap = filterAllergenMap(foodItems);

  console.log("--Part 1--");
  const nonAllergenCount = countNonAllergens(foodItems, allergenMap);
  console.log(`Non Allergens show up ${nonAllergenCount} times.`);

  console.log("--Part 2--");
  const finalAllergens = findAllergenIngredients(allergenMap);
  console.log(allergenString(finalAllergens));
}
main();
