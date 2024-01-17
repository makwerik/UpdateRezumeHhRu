<h1>Api для поднятия резюме в поиске на hh.ru</h1>
<h2>Использование: </h2>

- <code>pip install -r req.txt</code><br>
- Переходим внутрь файла generalapi.py<br>
- Указываем client_id, client_secret, code<br>
- Вызываем метод ``get_token()``<br>
- Создаётся файл token.json<br>
- Теперь не нужно указывать client_id, client_secret, code<br>
- Указываем id резюме и вызывааем ``update_rezume()``<br>
- Воуля, резюме поднялось в поиске

<h2>Чтобы работало всё автоматически после выше сделанного:</h2>

- ``python logic.py`` предварительно указав внутри скрипта id своего резюме

<h3>P.s. У меня не было 14 свободных дней, чтобы протестировать метод ``refresh_token()``.
Но он должен работать после запуска ``logic.py`` так: Если получаем ошибку 403 - токен просрочен, то запускается метод 
рефреша, перезаписывает новые токены и снова в цикле запускается ``update_rezume()``, тем самым
уже считывая новые токены из файла ``token.json`` и дальше продолжает поднимать наше резюме</h3>