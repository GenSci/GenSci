const gulp = require('gulp');
// var gulp = require('gulp');
const sass = require('gulp-sass');
const concat = require('gulp-concat');
const rename = require('gulp-rename');
const uglify = require('gulp-uglify');
const babel = require('gulp-babel');
const minifycss = require('gulp-minify-css');
const exec = require('child_process').exec;

// Defining SASS and CSS variables
var sassFiles = 'app/_assets/scss/*.scss',
      cssDest = 'app/_assets/_dist/css/';

//Processing any SASS into CSS
function mySass(done) {
    return gulp
            .src(sassFiles)
            .pipe(sass({outputStyle: "expanded"}))
            .pipe(gulp.dest(cssDest))
            .pipe(rename({suffix: '.min'}))
            .pipe(minifycss())
            .pipe(gulp.dest(cssDest));
            done();
}

// JS script paths
var jsFiles = 'app/_assets/js/*.js',
      jsDest = 'app/_assets/_dist/js/';

function myScripts(done) {
    return gulp
            .src(jsFiles)
            .pipe(babel({presets: ['env']}))
            .pipe(concat('scripts.js'))
            .pipe(gulp.dest(jsDest))
            .pipe(rename('scripts.min.js'))
            .pipe(uglify())
            .pipe(gulp.dest(jsDest));
            done();
}

// Using the Django command to collect various static files into a central repository.
function collectStatic(done) {
    exec('docker exec gs_app python3 manage.py collectstatic --noinput', function(stderr, stdout) {
        console.log(stdout);
        console.log(stderr);
        done();
    });
}

const compileScripts = gulp.parallel(mySass, myScripts)
compileScripts.descriptionb = 'Compiling SCSS and JS files'

const compCollect = gulp.series(compileScripts, collectStatic)
compCollect.description = 'Compiling and then collecting static files'

// Watching app specific static file directories and running the Django command to collect them in the static directory as well as watching our general SCSS and JS directories.
const watchJS = () => { gulp.watch(jsFiles, compCollect); }
const watchSCSS = () => { gulp.watch(sassFiles, compCollect); }
const watchApps = () => {
    // Watching individual app's static directories
}
const watch = gulp.parallel(watchJS, watchSCSS, watchApps);

const defaultTask = gulp.series(compCollect, watch);

exports.default = defaultTask
