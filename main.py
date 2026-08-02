import cv2
import numpy as np


# stuff that might change based on user input
asciiGradient = ' .\'`^",:;Il!i><~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$'    # from densest to lightest char
asciiGradientSize = len(asciiGradient)
columns = 150


camera = cv2.VideoCapture(0)
if camera.isOpened():
    isWorking, data = camera.read()     # get first frame
else:
    isWorking = False
    print('Failed to open camera')


height, width, _ = data.shape
grayscaleWeights = np.array([0.11, 0.59, 0.3])  # BGR format
grayscaleImage = np.empty((height, width), dtype=np.uint8)


tileWidth = width / columns
tileHeight = tileWidth * 2
rows = int(height / tileHeight)


print('\033[48;2;0;0;0m')
while isWorking:

    # for y in range(height):
    #     for x in range(width):
    #         grayscaleImage[y][x] = np.dot(data[y, x], grayscaleWeights).astype(np.uint8)
    grayscaleImage = np.dot(data, grayscaleWeights).astype(np.uint8)


    asciiImage = ''
    for y in range(rows):
        y1 = int(y * tileHeight)
        y2 = int((y + 1) * tileHeight)

        if y == rows - 1:
            y2 = height

        for x in range(columns):
            x1 = int(x * tileWidth)
            x2 = int((x + 1) * tileWidth)

            if x == columns - 1:
                x2 = width

            average = grayscaleImage[y1:y2, x1:x2].mean()
            char = asciiGradient[int(average * (asciiGradientSize - 1) / 255)]
            r = data[y1:y2, x1:x2, 2].mean().astype(np.uint8)
            g = data[y1:y2, x1:x2, 1].mean().astype(np.uint8)
            b = data[y1:y2, x1:x2, 0].mean().astype(np.uint8)
            asciiImage += f'\033[38;2;{r};{g};{b}m'
            asciiImage += char

        asciiImage += '\n'

    print('\033[H', end='')
    print(asciiImage, end='')
    

    isWorking, data = camera.read()


print('\033[0m', end='')
camera.release()
