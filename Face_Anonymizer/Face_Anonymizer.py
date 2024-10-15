import cv2

# Load the pre-trained face detection model (Haar Cascade)
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Open video capture (0 for webcam or provide video file path)
cap = cv2.VideoCapture(0)  # Replace 0 with 'path_to_video.mp4' for a video file

# Get frame width and height
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Define the codec and create VideoWriter objects
fourcc = cv2.VideoWriter_fourcc(*'XVID')  # Codec for saving videos in .avi format
original_writer = cv2.VideoWriter('original_video_output.mp4', fourcc, 20.0, (frame_width, frame_height))
anonymized_writer = cv2.VideoWriter('face_anonymizer_output.mp4', fourcc, 20.0, (frame_width, frame_height))

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame")
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Detect faces
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    
    # Anonymize faces by applying Gaussian blur
    for (x, y, w, h) in faces:
        # Extract the region of interest (the face)
        face_region = frame[y:y+h, x:x+w]
        # Apply Gaussian blur to the face region
        blurred_face = cv2.GaussianBlur(face_region, (99, 99), 30)
        # Replace the face region in the original frame with the blurred version
        frame[y:y+h, x:x+w] = blurred_face

    # Write the original and anonymized frames to the respective video files
    original_writer.write(frame)            # Save the original frame to the original video
    anonymized_writer.write(frame)           # Save the frame with anonymized faces

    # Display the output
    cv2.imshow('Face Anonymizer', frame)

    # Break the loop on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture and writer objects, and close all OpenCV windows
cap.release()
original_writer.release()
anonymized_writer.release()
cv2.destroyAllWindows()
