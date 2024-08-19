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
            status = f"CRITICAL: Could not open IP camera at {camera_url}"
            exit_code = 2  # Exit with status 2 to indicate a critical error
            return status, exit_code

        ret, _ = cap.read()
        if not ret:
            status = f"CRITICAL: Could not open IP camera at {camera_url}"
            exit_code = 2  # Exit with status 2 to indicate a critical error
            return status, exit_code

        status = f"OK: IP camera is accessible and streaming video at {camera_url}"
        exit_code = 0  # Exit with status 2 to indicate a critical error
        return status, exit_code

    except Exception as e:
        status = f"CRITICAL exception: {e}"
        exit_code = 2  # Exit with status 2 to indicate a critical error
        return status, exit_code

    finally:
        cap.release()

def read_ips_from_config(file_path):
    """Read IP addresses from a config file."""
    ip_list = []
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding="utf-8") as file:
            ip_list = [line.strip() for line in file if line.strip()]
    else:
        print(f"Config file {file_path} not found.")

    return ip_list

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: check_ip_camera.py <camera_conf>")
        sys.exit(3)  # Exit with status 1 to indicate a usage error

    camera_conf = sys.argv[1]
    camera_urls = read_ips_from_config(camera_conf)
    exit_status = []
    camera_status = []
    for cameraurl in camera_urls:
        status, exit_code = check_camera_connectivity(cameraurl)
        camera_status.append(status)
        exit_status.append(exit_code)

    print("\n".join(camera_status))
    sys.exit(max(exit_status))
