from flask import Flask, request, jsonify, render_template
import pandas as pd
from gtts import gTTS
import os
import uuid

app = Flask(__name__)

# Nome do arquivo Excel onde as perguntas e respostas serão salvas
excel_file = 'chatbot_data.xlsx'


# Função para carregar dados do Excel
def load_data():
    try:
        return pd.read_excel(excel_file)
    except FileNotFoundError:
        return pd.DataFrame(columns=['Pergunta', 'Resposta'])


# Função para salvar a pergunta e resposta no Excel
def save_data(pergunta, resposta):
    df = load_data()
    new_data = pd.DataFrame({'Pergunta': [pergunta], 'Resposta': [resposta]})
    df = pd.concat([df, new_data], ignore_index=True)
    df.to_excel(excel_file, index=False)


# Função para encontrar a resposta com base na pergunta
def get_response(pergunta):
    df = load_data()
    resposta = df.loc[df['Pergunta'] == pergunta, 'Resposta']
    if not resposta.empty:
        return resposta.values[0]
    else:
        return None  # Retorna None se não souber a resposta


# Função para gerar áudio a partir do texto
def generate_audio(text):
    tts = gTTS(text=text, lang='pt')
    audio_file = f'static/audio/{uuid.uuid4()}.mp3'
    tts.save(audio_file)
    return audio_file


# Rota principal
@app.route('/')
def home():
    return render_template('index.html')


# Rota para enviar uma pergunta
@app.route('/ask', methods=['POST'])
def ask():
    pergunta = request.form.get('pergunta')
    resposta = get_response(pergunta)

    if resposta is None:
        # Se não souber a resposta, pergunta se pode aprender
        resposta = "Desculpe, não sei a resposta para isso. Você deseja me ensinar uma nova resposta?"
    else:
        resposta = resposta

    # Gera áudio da resposta
    audio_file = generate_audio(resposta)
    return jsonify({'resposta': resposta, 'audio': audio_file})


# Rota para adicionar nova resposta
@app.route('/add', methods=['POST'])
def add():
    pergunta = request.form.get('pergunta')
    resposta = request.form.get('resposta')
    save_data(pergunta, resposta)
    return jsonify({'resposta': "Obrigado! Agora sei a resposta."})


if __name__ == '__main__':
    # Cria a pasta static/audio se não existir
    os.makedirs('static/audio', exist_ok=True)
    app.run(debug=True)
