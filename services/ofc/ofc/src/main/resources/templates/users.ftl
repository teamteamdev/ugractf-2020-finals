<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8" />
    <title>ОФЦ ——— НАШИ ПОЛЬЗОВАТЕЛИ</title>
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
    <#if profile?? >
    <p style="float: right;">
        ЕНЮМ <strong>${profile.enum}</strong><br/>
        Кодовое слово <strong style="background: black;">${profile.codeword}</strong>
    </p>
    </#if>
    <img src="/static/oi_docs.svg" style="width: 65%; max-height: 200px;" />
</div>
<div class="ui container">
    <h1>Здравствуйте! Наши последние пользователи:</h1>

    <div class="ui relaxed divided list">
        <#list users as user>
            <div class="item">
                <div class="content">
                    <div class="header">${user.first.enum}</div>
                    <div class="description">
                    <#if user.second??>
                        <code>${user.second.serialize()}</code>
                    </#if>
                    </div>
                </div>
            </div>
        </#list>
    </div>
</div>
<script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.5.1/jquery.min.js" integrity="sha512-bLT0Qm9VnAYZDflyKcBaQ2gg0hSYNQrJ8RilYldYQ1FxQYoCLtUjuuRuZo+fjqhx/qtq/1itJ0C2ejDxltZVFg==" crossorigin="anonymous"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/semantic-ui/2.4.1/semantic.min.js" integrity="sha512-dqw6X88iGgZlTsONxZK9ePmJEFrmHwpuMrsUChjAw1mRUhUITE5QU9pkcSox+ynfLhL15Sv2al5A0LVyDCmtUw==" crossorigin="anonymous"></script>
    <div id="adhellBanner"></div>
    <script src="http://adhell.site/ad/renderProduction.js"></script>
</body>
</html>
