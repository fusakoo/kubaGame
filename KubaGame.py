import copy     # Import to mainly use the deepcopy function

class KubaGame:
    '''
    KubaGame represents the board game called Kuba which the goal is to capture
    7 neutral red marbles or by pushing off all of the opponent's marbles. A player
    who has no legal moves available has lost the game. Note that any player can
    start the game. 
    
    Requires KubaBoard and KubaPlayer class to initialize the class instance
    (KubaBoard is used for board creation, KubaPlayer is used for players).
    Several getter/setter methods are implemented to check & change the private 
    data member(s) of the class instance. 

    '''

    def __init__(self, player1, player2):
        '''
        Initializes the KubaGame class instance by taking 2 tuples parameters (containing 
        player name and color of marble). Sets the two players in game (via KubaPlayer)
        and also creates a board by calling KubaBoard class (store the current state
        of board as the prev board state for future reference). 
        
        Also initializes the game with blank turn (anyone can start), player's
        red marble count as 0, and winner as None.
        '''
        self._player1 = KubaPlayer(player1)
        self._player2 = KubaPlayer(player2)
        self._board = KubaBoard()
        self._odd_turn_board = copy.deepcopy(self.get_board().get_board_state())  # Local copy of the board used for ko rule check
        self._even_turn_board = copy.deepcopy(self.get_board().get_board_state()) # Local copy of the board used for ko rule check
        self._game_turn_counter = 0     # Tracks what turn it is; used for board state updating purpo
        self._current_turn = None       # Stores the player class intance for the current turn
        self._player1_count = 0         # Counts the number of 'R' marbles captured by player 1
        self._player2_count = 0         # Counts the number of 'R' marbles captured by player 2
        self._winner = None             # Will store the winner's player name once game is over

    def get_player1(self):
        '''Returns the 1st player in game'''
        return self._player1

    def get_player2(self):
        '''Returns the 2nd player in game'''
        return self._player2

    def identify_player(self, player_name):
        '''Returns the player's class instance from the given name'''
        if self.get_player1().get_player_name() == player_name:
            return self.get_player1()
        elif self.get_player2().get_player_name() == player_name:
            return self.get_player2()

    def get_player1_count(self):
        '''Returns the count of red marbles captured by player1'''
        return self._player1_count

    def get_player2_count(self):
        '''Returns the count of red marbles captured by player2'''
        return self._player2_count

    def get_board(self):
        '''Returns the board (KubaBoard) class instance'''
        return self._board     

    def get_odd_board(self):
        '''Returns the previous state of board on previous odd turns (1,3,5,etc.)'''
        return self._odd_turn_board

    def get_even_board(self):
        '''Returns the previous state of board on previous even turns (0,2,4,etc.)'''
        return self._even_turn_board        

    def print_board(self,board):
        '''FOR DEBUG ONLY. Prints out the board to the console'''
        for key in board:
            print(board[key])

    def get_game_counter(self):
        '''Returns the counter keeping track of turn # in game'''
        return self._game_turn_counter

    def inc_game_counter(self):
        '''Increments the turn # of game by 1'''
        self._game_turn_counter += 1

    def set_prev_board(self, counter):
        '''
        Takes the current turn # in game and stores as the "previous" odd/even board state 
        to be referenced later in the game.
        '''
        if counter % 2 == 0:
            self._even_turn_board = self.get_board().get_board_state().copy()
        elif counter % 2 == 1:
            self._odd_turn_board = self.get_board().get_board_state().copy()

    def get_current_turn(self):
        '''Returns the current turn's player. Return None if no-one has made move'''
        return self._current_turn

    def set_current_turn(self, player):
        '''
        Takes the player class instance as input and opposite player as the 
        next player (whoever that will be in current_turn next).
        '''
        if self.get_player1() == player:
            self._current_turn = self.get_player2()
        else:
            self._current_turn = self.get_player1()

    def get_winner(self):
        '''Returns the name of the winning player'''
        # Returns the name of the winning player
        # If no player has won, return None
        if self._winner != None:
            return self._winner.get_player_name()
        return None

    def set_winner(self, player):
        '''Takes the player class instance and set as the winner'''
        self._winner = player

    def get_captured(self, player_name):
        '''Returns the number of red marbles captured by the player'''
        if self.get_player1().get_player_name() == player_name:
            return self._player1_count
        # not using else as there is a risk player may typo the player_name
        elif self.get_player2().get_player_name() == player_name:
            return self._player2_count

    def add_captured(self, player):
        '''
        Takes the player class instance and compare to the players.
        Once matched, increment the player's number of red marbles captured.
        '''
        if self.get_player1() == player:
            self._player1_count += 1
        else:
            self._player2_count += 1

    def make_move(self, player_name, coordinates, direction):
        ''' 
        Takes the player name, coordinates (tuple), and direction (one of [L,R,F,B])
        as parameters and first validate if the move is valid. If the move is valid,
        update the board accordingly, update the player for next turn, and return True.
        If invalid (after checking through different invalid scenarios), return False
        and do NOT update the player for next turn (the same player may make the move again).
        '''
        # Check 1) Check whether the player name is actual player in game
        if self.identify_player(player_name):
            # Set the player for future reference
            player = self.identify_player(player_name)
            # Check 2) Check whether the game has been won or not 
            if self.get_winner() == None:
                # Check 3) Just in case, check whether the direction is correctly inputted
                if direction in ['L','R','F','B']:
                    # Check 4) Check if it's the player's turn
                    if self.get_current_turn() == player or self.get_current_turn() == None:
                        # Check 5) Check whether the coordinates provided is valid 
                        if self.get_marble(coordinates) != 'X':
                            # Check 6) Check if the marble belongs to the player
                            if self.get_marble(coordinates):                            
                                # Check 7) Check whether the marble at the coordinate is equal to the player's color
                                if self.get_marble(coordinates) == player.get_player_color():                                
                                    # Check 8) Check if the move can be made (marble has a empty space next to it)
                                    north = self.get_marble((coordinates[0]-1,coordinates[1]))
                                    south = self.get_marble((coordinates[0]+1,coordinates[1]))
                                    east = self.get_marble((coordinates[0],coordinates[1]+1))
                                    west = self.get_marble((coordinates[0],coordinates[1]-1))
                                    # Check the directions and apply the moves accordingly 
                                    # IF there's empty space from the direction player push the marble from
                                    if direction == 'L':
                                        if east == 'X':
                                            # Move is safe to do. Perform.
                                            current_board = copy.deepcopy(self.get_board().get_board_state())
                                            current_board_row = current_board.get(coordinates[0]+1)                                  
                                            # Step 1) If the left of coordinate is already empty, update accordingly
                                            if west == 'X':
                                                # Pop the marble to the east and insert 'X' at coordinate position
                                                current_board_row.pop(coordinates[1]-1)
                                                current_board_row.insert(coordinates[1], 'X')
                                                # Update the board with the new board
                                                counter =  self.get_game_counter()
                                                return self.validate_board(counter, player, current_board)                                               
                                            # Step 2) Else, check how many values to the left of the coordinate are occupied by non-X
                                            else:
                                                empty_pos = None
                                                # For loop to find the 1st occurrent of 'X' to the left of non-'X' values
                                                for i in range(coordinates[1],-1,-1):
                                                    if current_board_row[i] == 'X':
                                                        empty_pos = i
                                                        break
                                                    # If it doesn't reach this point, all values are occupied to the left.
                                                    # We'd need to pop the index 0 value and insert 'X' at coordinate position
                                                # Step 3a) Pop the value at the empty_pos and insert 'X' at coordinate position
                                                if empty_pos:
                                                    current_board_row.pop(empty_pos)
                                                    current_board_row.insert(coordinates[1], 'X')                                        
                                                    # Update the board with the new board
                                                    counter = self.get_game_counter()
                                                    return self.validate_board(counter, player, current_board)                                       
                                                # Step 3b) If all values are occupied to the left, pop left-most value and insert 'X' at coordinate position
                                                else:
                                                    popped_marble = current_board_row.pop(0)
                                                    current_board_row.insert(coordinates[1], 'X')
                                                    # If it's 'R', add to player count
                                                    if popped_marble == 'R':
                                                        self.add_captured(player)
                                                    # If it's 'W' your own marble, return False (invalid)
                                                    elif popped_marble == player.get_player_color():
                                                        return False
                                                    # If it's the opponent's marble, ignore (get_marble_count() will track the number on the board)

                                                    # Update the board with the new board
                                                    counter =  self.get_game_counter()
                                                    return self.validate_board(counter, player, current_board)                                            
                                        # There's something blocking the move. Return False.
                                        return False
                                    elif direction == 'R':
                                        if west == 'X':
                                            # Move is safe to do. Perform.
                                            current_board = copy.deepcopy(self.get_board().get_board_state())
                                            current_board_row = current_board.get(coordinates[0]+1)                                   
                                            # Step 1) If the right of coordinate is already empty, update accordingly
                                            if east == 'X':
                                                # Pop the marble to the east and insert 'X' at coordinate position
                                                current_board_row.pop(coordinates[1]+1)
                                                current_board_row.insert(coordinates[1], 'X')
                                                # Update the board with the new board
                                                counter = self.get_game_counter()
                                                return self.validate_board(counter, player, current_board)                                             
                                            # Step 2) Else, check how many values to the right of the coordinate are occupied by non-X
                                            else:
                                                empty_pos = None
                                                # For loop to find the 1st occurrent of 'X' to the left of non-'X' values
                                                for i in range(coordinates[1],len(current_board)):
                                                    if current_board_row[i] == 'X':
                                                        empty_pos = i
                                                        break
                                                    # If it doesn't reach this point, all values are occupied to the left.
                                                    # We'd need to pop the index 0 value and insert 'X' at coordinate position
                                                # Step 3a) Pop the value at the empty_pos and insert 'X' at coordinate position
                                                if empty_pos:
                                                    current_board_row.pop(empty_pos)
                                                    current_board_row.insert(coordinates[1], 'X') 
                                                    # Update the board with the new board
                                                    counter = self.get_game_counter()
                                                    return self.validate_board(counter, player, current_board)                                          
                                                # Step 3b) If all values are occupied to the right, pop left-most value and insert 'X' at coordinate position
                                                else:
                                                    popped_marble = current_board_row.pop(6)
                                                    current_board_row.insert(coordinates[1], 'X')
                                                    # If it's 'R', add to player count
                                                    if popped_marble == 'R':
                                                        self.add_captured(player)
                                                    # If it's 'W' your own marble, return False (invalid)
                                                    elif popped_marble == player.get_player_color():
                                                        return False
                                                    # If it's the opponent's marble, ignore (get_marble_count() will track the number on the board)

                                                    # Update the board with the new board
                                                    counter = self.get_game_counter()
                                                    return self.validate_board(counter, player, current_board)
                                        # There's something blocking the move. Return False.
                                        return False                            
                                    elif direction == 'F':
                                        if south == 'X':
                                            # Move is safe to do. Perform.
                                            current_board = copy.deepcopy(self.get_board().get_board_state())
                                            current_board_column = list()           # This will be the values for the specific column from top to bottom
                                            # Get all the values in the coordinate's column
                                            for value in current_board.values():
                                                current_board_column.append(value[coordinates[1]])

                                            # Step 1) If the top of coordinate is already empty, update accordingly
                                            if north == 'X':
                                                # Pop the marble to the north and insert 'X' at coordinate position
                                                current_board_column.pop(coordinates[0]-1)
                                                current_board_column.insert(coordinates[0], 'X')
                                                # Update the current_board with the updates column values
                                                update_counter = 0
                                                for value in current_board.values():
                                                    value[coordinates[1]] = current_board_column[update_counter]
                                                    update_counter += 1      

                                                # Update the board with the new board
                                                counter = self.get_game_counter()
                                                return self.validate_board(counter, player, current_board)                                                  
                                            # Step 2) Else, check how many values to the left of the coordinate are occupied by non-X
                                            else:
                                                empty_pos = None
                                                # For loop to find the 1st occurrent of 'X' to the left of non-'X' values
                                                for i in range(coordinates[0],-1,-1):
                                                    if current_board_column[i] == 'X':
                                                        empty_pos = i
                                                        break
                                                    # If it doesn't reach this point, all values are occupied to the left.
                                                    # We'd need to pop the index 0 value and insert 'X' at coordinate position
                                                # Step 3a) Pop the value at the empty_pos and insert 'X' at coordinate position
                                                if empty_pos:
                                                    current_board_column.pop(empty_pos)
                                                    current_board_column.insert(coordinates[0], 'X')
                                                    # Update the current_board with the updates column values
                                                    update_counter = 0
                                                    for value in current_board.values():
                                                        value[coordinates[1]] = current_board_column[update_counter]
                                                        update_counter += 1      
                                                    # Update the board with the new board
                                                    counter = self.get_game_counter()
                                                    return self.validate_board(counter, player, current_board)                                 
                                                # Step 3b) If all values are occupied above, pop bottom value and insert 'X' at coordinate position
                                                else:
                                                    popped_marble = current_board_column.pop(0)
                                                    current_board_column.insert(coordinates[0], 'X')
                                                    # Update the current_board with the updates column values
                                                    update_counter = 0
                                                    for value in current_board.values():
                                                        value[coordinates[1]] = current_board_column[update_counter]
                                                        update_counter += 1  
                                                    # If it's 'R', add to player count
                                                    if popped_marble == 'R':
                                                        self.add_captured(player)
                                                    # If it's 'W' your own marble, return False (invalid)
                                                    elif popped_marble == player.get_player_color():
                                                        return False
                                                    # If it's the opponent's marble, ignore (get_marble_count() will track the number on the board)

                                                    # Update the board with the new board
                                                    counter =  self.get_game_counter()
                                                    return self.validate_board(counter, player, current_board)
                                        # There's something blocking the move. Return False.
                                        return False
                                    elif direction == 'B':
                                        if north == 'X':
                                            # Move is safe to do. Perform.
                                            current_board = copy.deepcopy(self.get_board().get_board_state())
                                            current_board_column = list()           # This will be the values for the specific column from top to bottom
                                            # Get all the values in the coordinate's column
                                            for value in current_board.values():
                                                current_board_column.append(value[coordinates[1]])

                                            # Step 1) If the bottom of coordinate is already empty, update accordingly
                                            if south == 'X':
                                                # Pop the marble to the north and insert 'X' at coordinate position
                                                current_board_column.pop(coordinates[0]+1)
                                                current_board_column.insert(coordinates[0], 'X')
                                                # Update the current_board with the updates column values
                                                update_counter = 0
                                                for value in current_board.values():
                                                    value[coordinates[1]] = current_board_column[update_counter]
                                                    update_counter += 1      

                                                # Update the board with the new board
                                                counter = self.get_game_counter()
                                                return self.validate_board(counter, player, current_board)                                                   
                                            # Step 2) Else, check how many values to the left of the coordinate are occupied by non-X
                                            else:
                                                empty_pos = None
                                                # For loop to find the 1st occurrent of 'X' to the left of non-'X' values
                                                for i in range(coordinates[0],len(current_board)):
                                                    if current_board_column[i] == 'X':
                                                        empty_pos = i
                                                        break    
                                                    # If it doesn't reach this point, all values are occupied to the left.
                                                    # We'd need to pop the index 0 value and insert 'X' at coordinate position
                                                # Step 3a) Pop the value at the empty_pos and insert 'X' at coordinate position
                                                if empty_pos:
                                                    current_board_column.pop(empty_pos)
                                                    current_board_column.insert(coordinates[0], 'X')
                                                    # Update the current_board with the updates column values
                                                    update_counter = 0
                                                    for value in current_board.values():
                                                        value[coordinates[1]] = current_board_column[update_counter]
                                                        update_counter += 1      
                                                    # Update the board with the new board
                                                    counter = self.get_game_counter()
                                                    return self.validate_board(counter, player, current_board)
                                                # Step 3b) If all values are occupied above, pop bottom value and insert 'X' at coordinate position
                                                else:
                                                    popped_marble = current_board_column.pop(6)
                                                    current_board_column.insert(coordinates[0], 'X')
                                                    # Update the current_board with the updates column values
                                                    update_counter = 0
                                                    for value in current_board.values():
                                                        value[coordinates[1]] = current_board_column[update_counter]
                                                        update_counter += 1  
                                                    # If it's 'R', add to player count
                                                    if popped_marble == 'R':
                                                        self.add_captured(player)
                                                    # If it's 'W' your own marble, return False (invalid)
                                                    elif popped_marble == player.get_player_color():
                                                        return False
                                                    # If it's the opponent's marble, ignore (get_marble_count() will track the number on the board)

                                                    # Update the board with the new board
                                                    counter =  self.get_game_counter()
                                                    return self.validate_board(counter, player, current_board)
                                        # There's something blocking the move. Return False.
                                        return False
                                    # We shouldn't end up here since we've already checked the direction, but keeping return False just in case
                                    return False
                                return False
                            return False
                        return False
                    return False
                return False
            return False
        return False

    def validate_board(self, counter, player, current_board):
        '''
        Takes the game turn # count, player, and current board state and validate 
        whether the user's move. Pass the parameters to check_ko_rule and update board state accordingly.
        '''
        # If it is different, update the current board state officially and 
        # set the previous board as the current board for future reference
        if counter == 0:
            self.get_board().set_board_state(current_board)
            self.set_prev_board(counter)
            self.inc_game_counter()
            self.set_current_turn(player)
            self.check_game_state()
            return True
        elif counter % 2 == 0: 
            # Get the previous board state (from 2 turns ago)
            old_board = copy.deepcopy(self.get_even_board())  
            # Check if the ko rule applies (move reverts the previous move or not)
            return self.check_ko_rule(counter, player, current_board, old_board)
        elif counter % 2 == 1:
            # Get the previous board state (from 2 turns ago)
            old_board = copy.deepcopy(self.get_odd_board())
            # Check if the ko rule applies (move reverts the previous move or not)
            return self.check_ko_rule(counter, player, current_board, old_board)

    def check_ko_rule(self, counter, player, current_board, old_board):
        '''
        Compares current board vs board state from 2 turns ago to see if the move done 
        by player reverts to the old state or not (we should not go back-and-fourth 
        through same moves). Return True/False depending on result and update board accordingly.
        '''
        # Check if the ko rule applies (move reverts the previous move or not)
        if old_board != current_board:
            self.get_board().set_board_state(current_board)
            self.set_prev_board(counter)
            self.inc_game_counter()
            self.set_current_turn(player)
            self.check_game_state()
            return True
        # If it is the same, then that's not a valid move (by ko rule)
        return False

    def check_game_state(self):
        ''' 
        During make_move method, checks to see who is currently winning the game.
        If the red marble count for one of the player is 7, update the winner.
        Else if one of the player runs out of their marble, update the winner.
        '''
        # Win scenario 1) if one of the players captured 7 red marbles, declare winner
        if self.get_player1_count() >= 7:
            self.set_winner(self.get_player1())     
        elif self.get_player2_count() >= 7:
            self.set_winner(self.get_player2())   

        # Win scenario 2) if one of the player runs out of their corresponding marble color, declare winner
        marble_count = self.get_marble_count()
        player1_color = self.get_player1().get_player_color()

        if marble_count[0] == 0:
            # Whichever player that controls 'B' wins
            if player1_color == 'W':
                self.set_winner(self.get_player2())
            else:
                self.set_winner(self.get_player1())
        elif marble_count[1] == 0:
            # Whichever player that controls 'W' wins
            if player1_color == 'B':
                self.set_winner(self.get_player2())
            else:
                self.set_winner(self.get_player1())
        # If none of the above scenarios are applicable, continue on the game

    def get_marble(self, coordinates):
        '''
        Takes the coordinates (tuple) of a cell and returns the marble (marble's color)
        that's at the specified coordinate.
        '''
        # Check if row coordinate is in range(0,7)
        if coordinates[0] in range(0,7):
            if coordinates[1] in range(0,7):
                return self.get_board().get_board_state().get(coordinates[0]+1)[coordinates[1]]
            # If the row coordinate is in the range (0,7) BUT the col coordinate is either -1 or 7
            # Check if it's the top side or bottom side of the board (such as (0,-1), (6,7))
            elif coordinates[1] == -1 or coordinates[1] == 7:
                return 'X'
            return False
        # If not, check to see if it's row coordinate is side of the board (used to check if move is valid)
        elif coordinates[0] == -1 or coordinates[0] == 7:
            # Check if col coordinate with x-coordinate hits the four corners of board (-1,-1), (-1,7), (7,-1) (7,7)
            if coordinates[1] == -1 or coordinates[1] == 7:
                return 'X'
            # Otherwise, check if it's the left side or right side of the board (such as (-1,0), (7,2), etc.)
            elif coordinates[1] in range(0,7):
                return 'X'
            # If not, return False
            return False
        return False

    def get_marble_count(self):
        '''
        Returns the number of White marbles, Black marbles, and Red marbles
        as tuple in the order (W,B,R).
        '''
        w_count = 0
        b_count = 0
        r_count = 0
        # count each color from the board and add it to the list index
        current_row = 1
        while current_row < 8:
            # fetch the marble color from current state of board and tally up
            for marble in self.get_board().get_board_state().get(current_row):
                if marble == 'W':
                    w_count += 1
                elif marble == 'B':
                    b_count += 1
                elif marble == 'R': 
                    r_count += 1
            current_row += 1
    
        marble_count = (w_count,b_count,r_count)
        return marble_count

class KubaBoard:
    ''' 
    KubaBoard represents the board that is used by the KubaGame class (used when the
    corresponding class is initialized). Stores the current state of the board (marble
    colors) as well as getter/setter method to check and update the color of marble 
    from the user provided coordinate.
    '''

    def __init__(self):
        '''
        Initializes a KubaBoard class instance without any input parameter by following
        the Kuba board game initial setup as reference. This will be called by KubaGame
        class when the corresponding class is initialized.
        '''
        # Board set according to official rules. Please don't change :/
        self._board = {
            1: ['W', 'W', 'X', 'X', 'X', 'B', 'B'],
            2: ['W', 'W', 'X', 'R', 'X', 'B', 'B'],
            3: ['X', 'X', 'R', 'R', 'R', 'X', 'X'],
            4: ['X', 'R', 'R', 'R', 'R', 'R', 'X'],
            5: ['X', 'X', 'R', 'R', 'R', 'X', 'X'],
            6: ['B', 'B', 'X', 'R', 'X', 'W', 'W'],
            7: ['B', 'B', 'X', 'X', 'X', 'W', 'W']
        }

    def get_board_state(self):
        '''Returns the current state of the board'''
        return self._board

    def set_board_state(self, board_state):
        '''
        Sets the board state to the given board dictionary. Intended to be used when
        the move is invalid (i.e. ko rule applied).
        '''
        self._board = board_state

class KubaPlayer:
    ''' 
    Player represents the player that is specifically playing the Kuba board game.
    Class instance is initialized with player name and marble color of choice (should
    be either B or W).
    '''
    
    def __init__(self, player_data):
        '''
        Initializes a KubaPlayer class instance by taking player_data (tuple with
        player name and marble color) and set it accordingly for the instance.
        '''
        self._name = player_data[0]
        self._color = player_data[1]
    
    def get_player_name(self):
        '''Returns the name of the player'''
        return self._name

    def get_player_color(self):
        '''Returns the marble color corresponding to the player'''
        return self._color

def main():
    '''Runs if the file is run as script. '''
    game = KubaGame(('PlayerA', 'W'), ('PlayerB', 'B'))

    # Test to check whether the turn check works
    # print(game.make_move('PlayerA', (6, 5), 'F'))
    # print(game.get_current_turn().get_player_name())
    # print(game.make_move('PlayerA', (5, 5), 'F'))
    # print(game.get_current_turn().get_player_name())

    # print(game.make_move('PlayerA', (6,5), 'L'))        # False
    # print(game.make_move('PlayerA', (6,6), 'L'))        # True
    # print(game.make_move('PlayerB', (6,0), 'R'))        # True
    # print(game.make_move('PlayerA', (6,5), 'L'))        # True
    # print(game.make_move('PlayerB', (6,1), 'R'))        # True
    # print(game.make_move('PlayerA', (6,5), 'L'))        # ko rule should apply and return false
    # print(game.get_current_turn().get_player_name())    # Should be PlayerA
    # print(game.make_move('PlayerA', (6,4), 'F'))        # True
    # print(game.make_move('PlayerB', (5,0), 'R'))        # True
    # print(game.make_move('PlayerA', (5,4), 'F'))        # True
    # print(game.make_move('PlayerB', (5,1), 'R'))        # True
    # print(game.make_move('PlayerA', (0,0), 'B'))        # True
    # print(game.make_move('PlayerB', (5,2), 'R'))        # B pushes off 1 'W'
    # print(game.get_marble_count())                      # (7,8,13)
    # print(game.make_move('PlayerA', (1,0), 'B'))        # True
    # print(game.make_move('PlayerB', (5,3), 'R'))        # B pushes off 1 'W'
    # print(game.get_marble_count())                      # (6,8,13)
    # print(game.make_move('PlayerA', (3,0), 'R'))        # True
    # print(game.make_move('PlayerB', (5,5), 'B'))        # B pushes off 1 'W'
    # print(game.get_marble_count())                      # (5,8,13)
    # print(game.make_move('PlayerA', (3,1), 'R'))        # W pushes off 1 'R'
    # print(game.get_marble_count())                      # (5,8,12)
    # print(game.make_move('PlayerB', (1,6), 'L'))        # True
    # print(game.make_move('PlayerA', (3,2), 'R'))        # W pushes off 1 'R'
    # print(game.get_marble_count())                      # (5,8,11)
    # print(game.make_move('PlayerB', (1,5), 'L'))        # True
    # print(game.make_move('PlayerA', (3,3), 'R'))        # W pushes off 1 'R'
    # print(game.get_marble_count())                      # (5,8,10)
    # print(game.get_player1_count())                     # Returns 3 (of 7)
    # print(game.make_move('PlayerB', (1,4), 'L'))        # B pushes off 1 'W'
    # print(game.get_marble_count())                      # (4,8,10)
    # print(game.make_move('PlayerA', (3,4), 'R'))        # W pushes off 1 'R'
    # print(game.get_marble_count())                      # (4,8,9)    
    # print(game.get_player1_count())                     # Returns 4 (of 7)
    # print(game.make_move('PlayerB', (1,3), 'L'))        # B pushes off 1 'R'
    # print(game.get_marble_count())                      # (4,8,8)
    # print(game.make_move('PlayerA', (3,5), 'R'))        # W pushes off 1 'R'
    # print(game.get_marble_count())                      # (4,8,7)   
    # print(game.get_player1_count())                     # Returns 5 (of 7)
    # print(game.make_move('PlayerB', (0,6), 'F'))        # True
    # print(game.make_move('PlayerA', (2,0), 'F'))        # True
    # print(game.make_move('PlayerB', (1,6), 'B'))        # True
    # print(game.make_move('PlayerA', (1,0), 'F'))        # W pushes off 1 'R'
    # print(game.get_marble_count())                      # (4,8,6)   
    # print(game.get_player1_count())                     # Returns 6 (of 7)
    # print(game.make_move('PlayerB', (0,5), 'B'))        # True
    # print(game.make_move('PlayerA', (4,6), 'B'))        # True
    # print(game.make_move('PlayerB', (1,5), 'B'))        # True
    # print(game.get_winner())                            # None (no winner yet)
    # print(game.make_move('PlayerA', (5,6), 'B'))        # Win step
    # print(game.get_player1_count())                     # Returns 7 (of 7)
    # print(game.get_winner())                            # PlayerA

    # Empty the board except for one 'B' 
    # game.print_board(game.get_board().get_board_state()) 
    # print(game.get_marble_count())                      # (9,1,16)  
    # print(game.make_move('PlayerA', (1,5), 'R'))        # Win step
    # game.print_board(game.get_board().get_board_state()) 
    # print(game.get_marble_count())                      # (9,0,16)            
    # print(game.get_winner())                            # PlayerA
 
if __name__ == '__main__':
    # Determines whether the main function is called 
    main()
