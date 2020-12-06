const fs = require("fs");
const readline = require("readline");

const FILENAME = "./input.txt";

async function getSeatsFromFile() {
  // Create a fileStream, and a line by line reader
  const fileStream = fs.createReadStream(FILENAME);
  const rl = readline.createInterface({
    input: fileStream,
    crlfDelay: Infinity,
  });

  // For each line in the file, get the line's seat id, and push it to the array.
  const seats = [];
  for await (const line of rl) {
    if (line) {
      const id = getSeatID(line);
      seats.push(id);
    }
  }

  return seats;
}

// Takes a string of tree decisions, the min, the max, and the character for a min decision
function binarySearchFromString(searchString, min, max, minChar) {
  let minSearch = min;
  let maxSearch = max;

  searchString.split("").forEach((char) => {
    const half = (maxSearch + 1 - minSearch) / 2;
    char === minChar ? (maxSearch -= half) : (minSearch += half);
  });
  return minSearch;
}

// Wrappers for binarySearch
function findRow(rowString) {
  return binarySearchFromString(rowString, 0, 127, "F");
}
function findCol(colString) {
  return binarySearchFromString(colString, 0, 7, "L");
}

function getSeatID(binaryPass) {
  const row = findRow(binaryPass.substring(0, 7));
  const col = findCol(binaryPass.substring(7));
  return row * 8 + col;
}

function findMissingSeat(seatArray) {
  let counter = 1;
  // Count through the array
  while (counter < seatArray.length) {
    // If the difference between the current seat and the previous one is 2, there's a gap of one seat
    // That seat is ours, since our missing seat won't be the first or last one
    if (seatArray[counter] - seatArray[counter - 1] === 2) {
      return seatArray[counter] - 1;
    }
    counter++;
  }
  return -1;
}

async function main() {
  const seats = await getSeatsFromFile();
  console.log("--Part 1--");
  const sortedSeats = seats.sort((num1, num2) => num1 - num2);
  console.log("Max seat: " + sortedSeats[sortedSeats.length - 1]);

  console.log("--Part 2--");
  const mySeat = findMissingSeat(sortedSeats);
  console.log("My seat is: " + mySeat);
}

main();
