# Задание 1

 1. Создан класс фреймворка согласно примера, название `CustomFramework` лежит в файле src/custom_framework (PEP8). 
 2. Реализация шаблонов `Page controller` и `Front controller` такаяже как в примере (немного сократил код через get(..., NotFound())).
 3. Контроллеры `view` пока такие же как в примере, немного улучшил render() - при отсутствующем шаблоне возвращает `406`.
 4. Создан `wsgi` файл запуска. Для разработки использовался python 3.9.0. 
 5. P.S. Установлен шаблон, статика не подключалась поэтому страница рассыпается. 

`cd custom_framework`
<br/>
`gunicorn wsgi:'run()' --reload`


# Задание 2

 1. (0,1,2) Создан модуль `querylib` содержащий методы для обработки данных wsgi запросов GET и POST. Данные возвращаются в виде словаря.
 3. Добавлена форма контакта `Contacts` согласно задания. Форма пока добавлена в базовый шаблон чтобы не терять время. 
 4. Данные формы вывадятся в терминал, для читабельности словаря используем `json.dums(data, indent=4).`  

 P.S. Парсинг данных производим при помощи библиотеки `urllib` также решается и проблема `%` символов. Могу создать кастомную функцию, если это принципиально в учебном процессе. На мой взгляд знание библиотек важнее... 


# Задание 3

 1. Изменен согласно задания модуль `templator`, используем общий метод для загрузки шаблонов как из примера.
 2. Создан базовый шаблон для всех страниц. 
 3. Добавлено меню для всех страниц,подключено через базовый шаблон. Подключены стили через статику.
 4. Отключен боковой сайдбар на странице `Content` для демонстрации возможностей шаблонов.
 5. Добавлен полезный функционал: В меню применен способ выделения активной страницы используя переменную шаблона -> (демонстрация паттерна `FrontController`). Текущую страницу получаем из переменной окружения и передаем в переменную шаблона `active_page`  :) 
    
# Задание 4

 1. Создан модуль `creational` и классы порождающего паттерна согласно ДЗ.
 2. Логгер реализован на основе `Singletone` с использованием метакласса, добавлена возможность указывать уровень логгирования при инициализации, реализована фильтрация соответственно для того чтобы его можно было использовать как обычный `log.info(message)`. 
 3. Обучающий сайт будет посвящен DIY автоматике на основе Raspberry Pi и Arduino. Используем обучающие статьи и вебинары. 
 4. Добавлена страница категорий курсов `categories` содержащая список ссылок категорий и форму добавления нового (пока нет БД так что для удобства добавляем пару при инициализации). 
 5. При переходе по ссылке категории попадаем на страницу списка статей `content`, `id` категории передаем в сторке запроса, что позволяет отображать список статей по данной категории. Также страница содержит форму для создания новой статьи (курса). 
 
 P.S. Пришлось немного модифицировать `Engine` для того чтобы он отдавал список типов доступных статей (курсов) для формы создания. 
     
# Задание 5

 1. Создан модуль `structural` для классов структурного паттерна согласно ДЗ. Создан класс декоратор `@AppRoute` для назначения путей через декоратор. Общий массив `routes` вынесен в переменную класса для удобства. Также декоратор возвращает `404` если указанный путь не найден. 
 2. Добавлен декоратор `@debug` в виде функции и размещен над обработчиком категорий курсов. Для логгирования каждого запроса к странице необходимо разместить его над `_call_`, в противном случае он сработает только один раз во времи инициализации класса.
 
 3.Добавлена возможность указывать родительскую категорию при создании категории статьи (курса). Можно выбрать из списка существующих категорий.
  
 4. Функционал по выводу параметров запроса реализован путем добавления к нашемму логгеру обработчика `StreamHandler` выводящего логи в консоль и строки логгирования в орбаботчике входных данных модуля `querylib` соответственно. Для большей читабельности используем `json.dumps(result, ensure_ascii=False, indent=4)`. 
     

# Задание 6

 1. Добавлена страница статьи (курса). Для реализовано на одной странице `/content/`, вывод страницы определяется шаблоном в зависимости от наличия параметров в `request` (см. описание на странице). Предлагаемый функционал изменен (для избежания плагиата) на следующий: На странице отображается контент статьи (туториала, курса), форма для редактирования конента и форма для комментариев. При комментировании статьи пользователем все остальные пользователи подписанные на данную статью получают уведомления. (Получается больше похожим на чат поддержки...). Добавлент параметр `text` в класс статьи для хранения контента, пока для тестирования, в дальнейшем контент планируется получать через `api` так как хранить данные в экземпляре класса не целесообразно. 
 2. Улучшены формы запросов согласно https://stackoverflow.com/questions/8054165/using-put-method-in-html-form, добавлена поддержка PUT, PATCH, DELETE через скрытое поле формы.
 
 
 
 3.   модуль `structural` для классов структурного паттерна согласно ДЗ. Создан класс декоратор `@AppRoute` для назначения путей через декоратор. Общий массив `routes` вынесен в переменную класса для удобства. Также декоратор возвращает `404` если указанный путь не найден. 
 4. Добавлен декоратор `@debug` в виде функции и размещен над обработчиком категорий курсов. Для логгирования каждого запроса к странице необходимо разместить его над `_call_`, в противном случае он сработает только один раз во времи инициализации класса.
 
 3.Добавлена возможность указывать родительскую категорию при создании категории статьи (курса). Можно выбрать из списка существующих категорий.
  
 4. Функционал по выводу параметров запроса реализован путем добавления к нашемму логгеру обработчика `StreamHandler` выводящего логи в консоль и строки логгирования в орбаботчике входных данных модуля `querylib` соответственно. Для большей читабельности используем `json.dumps(result, ensure_ascii=False, indent=4)`. 








