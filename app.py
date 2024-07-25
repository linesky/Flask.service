from flask import Flask, render_template, request, send_file
import wave
import numpy as np
import io
#pip install Flask
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            frequency = int(request.form['frequencia'])
            duration = int(request.form['segundos'])

            # Create the WAV file
            sample_rate = 44100
            t = np.linspace(0, duration, int(sample_rate * duration), False)
            audio_data = 0.5 * np.sin(2 * np.pi * frequency * t)
            audio_data = (audio_data * 32767).astype(np.int16)

            buffer = io.BytesIO()
            with wave.open(buffer, 'wb') as wf:
                wf.setnchannels(1)
                wf.setsampwidth(2)
                wf.setframerate(sample_rate)
                wf.writeframes(audio_data.tobytes())

            buffer.seek(0)

            return send_file(buffer, as_attachment=True, download_name='tone.wav', mimetype='audio/wav')
        except Exception as e:
            return str(e), 400

    return render_template('index.html')
print("\x1bc\x1b[47;34m")
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

