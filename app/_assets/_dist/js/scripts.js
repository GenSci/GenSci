"use strict";

/*
THIS IS A TEST

*/
var Test = function () {
  var myTest = 'This is my test';

  function showTest() {
    return myTest;
  }

  return {
    myTest: myTest,
    showTest: showTest
  };
}();