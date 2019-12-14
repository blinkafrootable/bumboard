
from PIL import Image, ImageDraw
import pyautogui
import time
import math
import os
import argparse
import colorsys
import logging
from predict import Predictor
from board import Board

class Analyzer:

    def __init__(self):

        self.category_map = {
            'b' : 'bone',
            's' : 'booger',
            'k' : 'corn',
            'c' : 'curse',
            'h' : 'heart',
            'u' : 'pee',
            'p' : 'poop',
            't' : 'tooth',
            'w' : 'wild'
        }
        self.category_count_map = {
            'b' : 0,
            's' : 0,
            'k' : 0,
            'c' : 0,
            'h' : 0,
            'u' : 0,
            'p' : 0,
            't' : 0,
            'w' : 0
        }

        # screen scaling based off of 4k (3840x2160) resolution
        self.BR_X_START_SCALE = 292.0/3840.0
        self.BR_Y_START_SCALE = 1838.0/2160.0
        self.BR_X_JUMP_SCALE = 233.0/3840.0
        self.BR_X_SIZE_SCALE = 240.0/3840.0

        self.SBR_X_START_SCALE = 400.0/3840.0
        self.SBR_Y_START_SCALE = 1602.0/2160.0
        self.SBR_X_JUMP_SCALE = 210.0/3840.0
        self.SBR_X_SIZE_SCALE = 210.0/3840.0

        self.STR_X_START_SCALE = 520.0/3840.0
        self.STR_Y_START_SCALE = 1434.0/2160.0
        self.STR_X_JUMP_SCALE = 185.0/3840.0
        self.STR_X_SIZE_SCALE = 180.0/3840.0

        self.TR_X_START_SCALE = 600.0/3840.0
        self.TR_Y_START_SCALE = 1291.0/2160.0
        self.TR_X_JUMP_SCALE = 170.0/3840.0
        self.TR_X_SIZE_SCALE = 150.0/3840.0

        logging.getLogger('keras').setLevel(logging.CRITICAL)
        logging.getLogger('tensorflow').setLevel(logging.CRITICAL)

        #construct the argument parser and parse the arguments
        ap = argparse.ArgumentParser()
        ap.add_argument("-w", "--width", required=False, help="screen pixel width")
        ap.add_argument("-hi", "--height", required=False, help="screen pixel height")
        args = vars(ap.parse_args())

        self.screen_size_x, self.screen_size_y = pyautogui.size()
        if args['width'] != None: # override the screen width and height if input
            self.screen_size_x = int(args['width'])
        if args['height'] != None:
            self.screen_size_y = int(args['height'])

        self.board = Board()
        self.predictor = Predictor('NN/boardidentifier.model', 'NN/boardidentifier_lb.pickle')
    
    def analyze(self):

        bottom_row = []
        second_bottom_row = []
        second_top_row = []
        top_row = []

        image = pyautogui.screenshot()
        image.save('screenshot.png')
        image = Image.open('screenshot.png')

        bottom_row = []
        second_bottom_row = []
        second_top_row = []
        top_row = []

        # fetch rows' images
        for i in range(0, 9): # bottom row
            cropped_image = image.crop((self.BR_X_START_SCALE*self.screen_size_x+i*self.BR_X_JUMP_SCALE*self.screen_size_x, self.BR_Y_START_SCALE*self.screen_size_y, 
                self.BR_X_START_SCALE*self.screen_size_x+i*self.BR_X_JUMP_SCALE*self.screen_size_x+self.BR_X_SIZE_SCALE*self.screen_size_x, self.BR_Y_START_SCALE*self.screen_size_y+self.BR_X_SIZE_SCALE*self.screen_size_x)).resize((32, 32))
            bottom_row.append(cropped_image)

        output_image = Image.new('L', (32*9*2, 32))
        for i in range(0, 9): # second-to-bottom row
            cropped_image = image.crop((self.SBR_X_START_SCALE*self.screen_size_x+i*self.SBR_X_JUMP_SCALE*self.screen_size_x, self.SBR_Y_START_SCALE*self.screen_size_y, 
                self.SBR_X_START_SCALE*self.screen_size_x+i*self.SBR_X_JUMP_SCALE*self.screen_size_x+self.SBR_X_SIZE_SCALE*self.screen_size_x, self.SBR_Y_START_SCALE*self.screen_size_y+self.SBR_X_SIZE_SCALE*self.screen_size_x)).resize((32, 32))
            second_bottom_row.append(cropped_image)

        output_image = Image.new('L', (32*9*2, 32))
        for i in range(0, 9): # second-to-top row
            cropped_image = image.crop((self.STR_X_START_SCALE*self.screen_size_x+i*self.STR_X_JUMP_SCALE*self.screen_size_x, self.STR_Y_START_SCALE*self.screen_size_y, 
                self.STR_X_START_SCALE*self.screen_size_x+i*self.STR_X_JUMP_SCALE*self.screen_size_x+self.STR_X_SIZE_SCALE*self.screen_size_x, self.STR_Y_START_SCALE*self.screen_size_y+self.STR_X_SIZE_SCALE*self.screen_size_x)).resize((32, 32))
            second_top_row.append(cropped_image)

        output_image = Image.new('L', (32*9*2, 32))
        for i in range(0, 9): # top row
            cropped_image = image.crop((self.TR_X_START_SCALE*self.screen_size_x+i*self.TR_X_JUMP_SCALE*self.screen_size_x, self.TR_Y_START_SCALE*self.screen_size_y, 
                self.TR_X_START_SCALE*self.screen_size_x+i*self.TR_X_JUMP_SCALE*self.screen_size_x+self.TR_X_SIZE_SCALE*self.screen_size_x, self.TR_Y_START_SCALE*self.screen_size_y+self.TR_X_SIZE_SCALE*self.screen_size_x)).resize((32, 32))
            top_row.append(cropped_image)

        # setup board based on NN predictions
        for i in range(9):
            self.board.set(0, i, self.predictor.predict(top_row[i]))
            self.board.set(1, i, self.predictor.predict(second_top_row[i]))
            self.board.set(2, i, self.predictor.predict(second_bottom_row[i]))
            self.board.set(3, i, self.predictor.predict(bottom_row[i]))

        # get all moves from the board
        moves = self.board.get_moves()

        if len(moves) == 0:
            print('No moves available.')
        else:
            screenshot = Image.open('screenshot.png').convert('RGBA')
            hsv_hue = 0
            hue_step = 1.0/len(moves)
            frequency_board = [[0 for x in range(9)] for y in range(4)] # keeps track of the number of times each tile is in a shift
            uses_board = [[0 for x in range(9)] for y in range(4)] # keeps track of how many times a shift node has been placed in the tile
            for move in moves:
                if move[0] == Board.SHIFT:
                    frequency_board[move[1]][move[2]] += 1
                    frequency_board[move[3]][move[4]] += 1
            for move in moves:
                overlay_image = Image.new('RGBA', screenshot.size, (0,0,0,0))
                overlay_draw = ImageDraw.Draw(overlay_image)
                rgb_color = self.hsv2rgb(hsv_hue, 1, 1)
                if move[0] == Board.SHIFT:
                    move_start = self.board_to_screen_position((self.screen_size_x, self.screen_size_y), move[1], move[2], frequency_board, uses_board)
                    move_end = self.board_to_screen_position((self.screen_size_x, self.screen_size_y), move[3], move[4], frequency_board, uses_board)
                    overlay_draw.line((move_start, move_end), fill=(rgb_color[0], rgb_color[1], rgb_color[2], 122), width=10)
                    overlay_draw.ellipse(((move_start[0]-20, move_start[1]-20), (move_start[0]+20, move_start[1]+20)), fill=(rgb_color[0], rgb_color[1], rgb_color[2], 122))
                    overlay_draw.rectangle(((move_end[0]-20, move_end[1]-20), (move_end[0]+20, move_end[1]+20)), fill=(rgb_color[0], rgb_color[1], rgb_color[2], 122))
                elif move[0] == Board.SPLIT:
                    for c in move[2]:
                        tile_pos = self.board_to_screen_position((self.screen_size_x, self.screen_size_y), move[1], c, None, None)
                        overlay_draw.rectangle(((tile_pos[0]-40, tile_pos[1]-40), (tile_pos[0]+40, tile_pos[1]+40)), fill=(rgb_color[0], rgb_color[1], rgb_color[2], 122))
                hsv_hue += hue_step
                screenshot = Image.alpha_composite(screenshot, overlay_image)
            screenshot = screenshot.resize((1280, 720))
            screenshot.save('result.png', 'PNG')
        os.remove('screenshot.png')

    def board_to_screen_position(self, screen_size, r, c, frequency_board, uses_board):
        y_start = 0
        self.screen_size_x, self.screen_size_y = screen_size
        if r == 0:
            y_start = self.TR_Y_START_SCALE*self.screen_size_y
            x_start = self.TR_X_START_SCALE*self.screen_size_x
            y_pos = y_start + self.TR_X_SIZE_SCALE*self.screen_size_x/2
            x_pos = self.TR_X_START_SCALE*self.screen_size_x+c*self.TR_X_JUMP_SCALE*self.screen_size_x + self.TR_X_SIZE_SCALE*self.screen_size_x/2
            if frequency_board != None and uses_board != None:
                x_pos += math.cos(math.pi*2/frequency_board[r][c] * uses_board[r][c] + math.pi/4) * 30
                y_pos += math.sin(math.pi*2/frequency_board[r][c] * uses_board[r][c] + math.pi/4) * 30
                uses_board[r][c] += 1
            return (x_pos, y_pos)
        elif r == 1:
            y_start = self.STR_Y_START_SCALE*self.screen_size_y
            x_start = self.STR_X_START_SCALE*self.screen_size_x
            y_pos = y_start + self.STR_X_SIZE_SCALE*self.screen_size_x/2
            x_pos = self.STR_X_START_SCALE*self.screen_size_x+c*self.STR_X_JUMP_SCALE*self.screen_size_x + self.STR_X_SIZE_SCALE*self.screen_size_x/2
            if frequency_board != None and uses_board != None:
                x_pos += math.cos(math.pi*2/frequency_board[r][c] * uses_board[r][c] + math.pi/4) * 30
                y_pos += math.sin(math.pi*2/frequency_board[r][c] * uses_board[r][c] + math.pi/4) * 30
                uses_board[r][c] += 1
            return (x_pos, y_pos)
        elif r == 2:
            y_start = self.SBR_Y_START_SCALE*self.screen_size_y
            x_start = self.SBR_Y_START_SCALE*self.screen_size_x
            y_pos = y_start + self.SBR_X_SIZE_SCALE*self.screen_size_x/2
            x_pos = self.SBR_X_START_SCALE*self.screen_size_x+c*self.SBR_X_JUMP_SCALE*self.screen_size_x + self.SBR_X_SIZE_SCALE*self.screen_size_x/2
            if frequency_board != None and uses_board != None:
                x_pos += math.cos(math.pi*2/frequency_board[r][c] * uses_board[r][c] + math.pi/4) * 30
                y_pos += math.sin(math.pi*2/frequency_board[r][c] * uses_board[r][c] + math.pi/4) * 30
                uses_board[r][c] += 1
            return (x_pos, y_pos)
        elif r == 3:
            y_start = self.BR_Y_START_SCALE*self.screen_size_y
            x_start = self.BR_Y_START_SCALE*self.screen_size_x
            y_pos = y_start + self.BR_X_SIZE_SCALE*self.screen_size_x/2
            x_pos = self.BR_X_START_SCALE*self.screen_size_x+c*self.BR_X_JUMP_SCALE*self.screen_size_x + self.BR_X_SIZE_SCALE*self.screen_size_x/2
            if frequency_board != None and uses_board != None:
                x_pos += math.cos(math.pi*2/frequency_board[r][c] * uses_board[r][c] + math.pi/4) * 30
                y_pos += math.sin(math.pi*2/frequency_board[r][c] * uses_board[r][c] + math.pi/4) * 30
                uses_board[r][c] += 1
            return (x_pos, y_pos)
        return None

    def hsv2rgb(self, h,s,v):
        return tuple(round(i * 255) for i in colorsys.hsv_to_rgb(h,s,v))