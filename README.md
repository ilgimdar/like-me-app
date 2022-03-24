# like-me-app
Backend for Badoo-like web/mobile application made with django and DRF

Проект размещен по адресу:

https://likester.herokuapp.com

Доступлные API запросы (я тестировал в Postman):

1) GET https://likester.herokuapp.com/api/list (возвращает список всех участников) Есть фильтры gender=Male / gender=Female а также фильтр name=...

Примеры запросов: 
 GET https://likester.herokuapp.com/api/list?name=Ildar&gender=Male
 
 GET https://likester.herokuapp.com/api/list
 
2) GET https://likester.herokuapp.com/api/distance?id1=<x>&id2=<y> (при указании корректных id1 пользователя и id2 другого пользователя возаращает расстояние между ними)
  
Пример запроса:
GET https://likester.herokuapp.com/api/distance?id1=1&id2=2 
  
3) POST https://likester.herokuapp.com/api/clients/create

(form-data)

-username (уникальный) 
-email
-name
-password
-image (прикрепить файл)
-gender (Male или Female)
-location (2 числа типа float через проблем) Пример: 55.7887 49.1221

Сервер вернет сообщение: "User username registration successful", а в папку media попадет картинка с водяным знаком APPTRIX.

4) GET https://likester.herokuapp.com/api/clients/match?from_id=<x>&to_id=<y>

Запрос отправляет симпатию от пользователя с id=from_id пользователю с id=to_id. 
Если происходит match, но на email обоих придет сообщение об этом.

Пример запроса:

GET https://likester.herokuapp.com/api/clients/match?from_id=3&to_id=2
