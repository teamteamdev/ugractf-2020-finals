<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8" />
    <title>ОФЦ ——— ВХОД</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/semantic-ui/2.4.1/semantic.min.css" integrity="sha512-8bHTC73gkZ7rZ7vpqUQThUDhqcNFyYi2xgDgPDHc+GXVGHXq+xPjynxIopALmOPqzo9JZj0k6OqqewdGO3EsrQ==" crossorigin="anonymous" />
    <style>
        body {
            background-color: #ddd;
        }

        body > .grid {
            height: 100%;
        }
    </style>
</head>
<body>
<div class="ui container">
    <img src="/static/oi_docs.svg" style="width: 65%; max-height: 200px;" />
</div>
<div class="ui container">
    <h1>Добро пожаловать!</h1>
    <div class="ui blue message">
        <div class="header">Как войти?</div>
        <p>Вход в однофункциональный центр осуществляется с помощью вашего
        сертификата безопасности и утилиты ШифроПро версии не ниже 1.44</p>
        <a href="/static/shifropro.py" class="ui red button">Скачать ШифроПро бесплатно</a>
    </div>
    <p>Ваша авторизационная строка (вставьте в ШифроПро):</p>
    <pre>${challenge}</pre>
    <form method="POST" class="ui stacked segment form">
        <p>Введите данные, которые выведены программой:</p>
        <div class="field">
            <label for="key">Ваш публичный ключ:</label>
            <input type="text" id="key" name="key" required />
        </div>
        <div class="field">
            <label for="high">Ключ высокого уровня:</label>
            <input type="text" id="high" name="high" required />
        </div>
        <div class="field">
            <label for="low">Ключ низкого уровня:</label>
            <input type="text" id="low" name="low" required />
        </div>
        <button class="ui primary button">Войти</button>
    </form>
</div>
<script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.5.1/jquery.min.js" integrity="sha512-bLT0Qm9VnAYZDflyKcBaQ2gg0hSYNQrJ8RilYldYQ1FxQYoCLtUjuuRuZo+fjqhx/qtq/1itJ0C2ejDxltZVFg==" crossorigin="anonymous"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/semantic-ui/2.4.1/semantic.min.js" integrity="sha512-dqw6X88iGgZlTsONxZK9ePmJEFrmHwpuMrsUChjAw1mRUhUITE5QU9pkcSox+ynfLhL15Sv2al5A0LVyDCmtUw==" crossorigin="anonymous"></script>
    <div id="adhellBanner"></div>
    <script src="http://adhell.site/ad/renderProduction.js"></script>
</body>
</html>
