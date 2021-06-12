$(function(){
    var connected = false;
    var socket = io.connect('/', {transports: ['websocket']});
    let userID = $( '#userID').html()
    var Ids = [userID]
    $( "#message-box" ).keydown(function() {
      setTimeout(() => {
           let user_input = $( 'input.message' ).val()
           console.log('sending keypress')
           socket.emit('keypress', {input: user_input, userID:userID})
      }, 100);
    });

    socket.on('resend_user', function(ID) {
        if (userID == ID) {
            let username = $( '#username').html()
            socket.emit('user_details', {ID:ID, name:username})
        }
    })

    socket.on( 'connect', function() {
      if (connected == false) {
          connected = true
          let username = $( '#username').html()
          let userID = $( '#userID').html()
          socket.emit( 'connecting', {username: username, userID: userID})
          console.log('user connected')
          var form = $( 'form' ).on( 'submit', function( e ) {
              e.preventDefault()
            })
      }
    })

    socket.on('log', function(msg) {
      $( '#log' ).append( '<div>'+ msg + '</div>' )
    })

    socket.on( 'user disconnect', function() {
      console.log('sending user disconnect message')
      Ids = [userID]
      $( "#enemy-paragraphs").empty()
      socket.emit('online', userID)
    });

    socket.on('error', function(id){
        console.log('error')
        if (id == userID) {
            $('#your-para').addClass('error');
        }
    })

    socket.on('fix', function(id){
        console.log('correct keypress')
        if (id == userID) {
            $('#your-para').removeClass('error');
        }
    })

    socket.on('connection', function(enemy_id){
        console.log('enemy connecting')
        console.log('checking if ' + enemy_id.id + 'is equal to ' + userID)
        if (userID == enemy_id.id) {
            var i;
            for (i = 0; i < enemy_id.len; i++) {
              console.log('id being checked:' + enemy_id[i])
              console.log(Ids)
              console.log(!(Ids.includes(enemy_id[i])))
              if (!(Ids.includes(enemy_id[i]))) {
                  Ids.push(enemy_id[i])
                  console.log('added' + enemy_id[i])
                  Ids.push(enemy_id[i])
                  console.log('adding enemy pargraph')
                  $( "#enemy-paragraphs").append('<iframe src="/paragraph/'+
                   enemy_id[i] +
                   '" title="your paragraph" class="enemy-para"></iframe>');
              }
            };
        }
    })

    socket.on('new user', function(id){
        console.log('new user: ' + id)
        console.log('checking if ' + id + 'is not equal to ' + userID)
        console.log(id != userID && !(id in Ids))
        console.log(Ids)
        if (id != userID && !(id in Ids)) {
            Ids.push(id)
            console.log('adding enemy paragraph')
            $( "#enemy-paragraphs").append('<iframe src="/paragraph/'+ id +'" title="your paragraph" class="enemy-para"></iframe>');
        }
    })

    socket.on('start', function(){
        console.log('starting')
        $('#your-para').removeClass('hidden')
        $('#start-button').addClass('hidden')
    })

    socket.on('victory', function(json){
        $('#table').addClass('hidden')
        $('#victory').html(json.name + ' WINS')
        $('#victory').removeClass('hidden')
        setTimeout(() => {
            $('#victory').addClass('hidden')
            location.reload()
        }, 5000)
    })

});
