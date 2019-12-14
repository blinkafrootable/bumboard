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
    time.sleep(0.1)
    stop_hotkey = ''
    while True:
        print('Press the key that you want to use to close this program...')
        stop_hotkey = keyboard.read_key()
        if stop_hotkey != scan_hotkey:
            break
        print('Make sure the stop hotkey is not the same as the analyze hotkey!')
    keyboard.add_hotkey(stop_hotkey, quit_program)

    print('You are ready to go! Press {} to analyze the gameboard and {} to exit this program (or just quit out).\nMake sure that The Legend of Bumbo is full screen and on your primary monitor when you scan the screen.'.format(scan_hotkey, stop_hotkey))
    keyboard.wait()

def analyze_board(analyzer, dumby):
    print('Scanning...')
    analyzer.analyze()
    print('Done!')

def quit_program():
    quit() 


if __name__== "__main__":
  main()