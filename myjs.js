<script type="text/javascript">
var pid = '';
var cards = '';
var events = '';
var positions = '';

$(document).ready(function() {

	var socket = io.connect('http://127.0.0.1:5000');
	socket.emit('join');

	<!--socket.on('connect', function() {-->
		<!--socket.send('User has connected!');-->
	<!--});-->

	socket.on('message', function(msg) {
		$("#messages").append(msg+'<br>');
	});

	socket.on('set_player', function(msg) {
		pid = msg;
        $('#pid').append('pid='+pid);
	});

	socket.on('GameUpdate', function(json_string) {
		console.log('GameUpdate');
		data = JSON.parse(json_string)

		$('#game').append('<pre>'+JSON.stringify(data, null, 2)+'</pre>')
		$('#game').append('############################################')

		$('#game_info').empty()
		$('#game_info').append('data["won"]='+data["won"].toString()+'<br>')
		$('#game_info').append('data["round_queue"]='+data["round_queue"].toString()+'<br>')
		$('#game_info').append('data["player_stage"]='+data["player_stage"].toString()+'<br>')
		$('#game_info').append('data["round"]='+data["round"].toString()+'<br>')

        my_data = data["players"][pid]
		$('#my_cards').empty();
		$('#my_cards').append(my_data.cards.toString())
		$('#my_stat').empty();
		$('#my_stat').append(JSON.stringify(data["players"][pid], null, 2));

		$('#opponents').empty();
		for (i = 0; i < Object.keys(data["players"]).length; i++) {
		    p = Object.keys(data["players"])[i]
		    if (p != pid) {
                $('#opponents').append(p+'<br>');
                $('#opponents').append('<td>'+JSON.stringify(data["players"][p], null, 2)+'</td>');
		    }
        }

        new_history = data["history"]
		for (l of new_history) {
            $("#messages").append(JSON.stringify(l));
        }

        if (data["won"] != false) {
		    alert(data["won"].toString()+' WON !')
		}
	});

	socket.on('cards', function(data) {
	    console.log('cards');
	    card_from_json = JSON.parse(data)
	    cards = card_from_json
	    console.log(cards)
	    <!--$('#opponents_panel').append('<pre>'+JSON.stringify(data, null, 2)+'</pre>');-->
	});

	socket.on('events', function(data) {
		console.log('events');
		events_from_json = JSON.parse(data)
	    events = events_from_json
	    console.log(events)
	});

	socket.on('positions', function(data) {
		console.log('positions');
		positions_from_json = JSON.parse(data)
	    positions = positions_from_json
	    console.log(positions)
	});

	socket.on('sys_message', function(data) {
		messages_from_json = JSON.parse(data)
	    messages = messages_from_json

	    console.log(messages)
	    <!--for each messages append to #messages-->
	});

	$('#sendbutton').on('click', function() {
		socket.send(pid+': '+$('#myMessage').val());
		$('#myMessage').val('');
	});

	$('#play_card').on('click', function() {
	    a = 'play'
	    c = $('#card').val();
	    t = $('#target').val();
		socket.emit('move', pid, a, c, t);
		$('#card').val('');
		$('#target').val('');
	});

	$('#end_play').on('click', function() {
	    a = 'end_play'
		socket.emit('move', pid, a);
	});

	$('#throw_card').on('click', function() {
	    a = 'throw'
	    c = $('#card').val();
		socket.emit('move', pid, a, c);
		$('#card').val('');
	});

	$('#end_throw').on('click', function() {
	    a = 'end_throw'
		socket.emit('move', pid, a);
	});

	$('#reset').on('click', function() {
		socket.emit('reset');
		setTimeout(function(){
            location.reload(true);
        }, 1500);

	});

	window.onbeforeunload = function(event) {
		/*
	    <!--event.returnValue = "abc";-->
        <!--stay on page still emit-->

        <!--refresh won't trigger-->
		*/
        socket.emit('quit', pid)

    };

});


</script>
