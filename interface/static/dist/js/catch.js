var keyEnum = {UP_Key: 0, DOWN_Key: 1, LEFT_Key: 2, RIGHT_Key: 3};
var keyArray = new Array(4);
var rightRequest = 0;
var leftRequest = 0;
var rightRequests = [];
var leftRequests = [];
var rightSuccess = true;
var leftSuccess = true;
var upRequests = [];
var downRequests = [];
var upPressed = false;
var downPressed = false;
var speed = 0;
var timeouts = [];
var a_start = false;
var a_pause = false;
var a_stop = false;

window.onload = function () {
      var a_start = document.getElementById("start");
      var a_pause = document.getElementById("pause");
      var a_stop = document.getElementById("stop");
      a_start.onclick = function () {
          if(a_start != true)
          {
              a_start = true;
              a_stop = false;
              a_pause = false;
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
          if(a_pause != true)
          {
              a_pause = true;
              a_start = false;
              a_stop = false;
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
          if(a_stop != true)
          {
              a_stop = true;
              a_start = false;
              a_pause = false;
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
document.getElementById("controls").onkeydown = function keyHandler(e) {
    if (event.keyCode == 37) {
        if (keyArray[keyEnum.RIGHT_Key] == true) {
            document.getElementById('arrowsbox right').classList.toggle("arrowsbox-active");
            keyArray[keyEnum.RIGHT_Key] = false;
        }
        else {
            document.getElementById('arrowsbox left').classList.add("arrowsbox-active");
            keyArray[keyEnum.LEFT_Key] = true;
            if(leftSuccess == true)
            {
                leftSuccess = false;
                leftRequest = $.ajax({
                    url: 'send_command/',
                    data: {
                        'command': 'left'
                    },
                    dataType: 'json',
                    complete: function() {
                        leftSuccess = true;
                    },
                    error: function(xhr, status, error){
                         leftSuccess = true;
                    }
                });
                leftRequests.push(leftRequest);
            }
        }
    }
    else if (event.keyCode == 32) {
        for (var i = 0 ; i < timeouts.length ; i++) {
            clearTimeout(timeouts[i]);
        }
        timeouts = [];
        if(upRequests.length != 0)
        {
            for(var i=0; i<upRequests.length; i++)
            {
                upRequests[i].abort();
                clearInterval(upRequests[i])
            }
        }
        upRequests = [];
        if(downRequests.length != 0)
        {
            for(var i=0; i<downRequests.length; i++)
            {
                downRequests[i].abort();
                clearInterval(downRequests[i])
            }
        }
        downRequests = [];
        $.ajax({
                        url: 'send_command/',
                        data: {
                          'command': 'brake'
                        },
                        dataType: 'json'
                      });
    }
    else if (event.keyCode == 39) {
        if (keyArray[keyEnum.LEFT_Key] == true) {
            document.getElementById('arrowsbox left').classList.toggle("arrowsbox-active");
            keyArray[keyEnum.LEFT_Key] = false;
        }
        else {
            document.getElementById('arrowsbox right').classList.add("arrowsbox-active");
            keyArray[keyEnum.RIGHT_Key] = true;
            if(rightSuccess == true)
            {
                rightSuccess = false;
                rightRequest = $.ajax({
                    url: 'send_command/',
                    data: {
                        'command': 'right'
                    },
                    dataType: 'json',
                    complete: function() {
                        rightSuccess = true;
                    },
                    error: function(xhr, status, error){
                         rightSuccess = true;
                    }
                });
                rightRequests.push(rightRequest);
            }
        }
    }
    else if (event.keyCode == 40) {
        if (keyArray[keyEnum.UP_Key] == true) {
            document.getElementById('arrowsbox up').classList.toggle("arrowsbox-active");
            keyArray[keyEnum.UP_Key] = false;
        }
        else {
            document.getElementById('arrowsbox down').classList.add("arrowsbox-active");
            keyArray[keyEnum.DOWN_Key] = true;
            if(downPressed == false)
            {
                downPressed = true;
                for (var i = 0 ; i < timeouts.length ; i++) {
                    clearTimeout(timeouts[i]);
                }
                timeouts = [];
                if(upRequests.length != 0)
                {
                    for(var i=0; i<upRequests.length; i++)
                    {
                        upRequests[i].abort();
                        clearInterval(upRequests[i])
                    }
                }
                upRequests = [];
                if(downRequests.length != 0)
                {
                    for(var i=0; i<downRequests.length; i++)
                    {
                        downRequests[i].abort();
                        clearInterval(downRequests[i])
                    }
                }
                downRequests = [];
                function goDown(){
                        downRequests.push($.ajax({
                        url: 'send_command/',
                        data: {
                            'command': 'down'
                        },
                        dataType: 'json',
                        success: function(data){
                        },
                        error: function(xhr, status, error){
                        },
                        complete: function (data){
                            timeouts.push(setTimeout(goDown, 2000));
                        }
                    }))
                }
                downRequests.push($.ajax({
                        url: 'send_command/',
                        data: {
                            'command': 'down'
                        },
                        dataType: 'json',
                        complete: function(data){
                         goDown();
                        }
                }));
            }
        }
    }
    else if (event.keyCode == 38) {
        if (keyArray[keyEnum.DOWN_Key] == true) {
            document.getElementById('arrowsbox down').classList.toggle("arrowsbox-active");
            keyArray[keyEnum.DOWN_Key] = false;
        }
        else {
            document.getElementById('arrowsbox up').classList.add("arrowsbox-active");
            keyArray[keyEnum.UP_Key] = true;
            if(upPressed == false)
            {
                upPressed = true;
                for (var i = 0 ; i < timeouts.length ; i++) {
                    clearTimeout(timeouts[i]);
                }
                timeouts = [];
                if(upRequests.length != 0)
                {
                    for(var i=0; i<upRequests.length; i++)
                    {
                        upRequests[i].abort();
                        clearInterval(upRequests[i])
                    }
                }
                upRequests = [];
                if(downRequests.length != 0)
                {
                    for(var i=0; i<downRequests.length; i++)
                    {
                        downRequests[i].abort();
                        clearInterval(downRequests[i])
                    }
                }
                downRequests = [];
                function goUp(){
                        upRequests.push($.ajax({
                        url: 'send_command/',
                        data: {
                            'command': 'up'
                        },
                        dataType: 'json',
                        success: function(data){
                        },
                        error: function(xhr, status, error){
                        },
                        complete: function (data){
                            timeouts.push(setTimeout(goUp, 2000));
                        }
                    }))
                }
                upRequests.push($.ajax({
                        url: 'send_command/',
                        data: {
                            'command': 'up'
                        },
                        dataType: 'json',
                        complete: function(data){
                         goUp();
                        }
                }));
            }
        }
    }
};
document.getElementById("controls").onkeyup = function (e) {
    if (event.keyCode == 37) {
        if (document.getElementById('arrowsbox left').classList.contains("arrowsbox-active")) {
            document.getElementById('arrowsbox left').classList.toggle("arrowsbox-active");
        }
        keyArray[keyEnum.LEFT_Key] = false;
        leftSuccess = true;
        if(leftRequests.length != 0 )
            {
                for(var i = 0; i < leftRequests.length; i++)
                {
                    leftRequests[i].abort();
                    clearInterval(leftRequests[i]);
                    leftRequests.splice(i, 1);
                }
            }
    }
    else if (event.keyCode == 32) {
    }
    else if (event.keyCode == 39) {
        if (document.getElementById('arrowsbox right').classList.contains("arrowsbox-active")) {
            document.getElementById('arrowsbox right').classList.toggle("arrowsbox-active");
        }
        keyArray[keyEnum.RIGHT_Key] = false;
        rightSuccess = true;
        if(rightRequests.length != 0 )
            {
                for(var i = 0; i < rightRequests.length; i++)
                {
                    rightRequests[i].abort();
                    clearInterval(rightRequests[i]);
                    rightRequests.splice(i, 1);
                }
            }
    }
    else if (event.keyCode == 40) {
        if (document.getElementById('arrowsbox down').classList.contains("arrowsbox-active")) {
            document.getElementById('arrowsbox down').classList.toggle("arrowsbox-active");
        }
        keyArray[keyEnum.DOWN_Key] = false;
        downPressed = false;
        if(downRequests.length != 0)
        {
            for(var i=0; i<downRequests.length; i++)
            {
                downRequests[i].abort();
                clearInterval(downRequests[i]);
            }
        }
        downRequests = [];
        for (var i = 0 ; i < timeouts.length ; i++) {
            clearTimeout(timeouts[i]);
        }
        timeouts = [];
        $.ajax({
            url: 'send_command/',
            data: {
                'command': 'get_data'
            },
            dataType: 'json',
            success: function(data){
                speed = data.speed;
                if(speed != 0)
                {
                    function goUp(){
                        upRequests.push($.ajax({
                            url: 'send_command/',
                            data: {'command': 'up'},
                            dataType: 'json',
                            success: function(data){
                                if(data.speed == 0)
                                {
                                    if(upRequests.length != 0)
                                    {
                                        for(var i=0; i<upRequests.length; i++)
                                        {
                                            upRequests[i].abort();
                                            clearInterval(upRequests[i])
                                        }
                                    }
                                    upRequests = [];
                                }
                                else {
                                    timeouts.push(setTimeout(goUp, 250));
                                }
                            },
                            error: function(xhr, status, error){
                              timeouts.push(setTimeout(goUp, 250));
                            },
                            complete: function (data){
                            }
                            }))
                        }
                    goUp();
                }
            }});

    }
    else if (event.keyCode == 38) {
        if (document.getElementById('arrowsbox up').classList.contains("arrowsbox-active")) {
            document.getElementById('arrowsbox up').classList.toggle("arrowsbox-active");
        }
        keyArray[keyEnum.UP_Key] = false;
        upPressed = false;
        if(downRequests.length != 0)
        {
            for(var i=0; i<downRequests.length; i++)
            {
                downRequests[i].abort();
                clearInterval(downRequests[i]);
            }
        }
        downRequests = [];
        for (var i = 0 ; i < timeouts.length ; i++) {
            clearTimeout(timeouts[i]);
        }
        timeouts = [];
        $.ajax({
            url: 'send_command/',
            data: {
                'command': 'get_data'
            },
            dataType: 'json',
            success: function(data){
                speed = data.speed;
                if(speed != 0)
                {
                    function goDown(){
                        downRequests.push($.ajax({
                            url: 'send_command/',
                            data: {'command': 'down'},
                            dataType: 'json',
                            success: function(data){
                                if(data.speed == 0)
                                {
                                    if(downRequests.length != 0)
                                    {
                                        for(var i=0; i<downRequests.length; i++)
                                        {
                                            downRequests[i].abort();
                                            clearInterval(downRequests[i])
                                        }
                                    }
                                    downRequests = [];
                                }
                                else {
                                    timeouts.push(setTimeout(goDown, 250));
                                }
                            },
                            error: function(xhr, status, error){
                              timeouts.push(setTimeout(goDown, 250));
                            },
                            complete: function (data){
                            }
                            }))
                        }
                    goDown();
                }
            }});

    }

};
window.onbeforeunload = function (event) {
    if(rightRequests.length != 0 )
            {
                for(var i = 0; i < rightRequests.length; i++)
                {
                    rightRequests[i].abort();
                    clearInterval(rightRequests[i]);
                    rightRequests.splice(i, 1);
                }
            }
    if(leftRequests.length != 0 )
            {
                for(var i = 0; i < leftRequests.length; i++)
                {
                    leftRequests[i].abort();
                    clearInterval(leftRequests[i]);
                    leftRequests.splice(i, 1);
                }
            }
    if(rightRequest !== 0)
    {
        rightRequest.abort();
        rightRequest = 0;
    }
    if(leftRequest !== 0)
    {
        leftRequest.abort();
        leftRequest = 0;
    }
    //OR use BELOW line to wait 10 secs before first call
    $.ajax({
                url: 'send_command/',
                data: {
                    'command': 'deactivate'
                },
                dataType: 'json'
            });
};