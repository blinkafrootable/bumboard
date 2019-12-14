from board_analyzer import Analyzer
import keyboard
import time
import sys

def main():
    print('Setting Up...')
    analyzer = Analyzer()

    while True:
        auto_show_response = input('Do you want the resulting image of the board scan to automatically show? [Y/N]').lower().strip()
        if auto_show_response == 'y':
            analyzer.auto_show = True
            break
        elif auto_show_response == 'n':
            analyzer.auto_show = False
            break
        else:
            print('Give a valid response (Y or N)')

    print('Press the key that you want to use to scan the analyze the game board...')
    scan_hotkey = keyboard.read_key()
    keyboard.add_hotkey(scan_hotkey, analyze_board, args=(analyzer, None))

    print('You are ready to go! Press {} to analyze the gameboard.\nMake sure that The Legend of Bumbo is full screen and on your primary monitor when you scan the screen.'.format(scan_hotkey))
    keyboard.wait()

def analyze_board(analyzer, _):
    print('Scanning...')
    analyzer.analyze()
    print('Done!')


if __name__== "__main__":
  main()