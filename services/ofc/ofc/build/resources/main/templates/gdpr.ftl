<#list users as user>${user.login}<#list user.rules as rule>
    ← ${rule.from}</#list>
</#list>
