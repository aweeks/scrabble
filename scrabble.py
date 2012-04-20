from index import *
from numpy import *

DEBUG = False
COLOR = False

class Board(object):
    LEFT  = 0
    DOWN  = 1
    RIGHT = 2
    UP    = 3
    
    EMPTY = '-'
    
    DOUBLE_LETTER = 1
    TRIPLE_LETTER = 2
    DOUBLE_WORD   = 3
    TRIPLE_WORD   = 4

    DOUBLE_LETTER_COLOR = '\033[46m'
    TRIPLE_LETTER_COLOR = '\033[44m'
    DOUBLE_WORD_COLOR = '\033[45m'
    TRIPLE_WORD_COLOR = '\033[41m'
    BOLD = '\033[1m'
    ENDC = '\033[0m'
    
    VALUES = { "a": 1, "c": 3, "b": 3, "e": 1, "d": 2, "g": 2, 
               "f": 4, "i": 1, "h": 4, "k": 5, "j": 8, "m": 3, 
               "l": 1, "o": 1, "n": 1, "q": 10, "p": 3, "s": 1, 
               "r": 1, "u": 1, "t": 1, "w": 4, "v": 4, "y": 4, 
               "x": 8, "z": 10 } 
    
    def __init__(self, dictionary):
        
        self.board = array([ ['-' for n in range(0, 15)] for j in range(0, 15)] , dtype=str )
        self.extras = zeros( (15,15), dtype=int )

        self.height = self.board.shape[0]
        self.width = self.board.shape[1]

        self.dictionary = dictionary

        for row, col in [ (0,  0), (0,  7), (7,  0) ]:
            self.extras[row              ][col             ] = self.TRIPLE_WORD
            self.extras[self.height-row-1][col             ] = self.TRIPLE_WORD
            self.extras[row              ][self.width-col-1] = self.TRIPLE_WORD
            self.extras[self.height-row-1][self.width-col-1] = self.TRIPLE_WORD

        for row, col in [ (1,5), (5,1), (5, 5) ]: 
            self.extras[row              ][col             ] = self.TRIPLE_LETTER
            self.extras[self.height-row-1][col             ] = self.TRIPLE_LETTER
            self.extras[row              ][self.width-col-1] = self.TRIPLE_LETTER
            self.extras[self.height-row-1][self.width-col-1] = self.TRIPLE_LETTER
        
        for row, col in [ (0,3), (2,6), (3, 0), (3, 7), (6, 2), (6,6), (7,3) ]: 
            self.extras[row              ][col             ] = self.DOUBLE_LETTER
            self.extras[self.height-row-1][col             ] = self.DOUBLE_LETTER
            self.extras[row              ][self.width-col-1] = self.DOUBLE_LETTER
            self.extras[self.height-row-1][self.width-col-1] = self.DOUBLE_LETTER
        
        for row, col in [ (1,1), (2,2), (3, 3), (4, 4), (7, 7) ]: 
            self.extras[row              ][col             ] = self.DOUBLE_WORD
            self.extras[self.height-row-1][col             ] = self.DOUBLE_WORD
            self.extras[row              ][self.width-col-1] = self.DOUBLE_WORD
            self.extras[self.height-row-1][self.width-col-1] = self.DOUBLE_WORD

        if not COLOR:

            self.DOUBLE_LETTER_COLOR = ''
            self.TRIPLE_LETTER_COLOR = ''
            self.DOUBLE_WORD_COLOR = ''
            self.TRIPLE_WORD_COLOR = ''
            self.BOLD = ''
            self.ENDC = ''
            
        if DEBUG:
            print self
             
    def __str__(self):

        buff = list()
        
        buff.append( '+' + '-'*(2*self.width+1) + '+\n' )
        for row in range(0, self.height):
            buff.append('|')
            for col in range(0, self.width):
                
                current = self.board[row][col]
                extra = self.extras[row][col]

                style = self.BOLD if current != self.EMPTY else ''

                if extra == self.DOUBLE_LETTER:
                    color = self.DOUBLE_LETTER_COLOR
                elif extra == self.TRIPLE_LETTER:
                    color = self.TRIPLE_LETTER_COLOR
                elif extra == self.DOUBLE_WORD:
                    color = self.DOUBLE_WORD_COLOR
                elif extra == self.TRIPLE_WORD:
                    color = self.TRIPLE_WORD_COLOR
                else:
                    color = self.ENDC
                
                #if current != self.EMPTY:
                #    color = self.ENDC 
                
                buff.append( ' ' + color + style + current + self.ENDC )
                 
            buff.append(' |\n')
        buff.append( '+' + '-'*(2*self.width+1) + '+' )
        
        return ''.join(buff)


    def valid_cross(self, row, col, direction,  letter):    
        #Get left and right orthoginal directions, to check cross words
        if direction == self.RIGHT:
            pre_dir = self.UP
            post_dir = self.DOWN

        if direction == self.DOWN:
            pre_dir = self.LEFT
            post_dir = self.RIGHT
        
        #Left is always a prefix (for down or right moves), and right always a postfix
        prefix  = self.get_slice(row + self.d_rowoffset(pre_dir) , col + self.d_coloffset(pre_dir) , pre_dir)
        postfix = self.get_slice(row + self.d_rowoffset(post_dir), col + self.d_coloffset(post_dir), post_dir) 
        
        if prefix or postfix:
            return self.dictionary.contains(prefix + letter + postfix)
        else:
            return True
   
    def all_plays(self, letters):
        for row in range(0, self.height):
            for col in range(0, self.width):
                if self.board[row][col] != self.EMPTY:
                    continue

                for play in self.plays(row, col, self.RIGHT, letters):
                    yield (row, col, self.RIGHT, play)
                for play in self.plays(row, col, self.DOWN, letters):
                    yield (row, col, self.DOWN, play)

    def plays(self, row, col, direction, letters):
        ''' Yields every valid play starting at row, col, in specified direction, which uses the specified letters '''
        
        if self.board[row][col] != self.EMPTY:
            return

        opposite = self.d_opp(direction)

        #Find a prefix already on the board, if it exists
        prefix = self.get_slice(row + self.d_rowoffset(opposite), col + self.d_coloffset(opposite), opposite)
        
        for play in self.continuations(row, col, direction, self.dictionary.find(prefix), letters, "", False):
            if DEBUG:
                print "DEBUG found play: %i %i %s (score: %i)" % (row, col, play, self.score(row, col, direction, play) )
                temp = self.board.copy()
                self.play(row, col, direction, play)
                self.board = temp
            yield play
    
    def continuations(self, row, col, direction, dict_node, letters, play_prefix, connected):
        ''' Yields every valid continuation of a play, at row, col, in the specified direction, with dict_node specifying the current word prefix, and play prefix the tiles that would be played to give the word (not including any tiles that may be on the board, but form part of the word). '''
        if not dict_node:
            return
        
        if not self.is_valid_position(row, col):
            if dict_node.final and play_prefix and connected:
                #If we have run off the side of the board, but have a valid word, yield it
                yield play_prefix
            return
                 
        next_row = row + self.d_rowoffset(direction)
        next_col = col + self.d_coloffset(direction)
        current = self.board[row][col]

        #A letter already occupies this square.  If there is a word that continues from here, explore those continuations.
        if current!= self.EMPTY:
            if current in dict_node:
                for play in self.continuations( next_row, next_col, direction, dict_node[current], letters, play_prefix, connected ):
                    yield play

        #We have an empty square, explore all possible continuations
        else:
            
            #If we already have a valid word, yield it
            if dict_node.final and play_prefix and connected: 
                yield play_prefix

            branches = set(letters).intersection(set(dict_node.keys()))
            for l in branches:
                if not self.valid_cross(row, col, direction, l):
                    continue
                    
                for play in self.continuations( next_row, next_col, direction, dict_node[l], letters.replace(l, "", 1), play_prefix + l, connected or self.is_connected(row, col)):
                    yield play

    def print_play(self, row, col, direction, s):
        tmp = self.board.copy()
        self.play(row, col, direction, s)
        print self
        self.board = tmp
    
    def best_plays(self, letters, n=None):
        ''' Returns the n best plays '''
        
        plays = map( lambda p: (self.score(*p), p), self.all_plays(letters) )
        plays.sort()
        plays.reverse()
        return plays[0:n]


    def cross_score(self, row, col, direction, l):
        pass 

    def score(self, row, col, direction, s, cross=True):
        opposite = self.d_opp(direction)
        
        word_mult = 1
        scores = list()
        cross_scores = list()

        #Add prefix letters to score, without any letter multipliers
        prefix = self.get_slice(row + self.d_rowoffset(opposite), col + self.d_coloffset(opposite), opposite)
        scores.extend( map( lambda l: self.VALUES[l], prefix ) )
        
        n = 0
        while self.is_valid_position(row, col) and n < len(s):
            current = self.board[row][col]
            extra = self.extras[row][col]
            if current == self.EMPTY:
                scores.append( self.VALUES[s[n]] )
                n += 1
                
                if extra == self.DOUBLE_LETTER:
                    scores[-1] *= 2
                elif extra == self.TRIPLE_LETTER:
                    scores[-1] *= 3

                elif extra == self.DOUBLE_WORD:
                    word_mult *= 2
                elif extra == self.TRIPLE_WORD:
                    word_mult *= 3
            else:
                scores.append( self.VALUES[current] )
           
            
            
            row += self.d_rowoffset(direction)
            col += self.d_coloffset(direction)

        #Add prefix letters to score, without any letter multipliers
        postfix= self.get_slice(row, col, direction)
        scores.extend( map( lambda l: self.VALUES[l], postfix ) )
             
        return sum(scores)*word_mult + (50 if len(s) == 7 else 0)
    
    def is_connected(self, row, col):
        ''' Returns true if the specified row/col is adjacent (not diagonal) to an occupied square '''
        if self.is_valid_position(row+1, col) and self.board[row+1][col] != self.EMPTY:
            return True 
        if self.is_valid_position(row-1, col) and self.board[row-1][col] != self.EMPTY:
            return True 
        if self.is_valid_position(row, col+1) and self.board[row][col+1] != self.EMPTY:
            return True 
        if self.is_valid_position(row, col-1) and self.board[row][col-1] != self.EMPTY:
            return True 
        
        return False


   
    def is_valid_position(self, row, col):
        return self.is_valid_row(row) and self.is_valid_col(col)
         
    def is_valid_row(self, row):
        return 0 <= row and row < self.height
    
    def is_valid_col(self, col):
        return 0 <= col and col < self.width
    
    def d_opp(self, direction):
        ''' Opposite direction '''
        if direction == self.UP:
            return self.DOWN
        if direction == self.RIGHT:
            return self.LEFT
        if direction == self.DOWN:
            return self.UP
        if direction == self.RIGHT:
            return self.LEFT

    def d_rotr(self, direction):
        ''' Rotate direction right '''
        if direction == self.UP:
            return self.RIGHT
        if direction == self.RIGHT:
            return self.DOWN
        if direction == self.DOWN:
            return self.LEFT
        if direction == self.LEFT:
            return self.UP

    def d_rotl(self, direction):
        ''' Rotate direction left '''
        if direction == self.UP:
            return self.LEFT
        if direction == self.RIGHT:
            return self.UP
        if direction == self.DOWN:
            return self.RIGHT
        if direction == self.LEFT:
            return self.DOWN

    def d_rowoffset(self, direction):
        if direction == self.DOWN:
            return 1
        if direction == self.UP:
            return -1
        else:
            return 0

    def d_coloffset(self, direction):
        if direction == self.RIGHT:
            return 1
        if direction == self.LEFT:
            return -1
        else:
            return 0
     
    def play(self, row, col, direction, s):
        for c in s:
            while self.board[row][col] != self.EMPTY:
                row += self.d_rowoffset(direction)
                col += self.d_coloffset(direction)
            self.board[row][col] = c
        
        if DEBUG:
            print self

    def get_slice(self, row, col, direction):
        buff = list()
        while self.is_valid_position(row, col)  and self.board[row][col] != self.EMPTY:
            buff.append(self.board[row][col])
            row += self.d_rowoffset(direction)
            col += self.d_coloffset(direction)
        
        if direction == self.UP or direction == self.LEFT:
            buff.reverse()

        return ''.join(buff)
 
