var astart = false;
var apause = false;
var astop = false;

window.onload = function () {
    "use strict";
      var a_start = document.getElementById("start");
      var a_pause = document.getElementById("pause");
      var a_stop = document.getElementById("stop");
      a_start.onclick = function () {
          if(astart != true)
          {
              astart = true;
              astop = false;
              apause = false;
              document.getElementById("start").style.background ='#3c8dbc';
              document.getElementById("pause").style.background ='#f4f4f4';
              document.getElementById("stop").style.background ='#f4f4f4';
              $.ajax({
                    url: 'start_recording/',
                    dataType: 'json'
                });
          }
      };
      a_pause.onclick = function () {
          if(apause != true)
          {
              apause = true;
              astart = false;
              astop = false;
              document.getElementById("start").style.background ='#f4f4f4';
              document.getElementById("pause").style.background ='#3c8dbc';
              document.getElementById("stop").style.background ='#f4f4f4';
              $.ajax({
                    url: 'pause_recording/',
                    dataType: 'json'
                });
          }

      };
      a_stop.onclick = function () {
          if(astop != true)
          {
              astop = true;
              astart = false;
              apause = false;
              document.getElementById("start").style.background ='#f4f4f4';
              document.getElementById("pause").style.background ='#f4f4f4';
              document.getElementById("stop").style.background ='#3c8dbc';
              $.ajax({
                    url: 'stop_recording/',
                    dataType: 'json'
                });
          }
      };

    };

window.onbeforeunload = function (event) {
    "use strict";
    $.ajax({
                url: 'send_command/',
                data: {
                    'command': 'deactivate'
                },
                dataType: 'json'
            });
};