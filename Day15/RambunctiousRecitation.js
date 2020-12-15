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

function main() {
  const input = [14, 3, 1, 0, 9, 5]; // No file today, just this :)

  // console.log("--Part 1--");
  // const number2020 = findNthSpokenWordUsingObjects(input, 2020);
  // console.log("2020th spoken number: " + number2020);

  // console.log("--Part 2--");
  // const number30000000 = findNthSpokenWordUsingObjects(input, 30000000);
  // console.log("30000000th spoken word: " + number30000000);

  console.log("--Part 1--");
  const number2020 = findNthSpokenWordUsingMaps(input, 2020);
  console.log("2020th spoken number: " + number2020);

  console.log("--Part 2--");
  const number30000000 = findNthSpokenWordUsingMaps(input, 30000000);
  console.log("30000000th spoken word: " + number30000000);
}

main();
