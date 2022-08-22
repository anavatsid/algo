import time
import cv2
import mss
import numpy


class ScreenCap:
   def __init__(self, box) -> None:
      left, top, width, height = box
      self.monitor = {'top': top, 'left': left, 'width': width, 'height': height}
      self.cap = None
      self.img = None
      self.fps = 5
      self.is_stop = False
      self.read()
      
   def isOpened(self):
      if self.img is not None:
         return True 
      else:
         return False

   def get(self, cap_prop_fps):
      return self.fps

   def set(self, cap_prop_fps, fps):
      self.fps = fps
   
   def read(self):
      with mss.mss() as sct:
         if not self.is_stop:
            self.img = numpy.array(sct.grab(self.monitor))
         else:
            self.img = None
      if self.img is not None:
         return True, self.img
      else:
         return False, None
   
   def release(self):
      self.is_stop = True

   def init(self):
      with mss.mss() as sct:
         while not self.is_stop:
            self.img = numpy.array(sct.grab(self.monitor))
                  # Press "q" to quit
            if cv2.waitKey(25) & 0xFF == ord('q'):
               cv2.destroyAllWindows()
               break
         self.img = None




      pass

# with mss.mss() as sct:
#    # Part of the screen to capture
#    monitor1 = {'top': 40, 'left': 0, 'width': 800, 'height': 640}
#    monitor2 = {'top': 40, 'left': 840, 'width': 800, 'height': 640}


#    while 'Screen capturing':
#       last_time = time.time()

#       # Get raw pixels from the screen, save it to a Numpy array
#       img1 = numpy.array(sct.grab(monitor1))
#       img2 = numpy.array(sct.grab(monitor2))


#       # Display the picture
#       cv2.imshow('first', img1)
#       cv2.imshow('second', img2)


#       # Display the picture in grayscale
#       # cv2.imshow('OpenCV/Numpy grayscale',
#       # cv2.cvtColor(img, cv2.COLOR_BGRA2GRAY))

#       print('fps: {0}'.format(1 / (time.time()-last_time)))

#       # Press "q" to quit
#       if cv2.waitKey(25) & 0xFF == ord('q'):
#          cv2.destroyAllWindows()
#          break