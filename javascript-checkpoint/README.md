# JavaScript Algorithm Functions

This document provides a detailed breakdown of the algorithms implemented in `index.js`. Each section describes the purpose of a function, the steps in its algorithm, and provides the JavaScript implementation.

## Table of Contents

1.  String Functions
    - `reverseString`
    - `countCharacters`
    - `capitalizeWords`
2.  Array Functions
    - `findMaxAndMin`
    - `sumArray`
    - `filterOddNumbers`
3.  Mathematical Functions
    - `isPrime`
    - `factorial`
    - `fibonacci`

---

## String Functions

### `reverseString(str)`

This function reverses a given string.

**Algorithm Steps:**

1.  Initialize an empty string, `reversedString`, to store the reversed result.
2.  Handle the edge case where the string is empty or has only one character by returning the string itself.
3.  Iterate through the input string `str` backwards, from the last character to the first.
4.  Concatenate each character to `reversedString`.
5.  Return the `reversedString`.

**Implementation:**

```javascript
function reverseString(str) {
  let reversedString = "";

  if (str.length <= 1) return str;

  for (let i = str.length - 1; i >= 0; i--) {
    reversedString += str[i];
  }

  return reversedString;
}
```

### `countCharacters(str)`

This function counts the number of non-space characters in a string.

**Algorithm Steps:**

1.  Initialize a counter `totalChars` to zero.
2.  Loop through each character of the string `str`.
3.  Inside the loop, if the character is not a space, increment `totalChars`.
4.  After the loop finishes, return `totalChars`.

**Implementation:**

```javascript
function countCharacters(str) {
  let totalChars = 0;

  for (let i = 0; i < str.length; i++) {
    if (str[i] !== " ") {
      totalChars += 1;
    }
  }

  return totalChars;
}
```

### `capitalizeWords(sentence)`

This function capitalizes the first letter of each word in a given sentence.

**Algorithm Steps:**

1.  Initialize an empty string `capitalizedSentence`.
2.  Iterate through each character of the `sentence`.
3.  For each character, check if it's the first character of the sentence or if the preceding character was a space.
4.  If it is, convert the character to uppercase and append it to `capitalizedSentence`.
5.  Otherwise, append the character in its original case.
6.  Return `capitalizedSentence` after the loop.

**Implementation:**

```javascript
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
```

---

## Array Functions

### `findMaxAndMin(arrNums)`

This function finds the maximum and minimum numbers in an array.

**Algorithm Steps:**

1.  If the array is empty, return `null`.
2.  Initialize `max` and `min` with the first element of the array.
3.  Iterate through the array starting from the second element.
4.  In each iteration, if the current element is greater than `max`, update `max`.
5.  If the current element is less than `min`, update `min`.
6.  Return an object containing the `max` and `min` values.

**Implementation:**

```javascript
function findMaxAndMin(arrNums) {
  if (arrNums.length === 0) {
    return null;
  }

  let max = arrNums;
  let min = arrNums;

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
```

### `sumArray(arrNums)`

This function calculates the sum of all numbers in an array.

**Algorithm Steps:**

1.  Initialize a variable `sum` to 0.
2.  Iterate through each number in the `arrNums` array.
3.  Add each number to `sum`.
4.  Return `sum`.

**Implementation:**

```javascript
function sumArray(arrNums) {
  let sum = 0;

  for (let i = 0; i < arrNums.length; i++) {
    sum += arrNums[i];
  }

  return sum;
}
```

### `filterOddNumbers(arrNums)`

This function filters out all the odd numbers from an array.

**Algorithm Steps:**

1.  Initialize an empty array `oddNums`.
2.  Iterate through each number in `arrNums`.
3.  For each number, check if it is odd using the modulo operator (`% 2 !== 0`).
4.  If it is odd, push it to the `oddNums` array.
5.  Return `oddNums`.

**Implementation:**

```javascript
function filterOddNumbers(arrNums) {
  let oddNums = [];

  for (let i = 0; i < arrNums.length; i++) {
    if (arrNums[i] % 2 !== 0) {
      oddNums.push(arrNums[i]);
    }
  }

  return oddNums;
}
```

---

## Mathematical Functions

### `isPrime(num)`

This function checks if a number is a prime number.

**Algorithm Steps:**

1.  Numbers less than or equal to 1 are not prime, so return `false`.
2.  The number 2 is the only even prime, so return `true`.
3.  All other even numbers are not prime, so return `false`.
4.  For odd numbers, iterate from 3 up to the square root of the number, incrementing by 2.
5.  If `num` is divisible by any number in this loop, it's not prime, so return `false`.
6.  If the loop completes, the number is prime, so return `true`.

**Implementation:**

```javascript
function isPrime(num) {
  if (num <= 1) return false;
  if (num === 2) return true;
  if (num % 2 === 0) return false;

  const boundary = Math.sqrt(num);
  for (let i = 3; i <= boundary; i += 2) {
    if (num % i === 0) return false;
  }

  return true;
}
```

### `factorial(num)`

This function calculates the factorial of a given number.

**Algorithm Steps:**

1.  Handle base cases: if the number is 0 or 1, return 1.
2.  Initialize `result` to 1.
3.  Iterate from the number down to 1.
4.  Multiply `result` by the current number in each iteration.
5.  Return `result`.

**Implementation:**

```javascript
function factorial(num) {
  if (num <= 1) return 1;

  let result = 1;
  for (let i = num; i > 0; i--) {
    result *= i;
  }

  return result;
}
```

### `fibonacci(n)`

This function generates the Fibonacci sequence up to `n` terms.

**Algorithm Steps:**

1.  Handle edge cases for `n` being 0 or 1.
2.  Initialize a `sequence` array with the first two Fibonacci numbers, `[0, 1]`.
3.  Loop from `i = 2` up to `n`.
4.  In each iteration, calculate the next Fibonacci number by summing the previous two numbers in the sequence.
5.  Push the `next` number into the `sequence` array.
6.  Return the `sequence`.

**Implementation:**

```javascript
function fibonacci(n) {
  if (n <= 0) {
    return [];
  }

  if (n === 1) {
    return;
  }

  const sequence =;

  for (let i = 2; i < n; i++) {
    const next = sequence[i - 1] + sequence[i - 2];
    sequence.push(next);
  }

  return sequence;
}
```
