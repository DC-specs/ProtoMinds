import cv2
import serial
import time

#classifier initialization
classifierFace = cv2.CascadeClassifier('haarcascade_file location')

arduino = serial.Serial('serial_port', 9600)

videoCam = cv2.VideoCapture()

if not videoCam.isOpened():
    print("No camera found")
    exit()

cv2.namedWindow("Body Tracking", cv2.WINDOW_NORMAL)
cv2.setWindowProperty("Body Tracking", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

while True:
    ret, frame = videoCam.read()
    if ret:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = classifierFace.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=2)

        if len(body) > 0:
            x, y, w, h = faces[0]
            center_x = x + w // 2
            center_y = y + h // 2

            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            
            arduino.write(f"{center_x},{center_y}\n".encode())


            cv2.putText(frame, f"({center_x}, {center_y})", (x, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

        cv2.imshow("Face Tracking", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

videoCam.release()
cv2.destroyAllWindows()
