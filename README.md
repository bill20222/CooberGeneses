
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Chatbot</title>

    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f7f7f7;
        }

        .chatbox {
            border: 1px solid #ccc;
            max-width: 600px;
            margin: auto;
            background-color: #fff;
            border-radius: 10px;
            box-shadow: 0px 2px 5px rgba(0, 0, 0, 0.1);
            overflow: hidden;
        }

        .chat-header {
            background-color: #4CAF50;
            color: #fff;
            padding: 10px;
            font-weight: bold;
            text-align: center;
        }

        .chat-messages {
            max-height: 400px;
            overflow-y: scroll;
            padding: 10px;
        }

        .chat-message {
            margin: 10px 0;
        }

        .user-message {
            text-align: right;
            color: #4CAF50;
        }

        .bot-message {
            text-align: left;
            color: #333;
        }

        .chat-input {
            width: calc(100% - 20px);
            padding: 10px;
            border: none;
            border-top: 1px solid #ccc;
            font-size: 16px;
        }

        .chat-input:focus {
            outline: none;
        }

        .chat-send-button {
            width: 40px;
            height: 40px;
            border: none;
            background-color: #4CAF50;
            color: #fff;
            border-radius: 50%;
            cursor: pointer;
            font-size: 20px;
            margin-left: 10px;
        }

        .chat-options {
            text-align: center;
            margin-top: 10px;
        }
    </style>
</head>
<body>
    <div class="chatbox">
        <div class="chat-header">
            Chatbot
        </div>
        <div class="chat-messages" id="chat"></div>
        <div class="chat-input-container">
            <input type="text" class="chat-input" id="userInput" placeholder="Digite sua mensagem...">
            <button class="chat-send-button" onclick="sendMessage()">➤</button>
        </div>
        <div class="chat-options">
            <button onclick="consultarRespostas()">Consultar Respostas</button>
            <div id="respostasSalvas" style="display:none;">
                <h2>Respostas Salvas:</h2>
                <ul id="respostasList"></ul>
            </div>
        </div>
    </div>

    <div id="questionPanel" style="display:none;">
        <h2>Pergunta:</h2>
        <textarea id="questionText" rows="4" cols="50"></textarea>
        <button onclick="submitQuestion()">Enviar Pergunta</button>
    </div>

    <div id="answerPanel" style="display:none;">
        <h2>Resposta:</h2>
        <textarea id="answerText" rows="4" cols="50"></textarea>
        <button onclick="submitAnswer()">Enviar Resposta</button>
    </div>

    <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
    <script>
        var qaPairs = JSON.parse(localStorage.getItem('qaPairs')) || [];

        document.getElementById('userInput').addEventListener('keypress', function(event) {
            if (event.key === 'Enter') {
                sendMessage();
            }
        });

        function falarMensagemBot(mensagem) {
            var synth = window.speechSynthesis;
            var utterance = new SpeechSynthesisUtterance(mensagem);
            synth.speak(utterance);
        }

        function generateBotResponse(message) {
            var botMessage = '<div class="chat-message bot-message">' + message + '</div>';
            var chat = document.getElementById('chat');
            chat.innerHTML += botMessage;
            falarMensagemBot(message); // Fala a resposta
            chat.scrollTop = chat.scrollHeight; // Rolagem automática para o fundo
        }

        function sendMessage() {
            var userInput = document.getElementById('userInput');
            var message = userInput.value.trim();
            if (!message) return; // Ignora mensagens vazias

            userInput.value = '';

            var chat = document.getElementById('chat');
            var userMessage = '<div class="chat-message user-message">' + message + '</div>';
            chat.innerHTML += userMessage;
            chat.scrollTop = chat.scrollHeight; // Rolagem automática para o fundo

            if (qaPairs.length > 0) {
                var foundAnswer = qaPairs.find(qaPair => qaPair.question.toLowerCase() === message.toLowerCase());
                if (foundAnswer) {
                    generateBotResponse(foundAnswer.answer);
                } else {
                    askHowToProceed(message);
                }
            } else {
                askHowToProceed(message);
            }
        }

        function askHowToProceed(question) {
            generateBotResponse("Como proceder com esta informação?");
            document.getElementById('questionText').value = question;
            document.getElementById('questionPanel').style.display = 'block';
        }

        function submitQuestion() {
            var questionText = document.getElementById('questionText').value;
            document.getElementById('answerPanel').style.display = 'block';
            document.getElementById('answerText').focus();
        }

        function submitAnswer() {
            var question = document.getElementById('questionText').value;
            var answer = document.getElementById('answerText').value;

            qaPairs.push({ question: question, answer: answer });
            localStorage.setItem('qaPairs', JSON.stringify(qaPairs));

            generateBotResponse('Obrigado por me ensinar!');

            document.getElementById('questionPanel').style.display = 'none';
            document.getElementById('answerPanel').style.display = 'none';
        }

        function consultarRespostas() {
            var respostasList = document.getElementById('respostasList');
            respostasList.innerHTML = '';

            if (qaPairs.length > 0) {
                qaPairs.forEach(qaPair => {
                    var listItem = document.createElement('li');
                    listItem.innerText = 'Pergunta: ' + qaPair.question + ' - Resposta: ' + qaPair.answer;
                    respostasList.appendChild(listItem);
                });

                document.getElementById('respostasSalvas').style.display = 'block';
            } else {
                alert('Nenhuma resposta salva ainda.');
            }
        }
    </script>
</body>
</html>
