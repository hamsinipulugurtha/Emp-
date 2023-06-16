import cv2
import face_recognition
import os
import numpy as np
from matplotlib import pyplot as plt
from google.colab.patches import cv2_imshow

known_faces = []
known_names = []
folder_path = '/workspace/emp-/images'
for file_name in os.listdir(folder_path):
    image_path = os.path.join(folder_path, file_name)
    image = face_recognition.load_image_file(image_path)
    face_encodings = face_recognition.face_encodings(image)

    if len(face_encodings) > 0:
        face_encoding = face_encodings[0]
        known_faces.append(face_encoding)
        known_names.append(file_name.split('.')[0])  # Extract name from file name
    else:
        #print(f"No face detected in {file_name}")
        pass

# print("Known faces and names:")
# for name in known_names:
#     print(name)
def print_all_frames(video_path):
    # Open the video file
    cap = cv2.VideoCapture(video_path)

    # Read and display all frames
    frame_count = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Display the frame
        #frame = cv2.resize(frame, (320, 240))

        #cv2_imshow(frame)

        frame_count += 1
    print(frame_count)

    # Release the video capture
    cap.release()

# Specify the path to the video file in your Google Drive
video_path = '/workspace/emp-/Video_file.mp4'

# # Call the function to print all frames
print_all_frames(video_path)
import datetime

def photos_print(video_path):
  count = 0
  cap = cv2.VideoCapture(video_path)

  frame_counter = 0
  attendance_dict = {}  # Dictionary to store attendance data

  # Get the original frame size
  width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
  height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

  # Calculate the cropping coordinates
  crop_x = (width - min(width, height)) // 2
  crop_y = (height - min(width, height)) // 2
  crop_width = min(width, height)
  crop_height = min(width, height)

  # Desired square frame size
  square_size = 500

  # Output video writer
  #out = cv2.VideoWriter('output_video.mp4', cv2.VideoWriter_fourcc(*'mp4v'), 30, (square_size, square_size))

  while cap.isOpened():
      ret, frame = cap.read()
      if not ret:
          break
      count += 1

      if count % 20 !=0:
        continue

      cropped_frame = frame[crop_y:crop_y+crop_height, crop_x:crop_x+crop_width]

      # Resize the square portion to the desired square frame size
      frame = cv2.resize(cropped_frame, (square_size, square_size))

      # Find faces in the frame
      face_locations = face_recognition.face_locations(frame)
      face_encodings = face_recognition.face_encodings(frame, face_locations)

      if len(face_locations) == 0:
          # Skip the frame if no faces are detected
          continue

      # Iterate over each detected face
      for face_encoding, face_location in zip(face_encodings, face_locations):
          # Compare face encoding with the known faces
          matches = face_recognition.compare_faces(known_faces, face_encoding)
          name = "Unknown"

          # Find the best match
          if len(matches) > 0:
              face_distances = face_recognition.face_distance(known_faces, face_encoding)
              best_match_index = np.argmin(face_distances)
              if matches[best_match_index]:
                  name = known_names[best_match_index]

                  # Update attendance dictionary with name and timestamp
                  attendance_dict[name] = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")

              # Draw a box around the face and label the name
              top, right, bottom, left = face_location
              cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
              cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

      # Write the frame to the output video
      #out.write(frame)

      # Display the resulting frame
      cv2_imshow(frame)
      print(count)

  cap.release()
  #out.release()
  cv2.destroyAllWindows()
  return attendance_dict
video_path = '/workspace/emp-/Video_file.mp4'
a = photos_print(video_path)
print(a)
import pandas as pd

# Convert attendance dictionary to DataFrame
df = pd.DataFrame.from_dict(a, orient='index', columns=['Timestamp'])

# Split timestamp into separate date and time columns
df[['Date', 'Time']] = df['Timestamp'].str.split(' ', 1, expand=True)

# Rename the first column as "Name"
df = df.rename(columns={0: 'Name'})

df.to_csv('Attendance.csv',index = True)