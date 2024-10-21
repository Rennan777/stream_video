from flask import Flask, render_template, Response
import cv2

app = Flask(__name__)

# Inicializa a captura de vídeo da câmera (0 é o índice da câmera padrão)
camera = cv2.VideoCapture(0)

def generate_frames():
    while True:
        success, frame = camera.read()  # Lê um frame da câmera
        if not success:
            break
        # Codifica o frame como JPEG
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()  # Converte para bytes
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # Cria o stream

@app.route('/')
def index():
    return render_template('index.html')  # Renderiza o template HTML

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')  # Cria o feed de vídeo

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)  # Inicia o servidor
