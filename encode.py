import cv2
from skimage import io

image = io.imread("bg.png")
image = cv2.cvtColor(image,cv2.COLOR_RGBA2BGRA)
cv2.imencode('.png',image)[1].tofile("bg.png")