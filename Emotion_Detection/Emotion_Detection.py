import cv2
from fer import FER

# Initialize the emotion detector
emotion_detector = FER()

# Open video capture (0 for webcam or provide video file path)
cap = cv2.VideoCapture(0)  # Replace 0 with 'path_to_video.mp4' for a video file

# Get frame width and height
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Define the codec and create VideoWriter object for saving the output video
fourcc = cv2.VideoWriter_fourcc(*'XVID')
output_writer = cv2.VideoWriter('emotion_detection_output.mp4', fourcc, 20.0, (frame_width, frame_height))

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame")
        break

    # Detect emotions in the current frame
    emotions = emotion_detector.detect_emotions(frame)

    # Draw rectangles around detected faces and label with the predominant emotion
    for emotion in emotions:
        x, y, w, h = emotion['box']  # Get bounding box for the face
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Get the emotion with the highest score
        dominant_emotion = max(emotion['emotions'], key=emotion['emotions'].get)
        emotion_score = emotion['emotions'][dominant_emotion]

        # Put the emotion label on the frame
        label = f"{dominant_emotion}: {emotion_score:.2f}"
        cv2.putText(frame, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Write the frame to the output video file
    output_writer.write(frame)

    # Display the output
    cv2.imshow('Emotion Detection', frame)

    # Break the loop on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture and writer objects, and close all OpenCV windows
cap.release()
output_writer.release()
cv2.destroyAllWindows()
