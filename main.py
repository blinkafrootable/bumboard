from board_analyzer import Analyzer
import keyboard
import time
import sys

def main():
    print('Setting Up...')
    analyzer = Analyzer()

    print('Press the key that you want to use to scan the analyze the game board...')
    scan_hotkey = keyboard.read_key()
    keyboard.add_hotkey(scan_hotkey, analyze_board, args=(analyzer, None))

    print('You are ready to go! Press {} to analyze the gameboard.\nMake sure that The Legend of Bumbo is full screen and on your primary monitor when you scan the screen.'.format(scan_hotkey))
    keyboard.wait()

def analyze_board(analyzer, dumby):
    print('Scanning...')
    analyzer.analyze()
    print('Done!')


if __name__== "__main__":
  main()