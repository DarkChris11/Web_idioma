import os
from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# Obtener las claves API desde las variables de entorno
gemini_api_key = os.getenv("GEMINI_API_KEY")
eleven_labs_api_key = os.getenv("ELEVEN_LABS_API_KEY")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generar_dialogo', methods=['POST'])
def generar_dialogo():
    try:
        # Obtener los datos del formulario
        prompt = request.form['prompt']
        num_frases = int(request.form['num_frases'])
        voice_ids = request.form.getlist('voice_ids')  # Obtener múltiples voice_ids

        # Llamar a la API de Eleven Labs para generar un diálogo
        eleven_labs_response = generate_dialogue_with_eleven_labs(prompt, num_frases, voice_ids)
        
        # Llamar a la API de Gemini si necesitas información adicional (Ejemplo: obtener datos de mercado)
        gemini_response = get_gemini_data()

        # Devolver la respuesta de la API al usuario
        return render_template('index.html', 
                               dialogo=eleven_labs_response['dialogue'], 
                               gemini_data=gemini_response)
    except Exception as e:
        return jsonify({"error": str(e)})

def generate_dialogue_with_eleven_labs(prompt, num_frases, voice_ids):
    url = 'https://api.elevenlabs.io/v1/generate-dialogue'
    data = {
        "prompt": prompt,
        "num_frases": num_frases,
        "voice_ids": voice_ids
    }
    headers = {'Authorization': f'Bearer {eleven_labs_api_key}'}
    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 200:
        return response.json()  # Devolver el diálogo generado
    else:
        return {"error": "Error al generar diálogo"}

def get_gemini_data():
    url = 'https://api.gemini.com/v1/marketdata'
    headers = {'Authorization': f'Bearer {gemini_api_key}'}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()  # Devolver los datos de Gemini
    else:
        return {"error": "Error al obtener datos de Gemini"}

if __name__ == '__main__':
    app.run(debug=True)
