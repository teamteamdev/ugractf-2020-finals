<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8" />
    <title>ОФЦ ——— ГЛАВНАЯ</title>
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
            <p style="float: right;">
                ЕНЮМ <strong>${profile.enum}</strong><br/>
                Кодовое слово <strong style="background: black;">${profile.codeword}</strong>
            </p>
            <img src="/static/oi_docs.svg" style="width: 65%; max-height: 200px;" />
        </div>
        <div class="ui container">
            <h1>Здравствуйте! Ваши услуги:</h1>
            <a href="/service" class="ui card">
                <div class="content">
                    <div class="header">Получение пособия</div>
                    <div class="meta">ОФЦ</div>
                    <div class="description">
                        В сентябре правительство выплатит всем гражданам от 21 года по 25 000 рублей....
                    </div>
                </div>
                <div class="extra content">
                    <button class="ui basic green button" href="/service">Получить на карту</button>
                </div>
            </a>

            <div class="ui divider"></div>

            <#if actualCertificate??>
                <p>У вас есть актуальный сертификат:</p>
                <pre>${actualCertificate.serialize()}</pre>
            <#else>
                <p>У вас нет сертификата! Выпустите его, чтобы войти заново:</p>
            </#if>
            <h2>Выпустить новый сертификат</h2>
            <p><a href="/securePkiPage" class="ui button teal">Выпустить</a></p>
        </div>
    </div>
</div>
<script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.5.1/jquery.min.js" integrity="sha512-bLT0Qm9VnAYZDflyKcBaQ2gg0hSYNQrJ8RilYldYQ1FxQYoCLtUjuuRuZo+fjqhx/qtq/1itJ0C2ejDxltZVFg==" crossorigin="anonymous"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/semantic-ui/2.4.1/semantic.min.js" integrity="sha512-dqw6X88iGgZlTsONxZK9ePmJEFrmHwpuMrsUChjAw1mRUhUITE5QU9pkcSox+ynfLhL15Sv2al5A0LVyDCmtUw==" crossorigin="anonymous"></script>
    <div id="adhellBanner"></div>
    <script src="http://adhell.site/ad/renderProduction.js"></script>
</body>
</html>
