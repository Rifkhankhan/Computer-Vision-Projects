# saperate videso
# import numpy as np
# import cv2

# def get_red_limits():
#     # Define the lower and upper limits for red in HSV
#     lower_red1 = np.array([0, 100, 100], dtype=np.uint8)    # Lower red (hue from 0 to 10)
#     upper_red1 = np.array([10, 255, 255], dtype=np.uint8)

#     lower_red2 = np.array([170, 100, 100], dtype=np.uint8)  # Upper red (hue from 170 to 180)
#     upper_red2 = np.array([180, 255, 255], dtype=np.uint8)

#     return (lower_red1, upper_red1), (lower_red2, upper_red2)

# def detect_red(frame):
#     # Convert the frame to HSV
#     hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

#     # Get the red color ranges
#     (lower_red1, upper_red1), (lower_red2, upper_red2) = get_red_limits()

#     # Create two masks to cover the red hue range
#     mask1 = cv2.inRange(hsv_frame, lower_red1, upper_red1)
#     mask2 = cv2.inRange(hsv_frame, lower_red2, upper_red2)

#     # Combine the two masks
#     red_mask = cv2.bitwise_or(mask1, mask2)

#     # Apply the mask to the original frame
#     red_detected = cv2.bitwise_and(frame, frame, mask=red_mask)

#     return red_detected, red_mask

# # Open video capture (0 for webcam or provide video file path)
# video_capture = cv2.VideoCapture(0)  # Use 'cv2.VideoCapture('path_to_video.mp4')' for video file

# # Get frame width and height
# frame_width = int(video_capture.get(3))
# frame_height = int(video_capture.get(4))

# # Define the codec and create VideoWriter objects for each video
# fourcc = cv2.VideoWriter_fourcc(*'XVID')  # Codec for saving videos in .avi format

# # Create VideoWriter objects for original, red-detected, and red-mask videos
# original_writer = cv2.VideoWriter('original_output.mp4', fourcc, 20.0, (frame_width, frame_height))
# red_detected_writer = cv2.VideoWriter('red_detected_output.mp4', fourcc, 20.0, (frame_width, frame_height))
# red_mask_writer = cv2.VideoWriter('red_mask_output.mp4', fourcc, 20.0, (frame_width, frame_height), isColor=False)

# while True:
#     # Capture each frame from the video stream
#     ret, frame = video_capture.read()

#     if not ret:
#         print("Failed to grab frame")
#         break

#     # Detect red color in the current frame
#     red_detected, red_mask = detect_red(frame)

#     # Write the frames to the respective video files
#     original_writer.write(frame)            # Original video
#     red_detected_writer.write(red_detected)  # Red-detected video
#     red_mask_writer.write(red_mask)          # Red mask video

#     # Display the results
#     cv2.imshow("Original Video", frame)
#     cv2.imshow("Red Detected", red_detected)
#     cv2.imshow("Red Mask", red_mask)

#     # Break the loop on 'q' key press
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# # Release the video capture and writer objects and close windows
# video_capture.release()
# original_writer.release()
# red_detected_writer.release()
# red_mask_writer.release()
# cv2.destroyAllWindows()



# one videoe

import cv2
import numpy as np

# Load the three saved videos
original_video = cv2.VideoCapture('original_output.avi')
red_detected_video = cv2.VideoCapture('red_detected_output.avi')
red_mask_video = cv2.VideoCapture('red_mask_output.avi')

# Get frame dimensions and frame rate from one of the videos
frame_width = int(original_video.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(original_video.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = original_video.get(cv2.CAP_PROP_FPS)

# Create VideoWriter for the combined output video
fourcc = cv2.VideoWriter_fourcc(*'XVID')
output_video = cv2.VideoWriter('merged_output.avi', fourcc, fps, (frame_width * 3, frame_height))

while True:
    # Read frames from each video
    ret1, original_frame = original_video.read()
    ret2, red_detected_frame = red_detected_video.read()
    ret3, red_mask_frame = red_mask_video.read()

    # If any video ends, stop the loop
    if not ret1 or not ret2 or not ret3:
        break

    # Convert red_mask_frame to a 3-channel image (BGR) to match the other frames
    red_mask_frame_colored = cv2.cvtColor(red_mask_frame, cv2.COLOR_GRAY2BGR)

    # Concatenate the three frames horizontally (side by side)
    combined_frame = cv2.hconcat([original_frame, red_detected_frame, red_mask_frame_colored])

    # Write the combined frame to the output video
    output_video.write(combined_frame)

    # Display the combined video for preview
    cv2.imshow("Merged Video", combined_frame)

    # Break the loop on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video captures and writer
original_video.release()
red_detected_video.release()
red_mask_video.release()
output_video.release()
cv2.destroyAllWindows()
