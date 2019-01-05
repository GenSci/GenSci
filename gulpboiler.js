import gulp from 'gulp'

const compileMarkup = () => { // COMPILE MARKUP }
const compileScript = () => { // COMPILE SCRIPT }
const compileStyle = () => { // COMPILE STYLE }

const watchMarkup = () => { // WATCH MARKUP }
const watchScript = () => { // WATCH SCRIPT }
const watchStyle = () => { // WATCH STYLE }

const compile = gulp.parallel(compileMarkup, compileScript, compileStyle)
compile.description = 'compile all sources'

// Not exposed to CLI
const startServer = () => { // START SERVER }

const serve = gulp.series(compile, startServer)
serve.description = 'serve compiled source on local server at port 3000'

const watch = gulp.parallel(watchMarkup, watchScript, watchStyle)
watch.description = 'watch for changes to all source'

const defaultTasks = gulp.parallel(serve, watch)

export {
  compile,
  compileMarkup,
  compileScript,
  compileStyle,
  serve,
  watch,
  watchMarkup,
  watchScript,
  watchStyle,
}

export default defaultTasks
