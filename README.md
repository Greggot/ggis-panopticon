# ГГИС Паноптикум
Скрипты для упрощения жизни при работе с Kaiten, Gitlab и пр.

## Cодержание  

- [Установка зависимостей](#установка-зависимостей)  
- [Использование skird.py](#использование-skirdpy)
- [Использование skird_cmd.py](#использование-skird_cmdpy)
- [Использование task_manager.py](#использование-task_managerpy)
   - [Изменение конфигурации](#изменение-конфигурации)  
- [Использование time_management.py](#использование-time_managementpy)  
- [Пожелания и предложения](#пожелания-и-предложения)

## Установка зависимостей 

Python3 предуставновлен на Ubuntu, но если что
```bash
sudo apt-get update
sudo apt-get install python3.6 python3-pip
```

Для корректной работы приложения необходимо удовлетворить зависимости проекта. Для этого вызовите следующую команду
```bash
pip3 install -r requirements.txt
```

## Использование skird.py

Скрипт создает и оформляет карточки по корпоративному стандарту
 
1. Поместить номера сторей в текстовый файл `data/tasks.txt` (или поменяйте путь в скрипте). 
На каждой новой строчке - через `Tab` описание того, что вы нужно сделать

```txt
42.0
   Страдать фигней
   Рефакторинг
   Связь с front-end
```

2. Добавить файл `env/env.json`

```json
{
 "kaiten_host": "https://kaiten.iccdev.ru", 
 "kaiten_token": "ваш-токен"
}
```

3. Запустить скрипт: 

```bash
python3 skird.py
```

4. ??????
5. Profit. Ваши задачи конвертируются в задачи delivery в бэклоге спринта с нужными:
   - названием (включает id карточки as well)
   - меткой "ГГИС"
   - типом
   - пользователем(вы) в роли "ответственного"
   - Ролью C++

## Использование skird_cmd.py
Новый `skird_cmd.py` аналогичен `skird.py`, но имеет интерфейс командной строки и подразумеваеет использование без
правки исходного кода. Результат вызова `skird_cmd.py` без аргументов аналогичен вызову `skird.py`. Для получения
справки вызовите:
```bash
./skird_cmd.py -h
```

Помимо этого `skird_cmd.py` может работать со списком задач в виде json- или yaml- документа (формат определяется
автоматически при расширении файла *.json или *.yaml):
```bash
./skird_cmd.py -p "data/tasks.json"
./skird_cmd.py -p "data/tasks.yaml"
```
Формат входного json-файла следующий (для понимания поля `"config"` изучите [соответствующее примечание](#изменение-конфигурации)):
~~~json5
{
  "BUG": {
    "81.23465": [
      {
        "config": "delivery", //можно опустить, используется "delivery" по-умолчанию
        "name": "Починить всё это",
        "size": 16 //(время в часах) можно опустить, используется занчение из выбранной конфигурации
      }
    ]
  },
  "US-EN": {
    "49.9": [
      {
        "config": "delivery",
        "name": "Что-то там интересное делать",
      }
    ],
    "94.3": [
      {
        "config": "discovery",
        "name": "Декомпозиция задач по адаптации алгоритмов буфера обмена и сессий",
        "size": 4
      },
      {
        "config": "delivery",
        "name": "Реализация всего этого",
        "size": 16
      }
    ]
  }, 
  "ALL": {
     "46324": [
        {
           "config": "delivery", 
           "name": "Что-то там интересное делать",
        }
     ]
  }
}
~~~
Вместо идентификаторов карточек `"94.3"`/`"49.9"` можно использовать полное ID карточки - `"45906"`.\
Поле `"ALL"` служит для поиска карточки среди всех типов и отлично подходит, если Вы указываете именно ID карточки, а
не ее идентификатор.

А это пример конфигурации yaml-файла:
~~~yaml
- type: BUG
  ggis_id: 114.47811
  tasks:
   - config: delivery
     name: "Удали меня 1"
     size: 8
   - config: discovery
     name: "Удали меня 2"
     size: 8
- id: 45906
  tasks:
    - config: delivery
      name: "Удали меня 3"
      size: 16
~~~
Здесь `type` может принимать значение типа родительской карточки по аналогии с форматом json. Помимо этого данное поле
может отсутствовать, что эквивалентно значению `"ALL"`.\
Поле `ggis_id` - идентификатор в проекте (`"94.3"`/`"49.9"`). Может быть не задан, если присутствует поле `id`,
по которому строго будет искаться карточка.\
Поле `tasks` эквивалентно задачам из json-формата. 

## Работа с текстовым интерактивным интерфейсом

Скрипт `./skird_cmd.py` позволяет работать через интерактивный интерфейс. Для этого необходимо передать аргумент `--tui` при вызове скрипта 

## Использование task_manager.py
Скрипт `task_manager.py` призван помочь создать список задач в виде json-формата в автоматическом режиме. Выполните
и следуйте вопросам из консоли:
```bash
./task_manager.py
```

Результом исполнения скрипта можно считать файл `data/tasks.json`, который позже можно поправить вручную или же перед
непосредственным ответом на вопрос скрипта _"Запустить скрипт создания новых карточек с Вашей конфигурацией?"_.

### Изменение конфигурации

Поскольку теперь нам нужно заводить карточки разных типов, были добавлены конфигурационные файлы следующей структуры:

```json
{
    "board_id": 192,
    "column_id": 776,
    "lane_id": 1275,
    "size_text": "16 ч",
    "type_id": 6,
    
    "properties": { 
        "id_19": "1"
    }
}
```

`board_id` - ID доски, на которой нужно создать карточку  
`column_id` - ID колонки  
`lane_id` - Даже не спрашивайте - не помню  
`size_text` - Длительность с единицами измерения  
`type_id` - Тип карточки, очередное магическое число. 11 - Delivery, 6 - Discovery.  
`properties.id_19` - Роль. "1" - С++. Остальные не знаю, реверсите через запросы сами.  

Файл с конфигурацией должен находиться в `env/skird_config/`.  
**Чтобы поменять конфиг**, замените значение переменной в `skird.py` на имя вашей конфигурации:
```python
   config_name = 'delivery'
```

## Использование time_management.py

Скрипт автоматически списывает одинаковое время в административную карточку в течение указанного времени

1. Заполнить под свою карточку файл с настройками `env/auto_time_log.json`

```json
{
    "start_date": "2024-04-01",
    "days_count": 3,
    "time_spent": 20,
    "role_id": 3,
    "card_id": 24411
}
```
`start_date` - Дата начала списаний YYYY-MM-DD  
`days_count` - Количество дней в течение которых списывать, включая выходные.
В сами выходные время списано не будет, просто оффсет по дням так работает  
`time_spent` - Время списаний в минутах  
`role_id` - Идентификатор роли, 3 - разработчик, остальные потом пронумерую  
`card_id` - ID карточки, в которую списать время. В данном случае - это дейлики  

2. Запустить скрипт:

```bash
python3 time_management.py
```

3. Принять всю ответственность на себя и ввести любой бред, начинающийся на `y` или `Y`.

4. ????????

5. Profit

## Пожелания и предложения

Оформляйте пожелания в `Issues`, отправляйте предложения через `Pull requests`
