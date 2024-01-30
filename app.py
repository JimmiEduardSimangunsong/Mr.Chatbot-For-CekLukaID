import vertexai
from flask_socketio import send, SocketIO
from vertexai.language_models import ChatModel, InputOutputTextPair
from flask import Flask
from flask_cors import CORS  # Import the CORS extension

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app)
socketio.init_app(app, cors_allowed_origins="*")

vertexai.init(project="capstone-project-c23-pc635", location="us-central1")
chat_model = ChatModel.from_pretrained("chat-bison")
parameters = {
    "candidate_count": 1,
    "max_output_tokens": 1024,
    "temperature": 0.2,
    "top_p": 0.8,
    "top_k": 40
}
chat = chat_model.start_chat(
    context="""Anda adalah Mr.Chat Luka, chatbot layanan pengguna untuk Cek Luka App Anda hanya menjawab pertanyaan 
    pelanggan tentang dunia kesehatan, terutama Pennaganan Luka Ringan dan luka, pola hidup sehat, saran kesehatan,hindari membahas diluar konteks kesehatan.""",
)


# Define a Socket.IO event handler for receiving messages
@socketio.on('message')
def handle_message(msg):
    response = chat.send_message(msg, **parameters)
    # Send the response back to the client that sent the original message
    send(str(response.text))


if __name__ == '__main__':
    socketio.run(app, port=8080, use_reloader=True)