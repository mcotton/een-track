(function($) {

    startupTime     =   new Date()

    $.fn.tracker = function(mode, options) {

        // use the defaults or customized options if they exist
        var options     =   options || {},
            debug       =   options.debug || true

        function stopTracking() {
          var stopTime = new Date()


          if(debug) {
            console.log('running time: ', stopTime - startupTime)
          }

          debugger

          $.ajax('https://een-track.appspot.com/upload/console', {
            type: 'POST',
            success: function(data) { console.log('success: ', data) },
            error: function(data) { console.log('error: ', data) },
            data: {
              'useable': stopTime - startupTime
            },
            dataType: 'json'
          });

        }

        switch(mode) {
          case 'stop':
            stopTracking()
            break
        }

        //return this to make it chainable
        return this;
    }

}(jQuery));
