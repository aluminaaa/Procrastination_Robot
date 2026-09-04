import cv2
import time
import subprocess
import random
from gtts import gTTS
import pygame

pygame.mixer.init()

INSULTS_DEADLINE = [
#here i just add specific/creative insults/reminders for whenever I have a deadline 
]

INSULTS_GESTURE = [
#here i just add specific/creative insults/reminders for whenever it detects 67 
]

INSULTS_PHONE
#here i just add specific/creative insults/reminders for whenever I'm on my phone for too long
]




def speak(text):
    print(f"\n[Insult Bot]: {text}\n")
    try:
        tts = gTTS(text=text, lang='en')
        tts.save("temp_speech.mp3")
        pygame.mixer.music.load("temp_speech.mp3")
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            time.sleep(0.1)
        pygame.mixer.music.unload()
    except Exception as e:
        print(f"Audio error: {e}")




def check_calcurse_deadlines():
    try:
        result = subprocess.run(["calcurse", "-r5"], capture_output=True, text=True)
        output = result.stdout.strip()
        if output:
            print(f"[Calendar Event Found]:\n{output}")
            speak(random.choice(INSULTS_DEADLINE))
            return True
    except Exception as e:
        print(f"Calendar check error: {e}")
    return False





cap = cv2.VideoCapture(0)

CALENDAR_CHECK_INTERVAL = 1800  # 30 minutes
PHONE_THRESHOLD_SECONDS = 900    # 15 minutes

last_cal_check = 0
presence_timer_start = None
bg_subtractor = cv2.createBackgroundSubtractorMOG2(history=100, varThreshold=50)

print("Starting... Press 'q' to quit.")

try:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        try:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        current_time = time.time()
        if current_time - last_cal_check > CALENDAR_CHECK_INTERVAL:
            check_calcurse_deadlines()
            last_cal_check = current_time

        fg_mask = bg_subtractor.apply(frame)
        contours, _ = cv2.findContours(fg_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        large_movement_count = 0
        for cnt in contours:
            if cv2.contourArea(cnt) > 5000:
                large_movement_count += 1

        if large_movement_count >= 2:
            speak(random.choice(INSULTS_GESTURE))
            time.sleep(5)

        # D. Presence / Phone Usage Timer
        if large_movement_count > 0:
            if presence_timer_start is None:
                presence_timer_start = current_time
            elif current_time - presence_timer_start > PHONE_THRESHOLD_SECONDS:
                speak(random.choice(INSULTS_PHONE))
                presence_timer_start = current_time
        else:
            presence_timer_start = None

        # Display feed
        cv2.imshow('Insult Bot - OpenCV Feed', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

finally:
    cap.release()
    cv2.destroyAllWindows()
