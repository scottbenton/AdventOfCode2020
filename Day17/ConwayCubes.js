const fs = require("fs");
const FILENAME = "./input.txt";

const ACTIVE_STATE = "#"; // Active character
const INACTIVE_STATE = "."; // Inactive character

function parseFile() {
  const lines = [];
  // Read in the input file
  const fileContent = fs.readFileSync(FILENAME, {
    encoding: "utf-8",
    flag: "r",
  });
  // Split into lines, split each line into characters
  fileContent.split("\n").map((line) => {
    if (line) lines.push(line.split(""));
  });

  return [lines];
}

// Counts all the active states in any dimension
function countActiveInNDimensions(state) {
  // While the state is an array, reduce the counts of all the substates
  if (Array.isArray(state)) {
    return state.reduce(
      (prev, current) => prev + countActiveInNDimensions(current),
      0
    );
  }
  // If the state isn't an array, we've hit bottom - check if its active or not
  else {
    if (state === ACTIVE_STATE) {
      return 1;
    } else {
      return 0;
    }
  }
}

// Constructs an empty N-Dimensional Array of a specific size
function constructEmptyNDimension(dimension, size) {
  let filledArray = Array(size).fill(INACTIVE_STATE);
  let dimensionCount = 1;
  while (dimensionCount < dimension) {
    filledArray = Array(size).fill(filledArray);
    dimensionCount++;
  }
  return filledArray;
}

// Expand a cube by two in each dimension
function expandNDimensionalCube(cubeState, dimension) {
  // If we are at the base dimension, add empty dimensions on each side
  if (dimension === 1) {
    return [INACTIVE_STATE, ...cubeState, INACTIVE_STATE];
  }
  // If we aren't at base, construct an N-Dimension array and wrap the recursive call with it
  else {
    const emptyDimension = constructEmptyNDimension(
      dimension - 1,
      cubeState[0].length + 2
    );
    let newDimension = [emptyDimension];
    cubeState.forEach((state) =>
      newDimension.push(expandNDimensionalCube(state, dimension - 1))
    );
    newDimension.push(emptyDimension);
    return newDimension;
  }
}

// Gets the minimum and maximum values to check for a point
function getMinMax(index, length) {
  const min = index > 1 ? index - 1 : 1;
  const max = index < length - 2 ? index + 1 : length - 2;
  return [min, max];
}

// Gets the value at a point in the array. PointArray is a vector
function getValueAtNDimensionalPoint(state, pointArray) {
  let currentState = state;
  pointArray.forEach((index) => {
    currentState = currentState[index];
  });
  return currentState;
}

// Counts number neighbors to a point that are active
function countActiveNDimensionalNeighbors(state, minMaxes, pointToCheck = []) {
  // If we aren't at the last dimension yet
  if (minMaxes.length > 0) {
    // Pull out our minimum and maximum for this level
    let [[min, max], ...otherMinMaxes] = minMaxes;
    // Recursive call, keep count
    let count = 0;
    for (let i = min; i <= max; i++) {
      count += countActiveNDimensionalNeighbors(state, otherMinMaxes, [
        ...pointToCheck,
        i,
      ]);
    }
    return count;
  }
  // We're at rock bottom :)
  else {
    // Get the value at the current point
    const value = getValueAtNDimensionalPoint(state, pointToCheck);
    // If the value is active, return 1
    if (value === ACTIVE_STATE) {
      return 1;
    } else {
      return 0;
    }
  }
}

// Recursively get the next state given the current one
function getNDimensionalNextState(
  fullState,
  currentState = fullState,
  currentIndex = [],
  minMaxes = []
) {
  // If we aren't at individual values yet
  if (Array.isArray(currentState)) {
    let newState = [];
    // Recurse through the array of next values, and create a new array from their returns
    for (let i = 0; i < currentState.length; i++) {
      newState.push(
        getNDimensionalNextState(
          fullState,
          currentState[i],
          [...currentIndex, i],
          [...minMaxes, getMinMax(i, currentState.length)]
        )
      );
    }
    return newState;
  }
  // If we are at an individual value
  else {
    // Find the count of active neighbors
    let activeCount = countActiveNDimensionalNeighbors(fullState, minMaxes);
    // Find the next state according to the rules
    if (currentState === ACTIVE_STATE) {
      activeCount -= 1;
      return activeCount === 2 || activeCount == 3
        ? ACTIVE_STATE
        : INACTIVE_STATE;
    } else {
      return activeCount === 3 ? ACTIVE_STATE : INACTIVE_STATE;
    }
  }
}

// Run N cycles in M dimensions and count the active states
function countActiveAfterNCycles(state, cycleCount, dimension) {
  let currentState = state;
  for (let n = 0; n < cycleCount; n++) {
    // We need to expand first to give the next group room on the board
    const expandedNextState = expandNDimensionalCube(currentState, dimension);
    currentState = getNDimensionalNextState(expandedNextState);
  }

  return countActiveInNDimensions(currentState);
}

function main() {
  const initialState = parseFile();

  console.log("--Part 1--");
  const activeAfter6d3 = countActiveAfterNCycles(initialState, 6, 3);
  console.log(`Active Cubes after 6 cycles = ${activeAfter6d3}`);

  console.log("--Part 2--");
  const activeAfter6d4 = countActiveAfterNCycles(initialState, 6, 4);
  console.log(`Active Cubes after 6 cycles = ${activeAfter6d4}`);
}

main();
