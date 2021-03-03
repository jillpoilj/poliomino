# -*- coding: utf-8 -*-
# by Alex Stroev

from __future__ import division

import numpy as np

import itertools
import sys

    

class PoliBase(object):
    
    def __init__(self, width, height):
        self.width = width
        self.height = height


class PoliSquare(PoliBase):

    def __init__(self, width, height):
        super(PoliSquare, self).__init__(width, height)
        
    def check_and_place(self, x, y, rotation, field):
        if rotation == 0:
            if x + self.width > field.shape[0] or y + self.height > field.shape[1]:
                return False
            for i in range(x, x+self.width):
                for j in range(y, y+self.height):
                    if field[i][j] == 0:
                        field[i][j] = 1
                    else:
                        return False
            return True
        else:
            if x + self.height > field.shape[0] or y + self.width > field.shape[1]:
                return False
            for i in range(x, x+self.height):
                for j in range(y, y+self.width):
                    if field[i][j] == 0:
                        field[i][j] = 1
                    else:
                        return False
            return True
        
    def get_states(self, width, height):
        """
        returns iterator of all possible positions of this polio
        """
        
        max_x = width - self.width
        max_y = height - self.height
        s1 =  list(itertools.product(range(max_x + 1), range(max_y + 1), [0]))
        
        if self.width == self.height:
            return s1
        
        #rotated
        max_x = width - self.height
        max_y = height - self.width
        s2 = list(itertools.product(range(max_x + 1), range(max_y + 1), [1]))
        return s1 + s2
        
class PoliL(PoliBase):

    def __init__(self, width, height):
        super(PoliL, self).__init__(width, height)


    def check_and_place(self, x, y, rotation, field):
        # x to the right, y to the top
        if rotation == 0:
            # \_ shape
            p1 = PoliSquare(1, self.height) 
            p2 = PoliSquare(self.width - 1, 1) 
            if not p1.check_and_place(x, y, 0, field):
                return False
            if not p2.check_and_place(x + 1, y, 0, field):
                return False
        elif rotation == 1:
            # _| shape
            p1 = PoliSquare(self.height, 1) 
            p2 = PoliSquare(1, self.width - 1)  
            if not p1.check_and_place(x, y, 0, field):
                return False
            if not p2.check_and_place(x + self.height - 1, y + 1, 0, field):
                return False
        elif rotation == 2:
            # ^| shape
            p1 = PoliSquare(1, self.height) 
            p2 = PoliSquare(self.width - 1, 1)  
            if not p1.check_and_place(x + self.width - 1, y, 0, field):
                return False
            if not p2.check_and_place(x, y + self.height - 1, 0, field):
                return False
        else:
            # |^ shape
            p1 = PoliSquare(self.height, 1) 
            p2 = PoliSquare(1, self.width - 1)
            if not p1.check_and_place(x, y + self.width - 1, 0, field):
                return False
            if not p2.check_and_place(x, y, 0, field):
                return False
        return True
        
    def get_states(self, width, height):
        """
        returns iterator of all possible positions of this polio
        """
        
        max_x = width - self.width
        max_y = height - self.height
        s1 = list(itertools.product(range(max_x + 1), range(max_y + 1), [0, 2]))
        
        #rotated
        max_x = width - self.height
        max_y = height - self.width
        s2 = list(itertools.product(range(max_x + 1), range(max_y + 1), [1, 3]))
        return s1 + s2

def solve_poliomino(width, height, polis):
    fields = [np.zeros((width, height))]
    for poli in polis: 
        states = poli.get_states(width, height)
        new_fields = []
        print('Next poli:')
        for field in fields:
            # print('Field now is: ')
            # print(field)
            for state in states:
                new_field = field.copy()
                if poli.check_and_place(*state, field=new_field):
                    new_fields.append(new_field)
            #         print(state, ' : ')
            #         print(new_field)
            # print('End field')
        fields = new_fields
        
        
    if fields:
        print('Possible!')
        return True
    else:
        print('Impossible')
        return False

def solve_poliomino_depth(width, height, polis):
    fields = [np.zeros((width, height))]
    for poli in polis:
        pass


def parse_input(s):    
    
    fw = int(s[s.find('(')+1 : s.find(',')])
    
    fh = int(s[s.find(',')+1 : s.find(')')])    
    
    qs = s[s.find('2.')+2 : s.find('3.')]
    
    polis = []
    
    while qs.find('((') > -1:
        pw = int(qs[qs.find('((')+2 : qs.find(',')])
        ph = int(qs[qs.find(',')+1 : qs.find('),')])
        t = qs.find('),')
        pn = int(qs[t+2 : qs.find(')', t+2)])
        for _ in range(pn):
            polis.append(PoliSquare(pw, ph))
        qs = qs[qs.find(')', t+2) + 2 : ]
        
    qs = s[s.find('3.')+2 : ]

    while qs.find('((') > -1:
        pw = int(qs[qs.find('((')+2 : qs.find(',')])
        ph = int(qs[qs.find(',')+1 : qs.find('),')])
        t = qs.find('),')
        pn = int(qs[t+2 : qs.find(')', t+2)])
        for _ in range(pn):
            polis.append(PoliL(pw, ph))
        qs = qs[qs.find(')', t+2) + 2 : ]

    return fw, fh, polis

def test():
    
    s = """ 
1. (3, 5)    
2. [((2, 2), 1)]
3. [((3, 2), 1), ((2, 2), 2)]
"""    
    # from task
    width, height, polis = parse_input(s)
    solve_poliomino(width, height, polis)

    # should not be possible
    polis = []
    polis.append(PoliL(3, 4))
    polis.append(PoliL(2, 3))
    polis.append(PoliL(2, 2))
    polis.append(PoliL(2, 2))
    solve_poliomino(4, 4, polis)
    
    s = """ 
1. (10, 6)
2. [((2, 2), 2), ((3, 3), 3)]
3. [((3, 2), 1), ((2, 2), 2)]
"""    
    # bigger board
    width, height, polis = parse_input(s)
    solve_poliomino(width, height, polis)
    
    s = """ 
1. (6, 6)
2. [((4, 4), 1)]
3. [((3, 3), 4)]
"""    
    # dont place square in the corner
    width, height, polis = parse_input(s)
    solve_poliomino(width, height, polis)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Please specify input file, for example: ')
        print('>>> python poliomino.py input.txt')
    else:
        with open(sys.argv[1], 'r') as file:
            s = file.read()
            width, height, polis = parse_input(s)
            solve_poliomino(width, height, polis)