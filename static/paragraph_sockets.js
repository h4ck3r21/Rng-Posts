$(function(){
    var socket = io.connect('/', {transports: ['websocket']});
    let userID = $( '#userid').html()
    socket.on('paragraph', function(paragraph){
            console.log('is ' + paragraph.id + '==' + userID)
            if (paragraph.id == userID) {
                console.log('updating paragraph')
                $( '#paragraph' ).html(paragraph.para)
                $('#para-correct').html(paragraph.cor)
                $( '#errors').html(paragraph.errors)
            }
        })
    socket.on('error', function(id){
            if (id == userID) {
                $('body').addClass('error');
            }
    })

    socket.on('fix', function(userid){
        if (userid == userID) {
            $('body').removeClass('error');
        }
    });

    socket.on('info', function(info){
        if (info.id == userID) {
            $('#name').html(info.name)
            $('#score').html(info.score)
        }
    })
});