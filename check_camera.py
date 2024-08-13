"""Sensu plugin to check the connectivity of an IP camera."""
import sys
import os
import cv2

def check_camera_connectivity(camera_url):
    """Check the connectivity of an IP camera."""
    # pylint: disable=broad-except
    # pylint: disable=no-member
    try:
        stderr_fd = sys.stderr.fileno()
        devnull_fd = os.open(os.devnull, os.O_WRONLY)
        os.dup2(devnull_fd, stderr_fd)

        cap = cv2.VideoCapture(camera_url)
        if not cap.isOpened():
            print("CRITICAL: Could not open video stream from IP camera.")
            sys.exit(2)  # Exit with status 2 to indicate a critical error

        ret, _ = cap.read()
        if not ret:
            print("CRITICAL: Could not read frame from IP camera.")
            sys.exit(2)  # Exit with status 2 to indicate a critical error

        print("OK: IP camera is accessible and streaming video.")
        sys.exit(0)  # Exit with status 0 to indicate success

    except Exception as e:
        print(f"CRITICAL: Exception occurred: {e}")
        sys.exit(2)  # Exit with status 2 to indicate a critical error

    finally:
        cap.release()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: check_ip_camera.py <camera_url>")
        sys.exit(3)  # Exit with status 1 to indicate a usage error

    cameraurl = sys.argv[1]
    check_camera_connectivity(cameraurl)

