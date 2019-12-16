# bumboard
This is a Python program that uses a trained convolutional network to identify the tiles on the Legend of Bumbo gameboard and mark the available moves on the board.

The following Python modules need to be installed in order to run this program:
- keyboard
- pyautogui
- pillow
- numpy
- cv2
- tensorflow
- keras

This command should install them all:
`pip install keyboard pyautogui pillow numpy cv2 tensorflow keras`

When scanning the board, make sure your mouse it outside the red area:
![Bumbo screenshot with red box around the game board](https://github.com/blinkafrootable/bumboard/blob/master/github-resources/no-mouse-zone.png)

If you choose the automatically show the results of the board scan, they will automatically open in your default image-viewing software. Otherwise, the result will save as result.png in the same directory as main.py
![Bumbo screenshot scanned with moves showing](https://github.com/blinkafrootable/bumboard/blob/master/github-resources/scanned-board.png)

The big boxes highlighting the tiles at the edges of the board indicate 4+ in a row that are split by the edges of the board.

The lines between tiles indicate that a move can be made by moving the tile marked with a circle to the tile marked with a square.
