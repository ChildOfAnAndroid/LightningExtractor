import cv2
import os
import time

# Function to process the video and extract lightning frames
def process_video(video_path):
    # Open the video file
    cap = cv2.VideoCapture(video_path)

    # Initialize variables
    prev_frame = None
    lightning_frames = []

    # Create directory to save lightning frames if it doesn't exist
    output_dir = os.path.splitext(video_path)[0] + "_lightning_frames"
    os.makedirs(output_dir, exist_ok=True)

    # Loop through frames
    frame_count = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Increment frame count
        frame_count += 1
        print(f"Processing frame {frame_count}...", end='\r')

        # Check if it's not the first frame
        if prev_frame is not None:
            # Calculate absolute difference between current and previous frame
            diff = cv2.absdiff(frame, prev_frame)

            # Convert difference to grayscale for simplicity
            gray_diff = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)

            # !!!!!!!!!!!! Define a threshold for significant lighting change !!!!!!!!!!!! 
            threshold = 2025000

            # Count number of pixels above the threshold
            count = cv2.countNonZero(gray_diff)
            print(f"Frame {frame_count} = {count}")

            # If a significant change in lighting is detected, store the frame number
            if count > threshold:
                lightning_frames.append(cap.get(cv2.CAP_PROP_POS_FRAMES))
                # Save the lightning frame as an image
                frame_path = os.path.join(output_dir, f"frame_{int(cap.get(cv2.CAP_PROP_POS_FRAMES))}.jpg")
                cv2.imwrite(frame_path, frame)
                print(f"Lightning Detected")

        # Store current frame for comparison in next iteration
        prev_frame = frame

    # Release video capture object
    cap.release()

    return lightning_frames

# Function to create a video from the lightning frames
def create_output_video(video_path, lightning_frames, output_path):
    # Open the video file
    cap = cv2.VideoCapture(video_path)

    # Get video properties
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)

    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    # Loop through frames and write lightning frames to output video
    for frame_num in lightning_frames:
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_num)
        ret, frame = cap.read()
        if ret:
            out.write(frame)

    # Release video capture and writer objects
    cap.release()
    out.release()

# Main function
def main():
    # Input video path
    video_path = input("Enter the path to the video file: ")

    # Start time for processing
    start_time = time.time()

    # Process the video and extract lightning frames
    print("Processing video...")
    lightning_frames = process_video(video_path)
    print("Video processing complete.")

    # End time for processing
    end_time = time.time()

    # Total processing time
    processing_time = end_time - start_time
    print(f"Total processing time: {processing_time:.2f} seconds")

    # Create output video with lightning frames
    print("Creating output video...")
    output_video_path = os.path.splitext(video_path)[0] + "_lightning.mp4"
    create_output_video(video_path, lightning_frames, output_video_path)
    print("Output video saved at:", output_video_path)

if __name__ == "__main__":
    main()
