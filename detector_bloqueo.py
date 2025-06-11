import cv2
import time
import os

# Inicializa el detector de rostros de OpenCV
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

# Configuración
CAMERA_INDEX = 0
NO_FACE_THRESHOLD = 5  # segundos sin detectar rostro

# Variables de control
last_face_time = time.time()

# Captura de la cámara
cap = cv2.VideoCapture(CAMERA_INDEX)

print("Iniciando detección de presencia... Presiona 'q' para salir.")

try:
    while True:
        ret, frame = cap.read()
        if not ret:
            print("No se pudo acceder a la cámara.")
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

        if len(faces) > 0:
            last_face_time = time.time()
            print("Rostro detectado.")
        else:
            no_face_duration = time.time() - last_face_time
            print(f"No hay rostro desde hace {int(no_face_duration)} segundos.")

            if no_face_duration > NO_FACE_THRESHOLD:
                print("No se detectó rostro por 5 segundos. Bloqueando sesión...")
                os.system("rundll32.exe user32.dll,LockWorkStation")
                break  # Detiene la app tras bloquear

        if cv2.waitKey(1000) & 0xFF == ord('q'):  # Espera 1 segundo entre capturas
            break

finally:
    cap.release()
    cv2.destroyAllWindows()
