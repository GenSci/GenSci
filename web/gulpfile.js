/**
guplfile.js
------------------------------------------------------------------------------
This file defines those tasks we are using the Node package Gulp to
execute.  I primarily use Gulp to automate the collection of various
Javascript files into a few, minified .js files.  Additionally I am trying
to get better at using SASS and also breaking out my compiled style
sheets into smaller, more managable components.
*/
// Loading Gulp
var gulp = require('gulp');
// And invidivual packages
var jshint = require('gulp-jshint');
var sass = require('gulp-sass');
var concat = require('gulp-concat');
var uglify = require('gulp-uglify');
var rename = require('gulp-rename');


//Javascript Lint task
gulp.task('jslint', function() {
    return gulp.src('static/source/*.js')
        .pipe(jshint())
        .pipe(jshint.reporter('default'));
});

// Sass compiling task
gulp.task('sass', function() {
    return gulp.src('static/scss/**/*.scss')
        .pipe(concat('main.css'))
        .pipe(sass())
        .pipe(gulp.dest('static/dist/css'));
});
// Concatenating and minifying Javascript
gulp.task('scripts', function() {
    return gulp.src('static/js/source/*.js')
        .pipe(concat('main.js'))
        .pipe(gulp.dest('static/dist'))
        .pipe(rename('main.min.js'))
        .pipe(uglify())
        .pipe(gulp.dest('static/dist/js'));
});

// Watching files for changes
gulp.task('watch', function(){
    gulp.watch('static/js/source/*.js', ['jslint', 'scripts']);
    gulp.watch('static/scss/**/*.scss', ['sass']);
});

// Default task (runs when `gulp` is called from CLI)
gulp.task('default', ['jslint', 'sass', 'scripts', 'watch']);
