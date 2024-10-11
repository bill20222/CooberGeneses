
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <title>Chatbot Online</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 20px;
        }
        #chat {
            border: 1px solid #ccc;
            padding: 10px;
            height: 300px;
            overflow-y: scroll;
        }
        #inputArea {
            margin-top: 10px;
        }
        #newResponseArea {
            display: none; /* Oculta a área inicialmente */
            margin-top: 10px;
        }
    </style>
</head>
<body>
    <h1>Chatbot Online</h1>
    <div id="chat"></div>
    <div id="inputArea">
        <input type="text" id="pergunta" placeholder="Digite sua pergunta">
        <button onclick="sendQuestion()">Enviar</button>
    </div>
    <div id="newResponseArea">
        <h3>Adicionar Nova Resposta</h3>
        <label for="newPergunta">Pergunta:</label>
        <input type="text" id="newPergunta">
        <label for="newResposta">Resposta:</label>
        <input type="text" id="newResposta">
        <button onclick="saveNewResponse()">Salvar</button>
    </div>
    <script>
        function sendQuestion() {
            const pergunta = document.getElementById('pergunta').value;
            fetch('/ask', {
                method: 'POST',
                headers: {'Content-Type': 'application/x-www-form-urlencoded'},
                body: new URLSearchParams({pergunta: pergunta})
            })
            .then(response => response.json())
            .then(data => {
                const chat = document.getElementById('chat');
                chat.innerHTML += `<div>Você: ${pergunta}</div>`;

                // Verifica se a resposta é para ensinar uma nova resposta
                if (data.resposta.includes("Você deseja me ensinar uma nova resposta?")) {
                    chat.innerHTML += `<div>Chatbot: ${data.resposta}</div>`;
                    document.getElementById('newResponseArea').style.display = 'block'; // Mostra a área para nova resposta
                } else {
                    chat.innerHTML += `<div>Chatbot: ${data.resposta}</div>`;
                    document.getElementById('newResponseArea').style.display = 'none'; // Esconde a área para nova resposta
                }

                // Adiciona a reprodução de áudio
                const audio = new Audio(data.audio);
                audio.play();

                document.getElementById('pergunta').value = '';
                chat.scrollTop = chat.scrollHeight;
            });
        }

        function saveNewResponse() {
            const pergunta = document.getElementById('newPergunta').value;
            const resposta = document.getElementById('newResposta').value;
            fetch('/add', {
                method: 'POST',
                headers: {'Content-Type': 'application/x-www-form-urlencoded'},
                body: new URLSearchParams({pergunta: pergunta, resposta: resposta})
            })
            .then(response => response.json())
            .then(data => {
                const chat = document.getElementById('chat');
                chat.innerHTML += `<div>Chatbot: ${data.resposta}</div>`;
                document.getElementById('newPergunta').value = '';
                document.getElementById('newResposta').value = '';
                document.getElementById('newResponseArea').style.display = 'none'; // Esconde a área após salvar
                chat.scrollTop = chat.scrollHeight;
            });
        }
    </script>
</body>
</html>
