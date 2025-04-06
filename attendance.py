import cv2
import pandas as pd
from datetime import datetime
import time

# load OpenCV face detector
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# manual name mapping (update with ur friends’ pics)
known_faces = {
    "Vittal-photo.jpg": "Vittal",
    "Prasanna.jpg": "Prasanna",
    "sahaj.jpg": "Sahaj"
}

# start webcam
cap = cv2.VideoCapture(0)
attendance = []
logged_names = set()  # track who’s logged
blink_state = True  # for toggling blink
last_blink = time.time()  # track blink timing

while True:
    ret, frame = cap.read()
    if not ret:
        print("webcam’s toast. rip")
        break

    # detect faces
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    # default red box when no face
    if len(faces) == 0:
        cv2.rectangle(frame, (50, 50, 590, 430), (0, 0, 255), 2)

    for idx, (x, y, w, h) in enumerate(faces):
        # assign name based on order of detection
        name = known_faces.get(list(known_faces.keys())[idx % len(known_faces)], "unknown")

        # log if known and not logged yet
        if name != "unknown" and name not in logged_names:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            attendance.append({"name": name, "time": timestamp})
            logged_names.add(name)
            print(f"{name} clocked in at {timestamp}")

        # box logic
        if name != "unknown":
            color = (0, 255, 0)  # green for known
            cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
            cv2.putText(frame, name, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)
        else:
            # blink red for unknown
            current_time = time.time()
            if current_time - last_blink >= 0.5:
                blink_state = not blink_state
                last_blink = current_time
            color = (0, 0, 255) if blink_state else (0, 0, 0)
            cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
            cv2.putText(frame, "unknown", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)

    cv2.imshow("attendance cam", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):  # press Q to quit
        break

# save to CSV
df = pd.DataFrame(attendance)
df.to_csv("attendance_log.csv", index=False)
print("saved to attendance_log.csv")

cap.release()
cv2.destroyAllWindows()