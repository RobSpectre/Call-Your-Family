module.exports = function(grunt) {
    var port = grunt.option('port') || 8000;
    // Project configuration
    grunt.initConfig({
        sass: {
            theme: {
                files: {
                'static/styles/index.css': 'static/materialize/sass/materialize.scss'
                }
            }
        },
        jshint: {
            files: [ 'Gruntfile.js', 'static/jss/*.js'],
            options: {
                globals: {
                    jQuery: true,
                    console: true
                }
            }
        },
        open: {
            delayed: {
                path: 'http://localhost:5000',
                options: {
                    openOn: 'serverListening'
                }
            }
        },
        watch: {
            options: {
                livereload: true
            },
            js: {
                files: [ 'Gruntfile.js', 'static/js/*.js' ],
                tasks: 'jshint'
            },
            theme: {
                files: [ 'static/materialize/sass/components/*.scss' ],
                tasks: 'sass'
            },
            html: {
                files: [ 'templates/*.html']
            }
        },
    });

    grunt.loadNpmTasks( 'grunt-sass' );
    grunt.loadNpmTasks( 'grunt-contrib-watch' );
    grunt.loadNpmTasks( 'grunt-contrib-jshint' );
    grunt.loadNpmTasks( 'grunt-open' );
    grunt.loadNpmTasks( 'grunt-connect' );

    grunt.registerTask( 'default', [ 'sass', 'jshint' ] );

    grunt.registerTask('flask', 'Run flask server.', function() {
       var spawn = require('child_process').spawn;
       grunt.log.writeln('Starting Flask development server.');
       // stdio: 'inherit' let us see flask output in grunt
       process.env.FLASK_YEOMAN_DEBUG = 1;
       var PIPE = {stdio: 'inherit'};
       spawn('python', ['app.py'], PIPE);
       grunt.event.emit('serverListening');
    });

    grunt.registerTask( 'serve', [ 'open', 'flask', 'watch', 'connect' ] );
};
