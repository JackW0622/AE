# AC: 


 
#rather to achieve Artificial consciousness, we need to think about the road/pathway to achieve artificial consciousness. The idea of artificial consciousness is perhaps a bit too risky, that we cannot fully interpret and control yet. However, I am confident that with the development on the way, we can harvest some of the most interesting "sideproducts" : AGI. AGI refers to the artificial general intelligence, where it can performs any tasks just like a human does. My focus is to try to simulate/create a small/simple version of AGI application in clinical medicine, using AI to help recognise not only emotions, but pain level.

concept: Use the existing facial recognition database and application as a start, further allow the model to learn more complicated data like muscle movement when painful. Another thought is to combine it with various devices: health monitoring devices to assist to have a more accurate prediction of the pain level, which helps the doctors to assist. Furthermore, I hope to build a base for the future AI doctors to be able to give social care to patients, enhancing their capabilities:

First, use OpenCV to allow the capture of facial expressions;
A very small sections of code allowing faces to be extracted:

!pip install opencv-python-headless
import cv2
print(cv2.__version__)
from google.colab.patches import cv2_imshow 

image = cv2.imread('IMG_1664.jpeg')


if image is None:
  print("Error: Image not loaded. Check the file path.")
else:
 
  cv2_imshow(image)


  cv2.waitKey(0)
  cv2.destroyAllWindows()

  face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')


  gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

  faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

  for (x, y, w, h) in faces:
    cv2.rectangle(image, (x, y), (x+w, y+h), (255, 0, 0), 2)


  cv2_imshow(image)

  cv2.waitKey(0)
  cv2.destroyAllWindows()
