import cv2
from pyzbar import pyzbar
import RPi.GPIO as GPIO
import requests

GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.IN)

def scanner(frame):
    barcodes = pyzbar.decode(frame)
    if len(barcodes) != 0:
        for barcode in barcodes:
            (x, y, w, h) = barcode.rect
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
            barcode_data = barcode.data.decode("utf-8")
            barcode_type = barcode.type
            text = "{} ({})".format(barcode_data, barcode_type)
            cv2.putText(frame, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
            print("[INFO] Found {} barcode: {}".format(barcode_type, barcode_data))
    return frame

def main():
    cap = cv2.VideoCapture(0)
    while cap.isOpened():
        input_state = GPIO.input(18)
        print(input_state)
        _, frame = cap.read()
        frame = scanner(frame)
        cv2.imshow('image', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
