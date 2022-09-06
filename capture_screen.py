
import time
import cv2
import mss
import numpy


with mss.mss() as sct:
   # Part of the screen to capture
   monitor1 = {'top': 40, 'left': 0, 'width': 800, 'height': 640}
   monitor2 = {'top': 40, 'left': 840, 'width': 800, 'height': 640}


   while 'Screen capturing':
      last_time = time.time()

      # Get raw pixels from the screen, save it to a Numpy array
      img1 = numpy.array(sct.grab(monitor1))
      img2 = numpy.array(sct.grab(monitor2))


      # Display the picture
      cv2.imshow('first', img1)
      cv2.imshow('second', img2)


      # Display the picture in grayscale
      # cv2.imshow('OpenCV/Numpy grayscale',
      # cv2.cvtColor(img, cv2.COLOR_BGRA2GRAY))

      print('fps: {0}'.format(1 / (time.time()-last_time)))

      # Press "q" to quit
      if cv2.waitKey(25) & 0xFF == ord('q'):
         cv2.destroyAllWindows()
         break