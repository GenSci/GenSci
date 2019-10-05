/*
THIS IS A TEST

*/

var Test = (function() {
    const myTest = 'This is my test';

    function showTest() {
        return myTest;
    }
    return{
        myTest: myTest,
        showTest: showTest
    };
}());
