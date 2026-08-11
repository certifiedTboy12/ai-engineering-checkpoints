// STRING Functions

/**
 * @function reverseString
 * @description the function revereses a string in the opposite direction
 * @param {string} str The string to be reversed
 * @return {string} the reversed string
 */
function reverseString(str) {
  let reversedString = "";

  if (str.length <= 1) return str;

  for (let i = str.length - 1; i >= 0; i--) {
    reversedString += str[i];
  }

  return reversedString;
}

console.log(reverseString("Hello, World!"));

/**
 * @function countCharacters
 * @description the function counts the total number of valid character in a string
 * @param {string} str The string that the character is to be counted
 * @return {number} totalChars
 */
function countCharacters(str) {
  let totalChars = 0;

  for (let i = 0; i < str.length; i++) {
    if (str[i] !== " ") {
      totalChars += 1;
    }
  }

  return totalChars;
}

console.log(countCharacters("Hello, World!"));

/**
 * @function capitalizeWords
 * @description capitalize each word in a given sentence
 * @param {string} sentence
 * @return {string} captilizedSentence
 */
function capitalizeWords(sentence) {
  let capitalizedSentence = "";

  for (let i = 0; i < sentence.length; i++) {
    if (sentence[i - 1] === " " || i === 0) {
      capitalizedSentence += sentence[i].toUpperCase();
    } else {
      capitalizedSentence += sentence[i];
    }
  }

  return capitalizedSentence;
}

console.log(capitalizeWords("hello, world!, how are you doing today?"));

// ARRAY Functions

/**
 * @function findMaxAndMin
 * @description finds the maximum and minimum value in a array
 * @param {number[]} arrNums
 */
function findMaxAndMin(arrNums) {
  if (arrNums.length === 0) {
    return null;
  }

  let max = arrNums[0];
  let min = arrNums[0];

  for (let i = 1; i < arrNums.length; i++) {
    if (arrNums[i] > max) {
      max = arrNums[i];
    }

    if (arrNums[i] < min) {
      min = arrNums[i];
    }
  }

  return { max, min };
}

console.log(findMaxAndMin([40, 10, 30, 12, 31, 40]));

/**
 * @function sumArray
 * @description a function that adds all the number values in an array
 * @param {number[]} arrNums
 * @return {number} sum
 */
function sumArray(arrNums) {
  let sum = 0;

  for (let i = 0; i < arrNums.length; i++) {
    sum += arrNums[i];
  }

  return sum;
}

console.log(sumArray([1, 2, 3, 4, 5]));

/**
 * @function filterOddNumbers
 * @description filter the odd numbers in a set of numbers
 * @param {number[]} arrNums
 * @return {number[]} oddNums
 */
function filterOddNumbers(arrNums) {
  let oddNums = [];

  for (let i = 0; i < arrNums.length; i++) {
    if (arrNums[i] % 2 !== 0) {
      oddNums.push(arrNums[i]);
    }
  }

  return oddNums;
}

console.log(filterOddNumbers([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]));

// Mathematical Functions

/**
 * @function isPrime
 * @description checks if a number is a prime number
 * @param {number} num
 * @return {boolean} true | false
 */
function isPrime(num) {
  // Numbers less than or equal to 1 are not prime
  if (num <= 1) return false;

  // 2 is the only even prime number
  if (num === 2) return true;

  // Exclude all other even numbers
  if (num % 2 === 0) return false;

  // Check odd numbers up to the square root of num
  const boundary = Math.sqrt(num);
  for (let i = 3; i <= boundary; i += 2) {
    if (num % i === 0) return false;
  }

  return true;
}

// Examples:
console.log(isPrime(11)); // true
console.log(isPrime(4)); // false
console.log(isPrime(1)); // false

/**
 * @function factorial
 * @description finds the factionrial of a given number
 * @param {number} num
 * @return {number} result
 */

function factorial(num) {
  if (num <= 0 || num === 1) return num;

  let result = 1;
  for (let i = num; i > 0; i--) {
    result *= i;
  }

  return result;
}

console.log(factorial(10));

/**
 * @function fibonacci
 * @description
 * @param {number} num
 */
function fibonacci(n) {
  if (n <= 0) {
    return [];
  }

  if (n === 1) {
    return [0];
  }

  const sequence = [0, 1];

  for (let i = 2; i < n; i++) {
    const next = sequence[i - 1] + sequence[i - 2];
    sequence.push(next);
  }

  return sequence;
}

console.log(fibonacci(10));
