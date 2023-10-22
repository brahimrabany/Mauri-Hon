var text_box =  '<div class="media my-4  justify-content-start align-items-start">' +
        '<div style="position: absolute; top: 0; left:3px; font-weight: bolder" class="title">{sender}</div>' +
        '{message}' +
        '</div>';


function scrolltoend() {
    $('#board').stop().animate({
        scrollTop: $('#board')[0].scrollHeight
    }, 800);
}

function send(sender, receiver, message) {
    $.post('/api/messages/', '{"sender": "'+ sender +'", "receiver": "'+ receiver +'","message": "'+ message +'" }', function (data) {
        console.log(data);
        var box = text_box.replace('{sender}');
        box = box.replace('{message}', message);
        $('#board').append(box);
        scrolltoend();apn
    })
}

function receive() {
    $.get('/api/messages/'+ sender_id + '/' + receiver_id, function (data) {
        console.log(data);
        if (data.length !== 0)
        { for(var i=0;i<data.length;i++) {
                console.log(data[i]);
                var box = text_box.replace('{sender}');
                box = box.replace('{message}', data[i].message);
                box = box.replace('right', 'left blue lighten-5');
                $('#board').append(box);
                scrolltoend();
            }
        }
    })
}
