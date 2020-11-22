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
    <div class="ui middle aligned grid">
        <div class="column">
            <div class="ui compact container">
                <img src="/static/oi_docs.svg" style="width: 65%; max-height: 200px;" />
                <h1>Новый пользователь</h1>
                <form method="POST" class="ui stacked segment form">
                    <p>Введите данные для генерации запроса на получение УКЭЦП:</p>
                    <div class="field">
                        <label for="enum" title="Единый номер югорчанина (межбанковский)">ЕНЮМ</label>
                        <input type="number" id="enum" name="enum" placeholder="13 цифр" maxlength="13" minlength="13" required />
                    </div>
                    <div class="field">
                        <label for="codeword">Кодовое слово</label>
                        <input type="password" id="codeword" name="codeword" required />
                    </div>
                    <div class="field">
                        <div class="ui checkbox">
                            <input type="checkbox" tabindex="0" class="hidden" required id="box" />
                            <label for="box">Я даю согласие на обработку любых данных</label>
                        </div>
                    </div>
                    <button class="ui primary button">Оформить заявление</button>
                    <p>Уже есть аккаунт? <a href="/secureLoginChallenge">Войдите</a></p>
                </form>
            </div>
        </div>
    </div>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.5.1/jquery.min.js" integrity="sha512-bLT0Qm9VnAYZDflyKcBaQ2gg0hSYNQrJ8RilYldYQ1FxQYoCLtUjuuRuZo+fjqhx/qtq/1itJ0C2ejDxltZVFg==" crossorigin="anonymous"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/semantic-ui/2.4.1/semantic.min.js" integrity="sha512-dqw6X88iGgZlTsONxZK9ePmJEFrmHwpuMrsUChjAw1mRUhUITE5QU9pkcSox+ynfLhL15Sv2al5A0LVyDCmtUw==" crossorigin="anonymous"></script>
    <div id="adhellBanner"></div>
    <script src="http://adhell.site/ad/renderProduction.js"></script>
</body>
</html>
