from flask import Flask
from flask_socketio import SocketIO, send, join_room

import SEOwar

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecret'
socketio = SocketIO(app)

socketio.connectionCount = 0
players = []
player_game = {}
# TODO game_rooms [{'game':game, 'players':[pids], 'rid':0}, 'status':'started or waiting']
lobby = []  # list of players

# TODO lobby: show and join button
# TODO create_room: emit looby update, move player, add game_rooms


@socketio.on('connect')
def handleConnection():
    socketio.connectionCount += 1  # TODO might not be necessary
    # TODO generate pid then add to players[] and lobby[]
    # TODO emit lobby update
    print('Main.py ', 'connectionCount = ', socketio.connectionCount)
    if socketio.connectionCount > 4:  # TODO should be removed
        return
    players.append('p'+str(socketio.connectionCount))
    print('connect: '+str(players))

    @socketio.on('join')
    def handleJoin():
        # create room only for the player
        # TODO move to handleConnection()
        room = 'room'+str(socketio.connectionCount)
        join_room(room)

        pid = 'p'+str(socketio.connectionCount)
        socketio.emit('set_player', pid, room=room)

        # TODO only when join a game room
        send(pid+' entered the room ', broadcast=True)

        if socketio.connectionCount == 4:

            # create Game for pids in players[]
            # TODO create game with pids in the game room
            game = SEOwar.Game(players)

            cards = game.make_cards()
            events = game.make_events()
            positions = game.make_positions()

            socketio.emit('cards', cards)
            socketio.emit('events', events)
            socketio.emit('positions', positions)

            for p in players:
                player_game[p] = game

            game_json = game.make_json()
            socketio.emit('GameUpdate', game_json)  # only after 'join', which is the 'real' connection

    @socketio.on('quit')
    def handleDisconnection(pid):
        # socketio.connectionCount -= 1  # TODO might not be necessary
        # TODO remove from player[] and (lobby[] or game_room[])
        print(pid+' disconnects')

    @socketio.on('move')
    def handleMove(pid, action, card='', target=''):  # TODO using''
        print('Main.py handleMove() ', pid, action, card, target)

        game = player_game[pid]
        game_json = game.handle_move((pid, action, card, target))

        socketio.emit('GameUpdate', game_json)

    @socketio.on('reset')
    def handleReset():
        print('reset server')
        global players
        global player_game

        socketio.connectionCount = 0
        players = []
        player_game = {}

    test_func()


def test_func():
    print('test_func')


@socketio.on('message')
def handleMessage(msg):
    # print('Message: ' + msg)
    send(msg, broadcast=True)

if __name__ == '__main__':
    socketio.run(app)
