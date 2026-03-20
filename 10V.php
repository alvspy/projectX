<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>10В класс - 179 Network</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 10px 20px;
            background-color: #f8f9fa;
            background-image: url(https://upload.wikimedia.org/wikipedia/commons/thumb/c/c1/%D0%A8%D0%BA%D0%BE%D0%BB%D0%B0_179_%D0%9C%D0%98%D0%9E%D0%9E%2C_%D0%9C%D0%BE%D1%81%D0%BA%D0%B2%D0%B0.jpg/1200px-%D0%A8%D0%BA%D0%BE%D0%BB%D0%B0_179_%D0%9C%D0%98%D0%9E%D0%9E%2C_%D0%9C%D0%BE%D1%81%D0%BA%D0%B2%D0%B0.jpg);
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
            position: relative;
        }
        
        body::before {
            content: '';
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(248, 249, 250, 0.7);
            z-index: -1;
        }
        
        :root {
            --title-size: 36px;
            --title-color: #2c3e50;

            --description-size: 18px;
            --description-color: #596162;

            --button-size: 14px;
            --button-color: rgb(52, 152, 219);
            --button-text-color: white;
            --button-width: 120px;
            --button-height: 35px;
        }

        .container {
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 15px;
        }

        .top-back-button {
            align-self: flex-start;
            border: none;
            border-radius: 6px;
            cursor: pointer;
            font-weight: bold;
            transition: all 0.3s ease;
            display: flex;
            align-items: center;
            justify-content: center;
            text-decoration: none;
            font-size: 14px;
            background-color: #596162;
            color: white;
            width: 100px;
            height: 35px;
            margin-bottom: 5px;
        }

        .top-back-button:hover {
            background-color: #7f8c8d;
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        }

        .title {
            font-size: var(--title-size);
            color: var(--title-color);
            text-align: center;
            margin-bottom: 1px;
            font-weight: bold;
        }

        .description {
            font-size: var(--description-size);
            color: var(--description-color);
            text-align: center;
            margin-bottom: 5px;
            line-height: 1.5;
        }

        .photo-placeholder {
            color: #7f8c8d;
            font-size: 14px;
            text-align: center;
        }

        .sections-container {
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 30px;
            width: 100%;
            max-width: 900px;
        }

        @media (max-width: 768px) {
            .sections-container {
                grid-template-columns: 1fr;
            }
            
            .members-container {
                grid-template-columns: repeat(2, 1fr);
            }
            
            .section {
                max-width: 500px;
            }
        }

        @media (max-width: 480px) {
            .members-container {
                grid-template-columns: 1fr;
            }
            
            .class-teacher-section {
                max-width: 250px;
            }
            
            .class-teacher-photo {
                width: 200px;
                height: 200px;
            }
            
            .member-photo {
                width: 120px;
                height: 120px;
            }
            
            .section {
                max-width: 300px;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <button class="top-back-button" onclick="window.location.href='index.php'">← Назад</button>
        <h1 class="title">10В класс</h1>
        <p class="description">Made by <a href="https://t.me/alvspy">Lion</a>, <a href="https://t.me/fuckingshitagain">Kebab</a>, <a href="https://t.me/MiniBesss">Imp</a> and <a href="https://t.me/t0hrepus">Field</a></p>
        <p class="description">Информация об учениках и учителях класса</p>
    </div>
</body>
</html>
