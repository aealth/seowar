import json

import random
import math
import pprint

import Cards


class Game:
    gameCount = 0
    universities = {'Arts': {'start_p': '10', 'rf': 10, 'cr': 1, 'cs': 2, 'ss': 2},  # TODO position adapt
                    'Music': {'start_p': '16', 'rf': 1, 'cr': 10, 'cs': 10, 'ss': 1},
                    'Science': {'start_p': '14', 'rf': 4, 'cr': 7, 'cs': 7, 'ss': 0},
                    'Building': {'start_p': '12', 'rf': 7, 'cr': 4, 'cs': 4, 'ss': 1}
                    # 'Building': {'start_p': '12', 'rf': 7, 'cr': 4, 'cs': 4, 'ss': 11}  # to test penguin
                    }

    stat_max = {'rf': 50, 'cr': 25, 'cs': 50, 'ss': 10}
    stat_min = {'rf': 1, 'cr': 1, 'cs': 1, 'ss': 0}

    cards = Cards.generate_card_dict('Tactic Card')
    events = Cards.generate_card_dict('Event Card')

    positions = {'1': {'visitors': 1100, 'rf_min_req': 35},
                 '2': {'visitors': 1000, 'rf_min_req': 35},
                 '3': {'visitors': 900, 'rf_min_req': 35},
                 '4': {'visitors': 800, 'rf_min_req': 35},
                 '5': {'visitors': 675, 'rf_min_req': 20},
                 '6': {'visitors': 600, 'rf_min_req': 20},
                 '7': {'visitors': 525, 'rf_min_req': 20},
                 '8': {'visitors': 450, 'rf_min_req': 20},
                 '9': {'visitors': 350, 'rf_min_req': 10},
                 '10': {'visitors': 300, 'rf_min_req': 10},
                 '11': {'visitors': 250, 'rf_min_req': 10},
                 '12': {'visitors': 200, 'rf_min_req': 10},
                 '13': {'visitors': 125, 'rf_min_req': 0},
                 '14': {'visitors': 100, 'rf_min_req': 0},
                 '15': {'visitors': 75, 'rf_min_req': 0},
                 '16': {'visitors': 50, 'rf_min_req': 0}
                 }

    conversion_rate = {x+1: 0.5 + x * 0.05 for x in range(25)}  # eg. {1: 0.5, 2: 0.55}

    def __init__(self, pids):
        print('SEOwar.py', 'creating Game ', pids)

        self.won = False
        self.player_stage = 'play'  # or 'throw'
        self.round = 1

        self.card_stack = []
        self.shuffle_cards()

        self.event_stack = [str(i) for i in range(len(Game.events))]
        random.shuffle(self.event_stack)

        # self.card_stack = []
        # self.card_stack += random.shuffle([str(i) for i in range(len(Game.cards)-len(self.card_stack))])

        self.players = {}

        # just for init universities
        sequence = [k for k in Game.universities.keys()]
        random.shuffle(sequence)

        for pid in pids:
            # print('creating player: pid = '+pid)
            player = dict()

            player['admission'] = 0
            player['university'] = sequence.pop(0)
            player['position'] = Game.universities[player['university']]['start_p']
            player['rf'] = Game.universities[player['university']]['rf']
            player['cr'] = Game.universities[player['university']]['cr']
            player['cs'] = Game.universities[player['university']]['cs']
            player['ss'] = Game.universities[player['university']]['ss']
            player['cards'] = self.draw_card(5)

            self.players[pid] = player

        self.round_queue = self.determine_queue()

        # self.round = 0
        # self.turn = ''

        self.history = []  # [-1]=last_played
        msg = {'type': 'custom', 'msg': 'Game initialized'}
        self.history.append(msg)
        self.current = 0

        Game.gameCount += 1

    def make_json(self):
        game = dict()
        game['players'] = self.players
        game['history'] = self.history[self.current:]
        game['round_queue'] = self.round_queue
        game['won'] = self.won
        game['player_stage'] = self.player_stage
        game['round'] = self.round

        self.current = len(self.history)
        # pp = pprint.PrettyPrinter(indent=4)
        # pp.pprint(game)

        return json.dumps(game)

    def make_cards(self):
        return json.dumps(Game.cards)

    def make_events(self):
        return json.dumps(Game.events)

    def make_positions(self):
        return json.dumps(Game.positions)

    # def add_history(self, pid, action, card, target=None):
    #     self.history.append({'pid': pid,
    #                          'action': action,
    #                          'card': card,
    #                          'target': target
    #                          })

    def handle_move(self, move):
        pid = move[0]
        action = move[1]
        card = move[2]
        target = move[3]

        if action == 'play':
            self.play_card(pid, card, target)
        elif action == 'end_play':
            self.player_draw(pid, 3)
        elif action == 'throw':
            self.player_throw(pid, card)
        elif action == 'end_throw':
            self.end_turn(pid)

        return self.make_json()

    def check_winner(self, pid):
        if self.players[pid]['admission'] >= 50:
            print('won', pid)
            msg = {'type': 'custom', 'msg': pid+' Won!'}
            self.history.append(msg)
            return True
        return False

    def adjust_stats(self, pid, stats):

        for idx, stat in enumerate(['rf', 'cr', 'cs', 'ss']):
            original = self.players[pid][stat]
            change = stats[idx]
            new_stat = original + change

            if new_stat < Game.stat_min[stat]:
                new_stat = Game.stat_min[stat]
            elif new_stat > Game.stat_max[stat]:
                new_stat = Game.stat_max[stat]

            self.players[pid][stat] = new_stat

            if original != self.players[pid][stat]:
                msg = {'type': 'adjust', 'pid': pid, 'stat': stat, 'original': original, 'new': new_stat}
                self.history.append(msg)

        if stats[0] > 0:
            self.adjust_position(pid)

    def adjust_position(self, pid):
        # input: [(player, position, rf)]
        rf = self.players[pid]['rf']  # int
        position = int(self.players[pid]['position'])  # str->int
        original = str(position)
        up_one_position = position - 1  # int

        position_list = [self.players[pid]['position'] for pid in self.players]  # str

        if up_one_position not in position_list and rf >= Game.positions[str(up_one_position)]['rf_min_req']:
            self.players[pid]['position'] = str(up_one_position)
            position = int(self.players[pid]['position'])  # str->int

        lower_rf_list = [(pid, self.players[pid]['position'], self.players[pid]['rf']) for pid in self.players if self.players[pid]['rf'] < rf]

        if len(lower_rf_list) == 0:
            return

        # print('before sort=', lower_rf_list)
        s = sorted(lower_rf_list, key=lambda x: int(x[1]))  # sort by p['position'] in asc
        # print('sorted=', s)
        if int(s[0][1]) < position:
            self.players[s[0][0]]['position'], self.players[pid]['position'] = self.players[pid]['position'], self.players[s[0][0]]['position']  # swap

        if self.players[pid]['position'] != original:
            msg = {'type': 'adjust', 'pid': pid, 'stat': 'position', 'original': original, 'new': self.players[pid]['position']}
            self.history.append(msg)

    def adjust_admission(self, pid, k):
        original = self.players[pid]['admission']
        self.players[pid]['admission'] += k  # TODO changed: += instead of =

        msg = {'type': 'adjust', 'pid': pid, 'stat': 'admission', 'original': original, 'new': self.players[pid]['admission']}
        self.history.append(msg)

        if self.check_winner(pid):
            self.won = pid

    def shuffle_cards(self):
        c = [str(i) for i in range(len(Game.cards))]
        random.shuffle(c)
        self.card_stack = c

    def draw_card(self, n):
        if len(self.card_stack) < n:
            self.shuffle_cards()
        drawn = self.card_stack[:n]
        self.card_stack = self.card_stack[n:]
        return drawn

    def play_card(self, pid, card, target):
        # skip criteria part
        print('SEOwar.py play_card() ', pid, card, target)
        subject = pid

        if target != '':
            # an attack card
            subject = target
            msg = {'type': 'attack', 'pid': pid, 'card': card, 'target': subject}
        else:
            msg = {'type': 'play', 'pid': pid, 'card': card}

        self.history.append(msg)

        the_card = Game.cards[card]
        self.adjust_stats(subject, the_card['stat'])

        self.players[pid]['cards'].remove(card)

    def player_draw(self, pid, n):
        new_cards = self.draw_card(n)
        self.players[pid]['cards'] += new_cards

        self.player_stage = 'throw'

        msg = {'type': 'draw', 'pid': pid, 'card': new_cards}
        self.history.append(msg)

    def player_throw(self, pid, card):
        self.players[pid]['cards'].remove(card)

        msg = {'type': 'throw', 'pid': pid, 'card': card}
        self.history.append(msg)

    def end_turn(self, pid):
        self.draw_events(pid)

        self.round_queue.pop(0)

        self.player_stage = 'play'

        if len(self.round_queue) == 0:
            self.end_round()

    def end_round(self):
        print('SEOwar.py end_round()')
        msg = {'type': 'custom', 'msg': 'End of Round'}
        self.history.append(msg)

        pens = self.get_penguins()
        for pid in self.players:
            if pid not in pens:
                position = self.players[pid]['position']
                v = Game.positions[position]['visitors']
                cr = self.players[pid]['cr']

                k = self.conversion_map(v, cr)
                self.adjust_admission(pid, k)

                self.link_earning(pid)
            else:
                msg = {'type': 'custom', 'msg': pid+' penguined'}
                self.history.append(msg)
                self.players[pid]['ss'] = 0

        self.round_queue = self.determine_queue()
        self.round += 1
        return

    def link_earning(self, pid):
        rf = math.floor(int(self.players[pid]['cs'])/5)

        if rf >= 0:
            msg = {'type': 'custom', 'msg': pid+' link earning: +'+str(rf)+'rf'}
            self.history.append(msg)

        self.adjust_stats(pid, [rf, 0, 0, 0])

    def conversion_map(self, v, cr):
        conversion_rate = Game.conversion_rate[cr]/100
        admission = conversion_rate*v
        return math.ceil(admission)

    def get_penguins(self):
        pid_ss = [(pid, self.players[pid]['ss']) for pid in self.players]
        penguins = [p[0] for p in pid_ss if p[1] >= 10]

        return penguins

    def determine_queue(self):
        pid_rf = [(pid, self.players[pid]['rf']) for pid in self.players]
        sort = sorted(pid_rf, key=lambda x: int(x[1]), reverse=True)

        return [s[0] for s in sort]

    def draw_events(self, pid):
        print('SEOwar.py draw_events()')

        event_no = self.event_stack.pop(0)  # TODO would not reshuffle when run out
        self.adjust_stats(pid, Game.events[event_no]['stat'])

        msg = {'type': 'event', 'pid': pid, 'event': event_no}
        self.history.append(msg)
