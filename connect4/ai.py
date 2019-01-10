import random
import board


class AI:
    def __init__(self, acontroller):
        '''
        Initializes ai class
        '''
        self.controller = acontroller
        self.board = board.Board(self.controller)

    def initialize(self):
        '''
        Initializes the ai and creates a new board object to
        experiment on.
        '''

        self.player = self.controller.playon.get_who_is_playing()
        self.cur_player = self.controller.playon.get_who_is_playing()
        self.enemy = self.get_enemy(self.player)

        self.board.initialize_board()
        self.board.add_where_pieces(self.controller.board.get_pieces())

    def switch_players(self):
        '''
        Returns which player is the enemy to the ai.
        '''
        if self.player == 'A':
            self.enemy = self.get_enemy(self.player)
            self.player = 'B'
        else:
            self.enemy = self.get_enemy(self.player)
            self.player = 'A'

    def get_enemy(self, player):
        '''
        Returns the opponent
        '''
        if player == 'A':
            return 'B'
        else:
            return 'A'

    def possible_moves(self):
        '''
        Get all possible moves. Check whether every possible move can
        result in a win.

        Result in a win: return the winning move

        Or else: return possble moves list,
        sorted with the moves which are likely to be optimal at the start,
        (according distance to center, and than to height)
        to optimize alpha-beta pruning in the recursive_eval method

        According to documentation about sorted and lambda
        https://docs.python.org/3/howto/sorting.html#sortinghowto
        https://docs.python.org/3/reference/expressions.html#lambda
        '''

        possible_moves_list = []

        for x in range(self.board.get_width()):
            y = 0
            while y < self.board.get_height() - 1 and self.board.get_pieces(
            )[x][y] != '0':
                y += 1
            if self.board.get_pieces()[x][y] == '0':
                if self.controller.playon.determine_win(
                        self.player, (x, y), False, self.board) == True:
                    return [float('inf'), (x, y)]
                else:
                    possible_moves_list.append((x, y))

        possible_moves_list_sorted = sorted(
            possible_moves_list,
            key=
            lambda move: (abs(((self.board.get_width() // 2) - move[0])), move[1])
        )
        return possible_moves_list_sorted

    def make_decision_random(self):
        '''
        Returns a winning move. If no winning move, return random move.
        '''
        self.initialize()
        possible_moves_list = self.possible_moves()
        if float('inf') in possible_moves_list:
            return possible_moves_list[1]
        else:
            return random.choice(possible_moves_list)

    def make_decision_smart(self, depth):
        '''
        Returns the best move given a player and a board.

        For the 1st 2 moves, the ai will play at the center.

        For the remaining moves, check whether a move can win
        Win: return move
        No win: return list containing all possible moves

        For every move in the list, use the recursive_eval method
        to recursively evaulate the move's score.
        We will then prioritise center by mutiplying the center's piece
        score by 4 during early game,
        and return the best move with the max score.

        As the pieces on the board increase,
        the possiblities will decrease and
        we can gradually increase the search depth
        while maintaining a reasonable computation time
        '''

        self.initialize()

        if self.controller.board.get_num_pieces() < 2:
            if self.board.get_pieces()[3][0] == '0':
                return (self.board.get_width() // 2, 0)
            else:
                return (self.board.get_width() // 2, 1)
        elif 15 < self.controller.board.get_num_pieces() <= 20:
            depth += 2
        elif 20 < self.controller.board.get_num_pieces() <= 25:
            depth += 4
        elif self.controller.board.get_num_pieces() > 25:
            depth += 6

        possible_moves_scores = {}
        possible_moves_list = self.possible_moves()

        if float('inf') in possible_moves_list:
            return possible_moves_list[1]
        else:
            max_score = -float('inf')
            for possible_move in possible_moves_list:
                x, y = possible_move
                self.board.add_piece(x, y, self.player)
                self.switch_players()
                node_score = self.recursive_eval(max_score, float('inf'),
                                                 depth)

                possible_moves_scores[possible_move] = node_score
                max_score = max(max_score, node_score)
                self.switch_players()
                self.board.remove_piece(x, y)

            print("AI's possible moves scores:\n{}\n".format(
                possible_moves_scores))

            if self.controller.board.get_num_pieces() < 10:
                for move in possible_moves_list:
                    if move[0] == self.board.get_width() // 2:
                        possible_moves_scores[move] *= 4

            max_move = [
                move for move, score in possible_moves_scores.items()
                if score == max(possible_moves_scores.values())
            ][0]

            return max_move

    def recursive_eval(self, a, b, depth):
        '''
        Uses minimax algorithm optimized with alpha beta pruning.

        Minimax:

        Uses a tree search algorithm and returns the best possible move,
        presuming both sides will play optimally.


        you       3      (Your score)
                /   \


        opp    3     6   (Opponent: Opponent will play the best move,
                            and return the move which
                            minimizes your score. 3/6 will return 3)
              / \   / \
        you  3   1 6   2 (Final level: return your base score
                            according to the eval score method.
                            As you will play your best move,
                            you will return your best score
                            in the branch. 3/1 will return 3,
                            6/2 will return 6)

        Alpha beta pruning:

        Does not search a branch when the branch results in a worse score
        than the present score.

        Upon evaluating the lower left tree:

        you
                /   \
        opp    3        (Beta is opponent present min score: 3)
              / \   / \
        you  3   1

        As you proceed with the lower right branch:

        you       3
                /   \
        opp    3    10   (Beta is opponent present min score: 3)
              / \   / \
        you  3   1 10  X (Alpha is your present max score: 10)

        As alpha 10 is greater than beta 3: X does not need to be evaluated
        as evaluating X will not change the decision.
        Getting a 10 on the right branch entails that the right branch is
        better than all the moves on the left branch.
        Hence the opponent, which aim to play the best move by minimizing
        you score, will never play the left move.

        Now evaluating the right branch:

        opp
                   /         \
        you       3                  (Alpha is your present maximum: 3)
                /   \       /    \
        opp    3    10               (Alpha is 3 gets recursively passed down)
              / \   / \    /  \   /  \
        you  3   1 10  X  2    1

        Opponent get a score = 2 on the right branch

        opp             3
                   /         \
        you       3            2     (Alpha your present maximum: 3)
                /   \        /    \
        opp    3    10      2      X  (Beta is opponent present min score: 2)
              / \   / \    /  \   /  \ while alpha is 3
        you  3   1 10  X  2    1  X  X

        As alpha 3 is greater than beta 2: Xs does not need to be evaluated
        as evaluating Xs will not change the decision.
        For you, getting a maximum 2 on the right branch entails that the
        right branch is worst than all the moves on the left branch.
        Hence the opponent, which aim to play the best move by minimizing
        you score, will return a move with score 2 or less.
        As your present move with score 3 is better than score 2,
        you will now definitely choose the left move despite any score given
        by the Xs.

        '''
        if depth == 0:
            possibles_move_list = self.possible_moves()
            if float('inf') in possibles_move_list:
                return float('inf')
            else:
                max_score = -float('inf')
                for possible_move in possibles_move_list:
                    x, y = possible_move
                    self.board.add_piece(x, y, self.player)
                    max_score = max(
                        max_score,
                        self.eval_score(self.player,
                                        self.board.get_new_piece()))
                    self.board.remove_piece(x, y)
                    a = max(a, max_score)
                    if b <= a:
                        break
                return max_score

        elif self.player == self.cur_player:
            '''
            Maximizes the score if the player's move
            being looked at is the ai
            '''
            possibles_move_list = self.possible_moves()
            if float('inf') in possibles_move_list:
                return float('inf')
            else:
                max_score = -float('inf')
                for possible_move in possibles_move_list:
                    x, y = possible_move
                    self.board.add_piece(x, y, self.player)
                    self.switch_players()
                    max_score = max(max_score,
                                    self.recursive_eval(a, b, depth - 1))
                    self.switch_players()
                    self.board.remove_piece(x, y)
                    a = max(a, max_score)
                    if a >= b:
                        break
                return max_score
        else:
            '''
            Assumes the opponent will minimize the ai's score
            '''
            possibles_move_list = self.possible_moves()
            if float('inf') in possibles_move_list:
                return -float('inf')
            else:
                min_score = float('inf')
                for possible_move in possibles_move_list:
                    x, y = possible_move
                    self.board.add_piece(x, y, self.player)
                    self.switch_players()
                    min_score = min(min_score,
                                    self.recursive_eval(a, b, depth - 1))
                    self.switch_players()
                    self.board.remove_piece(x, y)
                    b = min(b, min_score)
                    if b <= a:
                        break
                return min_score

    def eval_score(self, aplayer, apiece, prioritise_center=True):
        '''
        Check whether possble move can win in a direction
        using possible_win_in_a_dirct method.
        For player A, arrangement 0,A,0,0 can possible win,
        in the horizontal direction, but not arrangement B,A,0,B.

        Cannot possibly win: delete in list
        Remaining possibles_move_list will contain those moves
        which can possibly win and we will evaluate those moves

        Those directions which can't create a win are discounted.
        Then the remaining directions are evaluated
        using multiplier_in_a_dirctn, with direct connections in a direction
        multiplied by 4. For player A, arrangement A,A will give 4 points,
        while A,A,A will give 16 points.

        Multiplier_in_a_dirctn take into account gaps as well,
        with '0's multiplied by 2.
        For player A, arrangement A,A,B will give 16 points,
        while A,A,0 will give 32 points.

        The method will recurse up to 1 zero in a direction,
        with any connection beyond the zero mulitplying the
        score by 2.
        For player A, arrangement the last A in A,0,A will
        multiply the score by 2.
        Both A,0,A,0 and A,0,A,B will give 8 points,
        as we do not take into account the 2nd zero
        (or anything beyond)

        Then eval_score will sum up the scores in every direction
        to give the total scores. To prioritise center, the total score
        will be multiplied by the the piece's distance to center,
        where a piece closer to the center will get a greater score.

        More examples in testing_ai.py

        uldr, ud, urdl
        lr, piece,  lr
        urdl, ud, uldr

        uldr = connections to the up, left / down, right
        urdl = connections to up, right / down, left
        ud = connections to up / down
        lr = connections to left / right
        '''

        self.dirtn_score = {'uldr': 1, 'urdl': 1, 'lr': 1, 'ud': 1}
        self.connections_dirtn = {'uldr': 0, 'urdl': 0, 'lr': 0, 'ud': 0}
        self.directions_coords = {
            'uldr': ((-1, 1), (1, -1)),
            'urdl': ((1, 1), (-1, -1)),
            'lr': ((-1, 0), (1, 0)),
            'ud': ((0, -1), (0, 1))
        }

        for dirtns in self.directions_coords.copy():
            for a_dirtn in self.directions_coords.copy()[dirtns]:
                self.connections_dirtn[
                    dirtns] += self.possible_win_in_a_dirctn(
                        a_dirtn, self.player, apiece)
            if self.connections_dirtn[dirtns] < 3:
                del self.directions_coords[dirtns]

        for dirtns in self.directions_coords:
            for a_dirtn in self.directions_coords[dirtns]:
                self.dirtn_score[dirtns] *= self.multiplier_in_a_dirctn(
                    a_dirtn, self.player, apiece)

        total_score = sum(self.dirtn_score.values())

        if prioritise_center == True:
            distance_to_center = abs(apiece[0] - self.board.get_width() // 2)
            if distance_to_center == 0:
                center_multiplier = 2.5
            elif distance_to_center == 1:
                center_multiplier = 2
            elif distance_to_center == 2:
                center_multiplier = 1.5
            else:
                center_multiplier = 1

            total_score *= center_multiplier
        return total_score

    def multiplier_in_a_dirctn(self, adirection, aplayer, apiece, zero_num=0):
        '''
        checks for connections in a given direction and only stops if it
        encounters two zeroes or one of the enemies pieces. Returns a score
        which has a multiplier that is halved if a zero has already been
        encountered in that direction.
        '''
        new_piece = (apiece[0] + adirection[0], apiece[1] + adirection[1])
        new_x, new_y = new_piece[0], new_piece[1]

        if new_x >= self.board.get_width() or new_y >= self.board.get_height(
        ) or new_x < 0 or new_y < 0:
            return 1

        elif zero_num == 1:
            if self.board.get_pieces()[new_x][new_y] == self.player:
                return 2 * self.multiplier_in_a_dirctn(adirection, self.player,
                                                       new_piece, 1)
            else:
                return 1
        else:
            if self.board.get_pieces()[new_x][new_y] == '0':
                return 2 * self.multiplier_in_a_dirctn(adirection, self.player,
                                                       new_piece, 1)

            else:
                return 4 * self.multiplier_in_a_dirctn(adirection, self.player,
                                                       new_piece)

    def possible_win_in_a_dirctn(self, adirection, aplayer, apiece):
        '''
        Adds up connections in a direction, and counts empty spaces as a
        connection.
        '''
        new_piece = (apiece[0] + adirection[0], apiece[1] + adirection[1])
        new_x, new_y = new_piece[0], new_piece[1]
        if new_x >= self.board.get_width() or new_y >= self.board.get_height(
        ) or new_x < 0 or new_y < 0:
            return 0
        elif self.board.get_pieces()[new_x][new_y] not in (self.player, '0'):
            return 0
        else:
            return 1 + self.possible_win_in_a_dirctn(adirection, self.player,
                                                     new_piece)
