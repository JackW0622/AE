# AC: 


 
#rather to achieve Artificial consciousness, we need to think about the road/pathway to achieve artificial consciousness. The idea of artificial consciousness is perhaps a bit too risky, that we cannot fully interpret and control yet. However, I am confident that with the development on the way, we can harvest some of the most interesting "sideproducts" : AGI. AGI refers to the artificial general intelligence, where it can performs any tasks just like a human does. My focus is to try to simulate/create a small/simple version of AGI application in clinical medicine, using AI to help recognise not only emotions, but pain level.

concept: Use the existing facial recognition database and application as a start, further allow the model to learn more complicated data like muscle movement when painful. Another thought is to combine it with various devices: health monitoring devices to assist to have a more accurate prediction of the pain level, which helps the doctors to assist. Furthermore, I hope to build a base for the future AI doctors to be able to give social care to patients, enhancing their capabilities:

First, use OpenCV to allow the capture of facial expressions;
A very small sections of code allowing faces to be extracted:
```
import cv2
print(cv2.__version__)
import cv2

image = cv2.imread('IMG_1664.jpeg')
cv2.imshow('Image', image)

cv2.waitKey(0)
cv2.destroyAllWindows()
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))


for (x, y, w, h) in faces:
    cv2.rectangle(image, (x, y), (x+w, y+h), (255, 0, 0), 2)

cv2.imshow('Face Detection', image)
cv2.waitKey(0)
cv2.destroyAllWindows()

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
```
Improvements: We could download the faces for further manipulation, with also multiple faces.

```
import os


dest_folder = "cropped_faces"
if not os.path.exists(dest_folder):
    os.makedirs(dest_folder)


!pip install opencv-python-headless
import cv2
print(cv2.__version__)
from google.colab.patches import cv2_imshow

image = cv2.imread('/content/test image/test 2.jpg')


if image is None:
  print("Error: Image not loaded. Check the file path.")
else:

  cv2_imshow(image)


  cv2.waitKey(0)
  cv2.destroyAllWindows()

  face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')


  gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

  faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

  if len(faces) > 0:
   for i, (x, y, w, h) in enumerate(faces):
    face_crop = image[y:y+h, x:x+w]

 
    face_path = os.path.join(dest_folder, f"face_{i+1}.jpg")
    cv2.imwrite(face_path, face_crop)

    print(f"Face {i+1} saved as {face_path}")
    cv2_imshow(face_crop)

  else:
    print("No faces detected in the image.")
```
This is the result when run on google colab:
<img width="623" alt="Screenshot 2024-11-24 at 22 40 09" src="https://github.com/user-attachments/assets/238ae607-17d6-4d9c-97ec-31810ba6d6f7">
<img width="387" alt="Screenshot 2024-11-24 at 22 40 15" src="https://github.com/user-attachments/assets/0cf79ff0-6ed8-4b14-a2cc-a3ad770743a8">

It is a good base for me to work further into facial emotion processing
