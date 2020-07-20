var gulp = require('gulp');
var browserSync = require('browser-sync');
var reload = browserSync.reload;
var nodemon = require('gulp-nodemon');

gulp.task("node", gulp.series(done => {
    nodemon({
        script: './bin/www',
        ext: 'js html',
        env: {
            'NODE_ENV': 'development'
        }
    })
}));


gulp.task('server', gulp.series('node', done => {
    //此处的files为你所需要跟踪的文件，根据实际项目需要配置即可
    var files = [
        'views/**/*.html',
        'views/**/*.ejs',
        'views/**/*.jade',
        'public/**/*.*'
    ];
    //gulp.run(["node"]);
    browserSync.init(files, {
        proxy: 'http://localhost:4000',
        browser: 'chrome',
        notify: false,
        port: 4001 //这个是browserSync对http://localhost:3000实现的代理端口
    });
    gulp.watch(files).on("change", reload);
}));
