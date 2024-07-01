import mediapipe as mp
import cv2
import time
import dobot as ctl

def determine_pointing_direction(index_finger_tip, index_finger_mcp):
    if index_finger_tip.x < index_finger_mcp.x:
        print('right')
        ctl.GoRight()
        return 'right'
    elif index_finger_tip.x > index_finger_mcp.x:
        print('left')
        ctl.GoLeft()
        return 'left'
    else:
        print('undetermined')
        return 'undetermined'


def determine_pointing_direction2(thumb_tip, thumb_mcp):
    if thumb_tip.y < thumb_mcp.y:
        print('up')
        ctl.GoUp()
        return 'up'
    elif thumb_tip.y > thumb_mcp.y:
        print('down')
        ctl.GoDown()
        return 'down'
    else:
        print('undetermined')
        return 'undetermined'

ctl.connect()
# Initialize MediaPipe Holistic.
mp_drawing = mp.solutions.drawing_utils
mp_holistic = mp.solutions.holistic

cap = cv2.VideoCapture(0)  # Use the default webcam.

# Initiate holistic model.
with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("Ignoring empty camera frame.")
            continue

        # Convert the frame color from BGR to RGB.
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # To improve performance, optionally mark the image as not writeable.
        image.flags.writeable = False

        # Process the image and make detections.
        results = holistic.process(image)

        image.flags.writeable = True  # Make the image writeable again.
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        # Draw the hand landmarks on the image.
        # Check if right hand landmarks are available.
        """"index left/right"""
        if results.right_hand_landmarks:
            # Extract the coordinates of the tip and MCP of the index finger
            index_finger_tip = results.right_hand_landmarks.landmark[
                mp_holistic.HandLandmark.INDEX_FINGER_TIP]
            index_finger_mcp = results.right_hand_landmarks.landmark[
                mp_holistic.HandLandmark.INDEX_FINGER_MCP]
            # Now safely use the variables since they are defined within this scope
            direction = determine_pointing_direction(
                index_finger_tip, index_finger_mcp)
            print(f"The finger is pointing {direction}.")

            # Draw landmarks and connections on the image
            mp_drawing.draw_landmarks(
                image, results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS,
                mp_drawing.DrawingSpec(
                    color=(80, 22, 10), thickness=2, circle_radius=4),
                mp_drawing.DrawingSpec(color=(80, 44, 121), thickness=2, circle_radius=2))
        else:
            print("No right hand landmarks detected.")

        """"thumb up/down"""

        if results.left_hand_landmarks:
            # Extract the coordinates of the tip and MCP of the index finger
            thumb_mcp = results.left_hand_landmarks.landmark[
                mp_holistic.HandLandmark.THUMB_MCP]
            thumb_tip = results.left_hand_landmarks.landmark[
                mp_holistic.HandLandmark.THUMB_TIP]

            # Now safely use the variables since they are defined within this scope
            direction = determine_pointing_direction2(
                thumb_tip, thumb_mcp)
            print(f"The finger is pointing {direction}.")

            # Draw landmarks and connections on the image
            mp_drawing.draw_landmarks(
                image, results.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS,
                mp_drawing.DrawingSpec(
                    color=(80, 22, 10), thickness=2, circle_radius=4),
                mp_drawing.DrawingSpec(color=(80, 44, 121), thickness=2, circle_radius=2))
        else:
            print("No left hand landmarks detected.")
        # Similar for the left hand, if needed.
        # Display the resulting frame.
        cv2.imshow('Raw Webcam Feed', image)
        if cv2.waitKey(5) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()

"""
left
Index Finger Tip Coordinates : (x: 0.5102996826171875, y: 0.6450017094612122, z: -0.052429839968681335)
Index Finger Mcp Coordinates : (x: 0.262126088142395, y: 0.599713921546936, z: -0.034047987312078476)
right
Index Finger Tip Coordinates : (x: 0.15600472688674927, y: 0.5918487906455994, z: -0.043088823556900024)
Index Finger Mcp Coordinates : (x: 0.3024299442768097, y: 0.5634250044822693, z: -0.016751110553741455)
"""
