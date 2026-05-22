<!DOCTYPE html>
<html lang="fi">
<head>
    <meta charset="UTF-8">
    <title>Digi-Apuri | PC-KEISARI</title>
    <style>
        body { font-family: 'Segoe UI', sans-serif; margin: 0; background: #f9f9f9; }
        .container { max-width: 900px; margin: 0 auto; padding: 2rem; }
        .ai-container { border: 2px solid #ddd; border-radius: 15px; overflow: hidden; background: white; }
        .ai-header { background: #2c3e50; color: white; padding: 15px; text-align: center; }
        /* Tähän upotat Streamlit-linkkisi */
        .chat-frame { width: 100%; height: 600px; border: none; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Digi-Apuri</h1>
        <div class="ai-container">
            <div class="ai-header">PC-Keisarin älyapuri</div>
            <iframe src="https://sinun-sovelluksesi-osoite.streamlit.app" class="chat-frame"></iframe>
        </div>
    </div>
</body>
</html>
