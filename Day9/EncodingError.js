const fs = require("fs");
const readline = require("readline");

const FILENAME = "./input.txt"; // Our input file
const ADDEND_CHECK_COUNT = 25;

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
    lines.push(parseInt(line));
  }

  return lines;
}

function checkPreviousNForAddends(numArray, currentIndex, n) {
  if (currentIndex < n || currentIndex >= numArray.length) return false;
  else {
    numsToCheck = numArray.slice(currentIndex - 25, currentIndex);
    currNum = numArray[currentIndex];

    for (let i = 0; i < numsToCheck.length; i++) {
      checkingNumber = numsToCheck[i];
      if (checkingNumber < currNum) {
        if (numsToCheck.slice(i + 1).includes(currNum - checkingNumber)) {
          return true;
        }
      }
    }
    return false;
  }
}

function findEncodingError(numArray) {
  for (let i = ADDEND_CHECK_COUNT; i < numArray.length; i++) {
    if (!checkPreviousNForAddends(numArray, i, ADDEND_CHECK_COUNT)) {
      return numArray[i];
    }
  }
  return -1;
}

function findContiguousSet(numArray, targetNumber) {
  let total = numArray[0] + numArray[1];
  let count = 2;
  for (let i = 0; i < numArray.length - 1; i++) {
    while (total < targetNumber) {
      total += numArray[i + count];
      count++;
    }
    if (total === targetNumber) {
      return numArray.slice(i, i + count);
    } else {
      total -= numArray[i];
      if (count > 2) {
        count--;
      }
    }
  }
  return [];
}

async function main() {
  const lines = await parseFile();
  console.log("--Part 1--");
  const encodingError = findEncodingError(lines);
  console.log(encodingError);
  console.log("--Part 2--");
  const summingArray = findContiguousSet(lines, encodingError);
  const encryptionWeakness =
    Math.min(...summingArray) + Math.max(...summingArray);
  console.log(encryptionWeakness);
}

main();
