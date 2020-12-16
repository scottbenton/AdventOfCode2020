const { performance } = require("perf_hooks");

function findNthSpokenWordUsingObjects(starter, n) {
  let lastSeenIndexes = {};
  starter.slice(0, starter.length - 1).forEach((value, idx) => {
    lastSeenIndexes[value] = idx;
  });

  let lastNumber = starter[starter.length - 1];
  for (i = starter.length; i < n; i++) {
    const lastSeenAt = lastSeenIndexes[lastNumber];
    const currentValue = lastSeenAt >= 0 ? i - 1 - lastSeenAt : 0;
    lastSeenIndexes[lastNumber] = i - 1;
    lastNumber = currentValue;
  }

  return lastNumber;
}

function findNthSpokenWordUsingMaps(starter, n) {
  let lastSeenIndexes = new Map();
  starter.slice(0, starter.length - 1).forEach((value, idx) => {
    lastSeenIndexes.set(value, idx);
  });

  let lastNumber = starter[starter.length - 1];
  for (i = starter.length; i < n; i++) {
    const lastSeenAt = lastSeenIndexes.get(lastNumber);
    const currentValue = lastSeenAt >= 0 ? i - 1 - lastSeenAt : 0;
    lastSeenIndexes.set(lastNumber, i - 1);
    lastNumber = currentValue;
  }

  return lastNumber;
}

function printExecutionTimes(input, n) {
  console.log(`Times for ${n} items:`);

  let objectT0 = performance.now();
  findNthSpokenWordUsingObjects(input, n);
  let objectT1 = performance.now();

  console.log(`Object: ${objectT1 - objectT0} milliseconds`);

  let mapT0 = performance.now();
  findNthSpokenWordUsingMaps(input, n);
  let mapT1 = performance.now();

  console.log(`Map: ${mapT1 - mapT0} milliseconds`);
}

function main() {
  const input = [14, 3, 1, 0, 9, 5]; // No file today, just this :)

  // Solution Using Objects
  // console.log("--Part 1--");
  // const number2020 = findNthSpokenWordUsingObjects(input, 2020);
  // console.log("2020th spoken number: " + number2020);

  // console.log("--Part 2--");
  // const number30000000 = findNthSpokenWordUsingObjects(input, 30000000);
  // console.log("30000000th spoken word: " + number30000000);

  // Solution using maps
  console.log("--Part 1--");
  const number2020 = findNthSpokenWordUsingMaps(input, 2020);
  console.log("2020th spoken number: " + number2020);

  console.log("--Part 2--");
  const number30000000 = findNthSpokenWordUsingMaps(input, 30000000);
  console.log("30000000th spoken word: " + number30000000);

  // Prints execution times for objects and for maps
  // printExecutionTimes(input, 30000000);
}

main();
