const fs = require("fs");

const FILENAME = "./input.txt"; // Our input file

function parseFile() {
  // Read in the input file
  const fileContent = fs.readFileSync(FILENAME, {
    encoding: "utf-8",
    flag: "r",
  });
  // Split into lines
  const splitContent = fileContent.split("\n");

  // The first line is the closest time I can leave the port
  const nearestLeaveTime = parseInt(splitContent[0]);

  // This line is for all the buses that aren't 'x' or closed out
  const activeBuses = splitContent[1]
    .replace(/x,/gi, "")
    .split(",")
    .map((busStr) => parseInt(busStr));

  // This includes the 'x' buses
  const allBuses = splitContent[1]
    .split(",")
    .map((busStr) => (busStr === "x" ? busStr : parseInt(busStr)));

  // Return all
  return { nearestLeaveTime, activeBuses, allBuses };
}

// Finds the closest bus after the given time.
function findClosestBusTo(buses, time) {
  // Minimum bus and minimum time.
  let minBus;
  let minTime = Infinity;
  // Loop through the buses
  buses.forEach((bus) => {
    // If the next time the bus arrives is less than the min, update them
    const busRouteCount = Math.ceil(time / bus);
    const nextTime = bus * busRouteCount;
    if (nextTime < minTime) {
      minTime = nextTime;
      minBus = bus;
    }
  });
  // Return the values
  return { nextBus: minBus, waitTime: minTime - time };
}

// LCM function
function leastCommonMultiple(n1, n2) {
  let gcf = 1;
  // Find the greatest common factor, then return the product of the numbers divided by it
  for (let i = 1; i <= n1 && i <= n2; i++) {
    if (n1 % i === 0 && n2 % i === 0) gcf = i;
  }

  return (n1 * n2) / gcf;
}

function findSubsequentBusTime(buses) {
  let starterTime = buses[0]; // The time
  let currentIndex = 1; // Current index in the buses array
  let addend = buses[0]; // Addend - will be the GCF of the different bus times

  // Run through the bus length
  while (currentIndex < buses.length) {
    // If the current bus is out of commission, move to the next one
    if (isNaN(buses[currentIndex])) {
      currentIndex++;
    }
    // If the current start time works for our current index...
    else if ((starterTime + currentIndex) % buses[currentIndex] === 0) {
      // Update our addend, and move to the next bus
      addend = leastCommonMultiple(addend, buses[currentIndex]);
      currentIndex++;
    }
    // Otherwise, keep incrementing our start time
    else {
      starterTime += addend;
    }
  }

  return starterTime;
}

function main() {
  const { nearestLeaveTime, activeBuses, allBuses } = parseFile();

  console.log("--Part 1--");
  const { nextBus, waitTime } = findClosestBusTo(activeBuses, nearestLeaveTime);
  console.log("ID * wait time = ", nextBus * waitTime);

  console.log("--Part 2--");
  const time = findSubsequentBusTime(allBuses);
  console.log(time);
}

main();
