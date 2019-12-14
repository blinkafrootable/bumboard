
class Board:

    SHIFT = 'shift'
    SPLIT = 'split'

    def __init__(self):
        self.board = [['' for x in range(9)] for y in range(4)]

    def set(self, r, c, value):
        self.board[r][c] = value

    def get_moves(self):
        shifts = []
        splits = []
        moves = []

        shifts = self.find_interior_moves()
        for shift in shifts:
            if shift[3] == 'v':
                for r in range(4):
                    if self.board[r][shift[2]] == shift[0] or self.board[r][shift[2]] == 'w': # if the character is the character that needs to go in the spot
                        moves.append([self.SHIFT, r, shift[2], shift[1], shift[2]]) # [move_type, r1, c1, r2, c2] move from (r1, c1) to (r2, c2)
            elif shift[3] == 'h':
                for c in range(9):
                    if self.board[shift[1]][c] == shift[0] or self.board[shift[1]][c] == 'w':
                        moves.append([self.SHIFT, shift[1], c, shift[1], shift[2]]) # [move_type, r1, c1, r2, c2] move from (r1, c1) to (r2, c2)
        splits = self.find_exterior_moves()
        for split in splits:
            moves.append([self.SPLIT, split[0], split[1]])

        return moves

    def find_interior_moves(self):
        shifts = []
        for r in range(4):
            for c in range(6):
                character_count = {}
                for i in range(4):
                    character = self.board[r][c+i]
                    if character not in character_count:
                        character_count[character] = [1, r, c+i] # count, row, column
                    else:
                        character_count[character][0] += 1
                        character_count[character][1] = r
                        character_count[character][2] = c+i
                most_common_character = self.get_most_common_character(character_count)
                if most_common_character[0] != 'k' and most_common_character[0] != 'c':
                    if most_common_character[0] == 'w' and most_common_character[1] == 2: # if 2 wilds
                        non_wilds = []
                        for character in character_count:
                            if character != 'w':
                                non_wilds.append(character)
                        shift = [non_wilds[1], character_count[non_wilds[0]][1], character_count[non_wilds[0]][2], 'v']
                        if shift not in shifts:
                            shifts.append(shift)
                        shift = [non_wilds[0], character_count[non_wilds[1]][1], character_count[non_wilds[1]][2], 'v']
                        if shift not in shifts:
                            shifts.append(shift)
                    elif most_common_character[1] == 3 or most_common_character[1] == 2 and 'w' in character_count and character_count['w'][0] == (3-most_common_character[1]):
                        for character in character_count:
                            if character != most_common_character[0] and character != 'w':
                                shift = [most_common_character[0], character_count[character][1], character_count[character][2], 'v'] # [ideal character, existing character r, existing character c, orientation]
                                if shift not in shifts:
                                    shifts.append(shift)
        for c in range(9):
            character_count = {}
            for r in range(4):
                character = self.board[r][c]
                if character not in character_count:
                    character_count[character] = [1, r, c] # count, row, column
                else:
                    character_count[character][0] += 1
                    character_count[character][1] = r
                    character_count[character][2] = c
            most_common_character = self.get_most_common_character(character_count)
            if most_common_character[0] != 'k' and most_common_character[0] != 'c':
                if most_common_character[0] == 'w' and most_common_character[1] == 2: # if 2 wilds
                    non_wilds = []
                    for character in character_count:
                        if character != 'w':
                            non_wilds.append(character)
                    shift = [non_wilds[1], character_count[non_wilds[0]][1], character_count[non_wilds[0]][2], 'h']
                    if shift not in shifts:
                        shifts.append(shift)
                    shift = [non_wilds[0], character_count[non_wilds[1]][1], character_count[non_wilds[1]][2], 'h']
                    if shift not in shifts:
                        shifts.append(shift)
                elif most_common_character[1] == 3 or most_common_character[1] == 2 and 'w' in character_count and character_count['w'][0] == (3-most_common_character[1]):
                    for character in character_count:
                        if character != most_common_character[0] and character != 'w':
                            shift = [most_common_character[0], character_count[character][1], character_count[character][2], 'h'] # [ideal character, existing character r, existing character c, orientation]
                            if shift not in shifts:
                                shifts.append(shift)
        
        return shifts
    
    def find_exterior_moves(self):
        splits = []
        search_columns = (
            (0, 1, 2, 8),
            (0, 1, 7, 8),
            (0, 6, 7, 8)
        )
        for r in range(4):
            for columns in search_columns:
                letters = set()
                for c in columns:
                    letters.add(self.board[r][c])
                letters = list(letters)
                if len(letters) == 1 or (len(letters) == 2 and (letters[0] == 'w' or letters[1] == 'w')):
                    splits.append((r, columns))
        
        return splits

    def get_most_common_character(self, character_count):
        most_common = ['', 0] # [number of occurances, character]
        for character, count in character_count.items():
            if count[0] > most_common[1]:
                most_common = [character, count[0]]
        return most_common
    
    def __str__(self):
        return '\n'.join([''.join([item + ' ' for item in row]) for row in self.board])