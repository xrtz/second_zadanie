# Задание №2 Индивидуальный вариант №18
Михеев А.С. 18 вариант
# Постановка задачи
Разработать инструмент командной строки для визуализации графа 
зависимостей, включая транзитивные зависимости. Сторонние средства для 
получения зависимостей использовать нельзя. Зависимости определяются для git-репозитория. Для описания графа 
зависимостей используется представление Graphviz. Визуализатор должен 
выводить результат на экран в виде графического изображения графа. 
Построить граф зависимостей для коммитов, в узлах которого содержатся 
номера коммитов в хронологическом порядке. Граф необходимо строить только 
для тех коммитов, где фигурирует файл с заданным именем. 

Конфигурационный файл имеет формат yaml и содержит: 

• Путь к программе для визуализации графов. 
• Путь к анализируемому репозиторию. 
• Файл с заданным именем в репозитории.

# Описание функций

load_config(config_file) - Загружает конфигурацию из YAML-файла. Открывает файл, считывает его содержимое и возвращает данные в виде словаря.

get_commits_and_metadata(repo_path, file_name) - Получает информацию о коммитах для указанного файла в Git-репозитории. Выполняет команду git log, чтобы собрать хэши коммитов, родительские коммиты и даты. Возвращает список, где каждый элемент содержит хэш коммита, его родителей и дату.

build_dependency_graph(commit_metadata) - Строит граф зависимостей коммитов с использованием Graphviz. Создает узлы для коммитов с сокращенным хэшем и датой, а также добавляет ребра между коммитами и их родителями.

show_graph(graph) - Генерирует изображение графа в формате PNG и открывает его с помощью библиотеки PIL для отображения на экране.

main() - Читает аргумент с путем к конфигурационному файлу, загружает конфигурацию, извлекает данные о коммитах и строит граф зависимостей, который затем отображается.

# Запуск программы 
python visualizer.py config.yaml

# Тесты 
Граф с датой под названием коммита 
![image](https://github.com/user-attachments/assets/9421436f-90af-4360-8824-845a816cb1bc) 


Граф

![image](https://github.com/user-attachments/assets/645220e0-c95a-4f51-9e58-7564298d8142)





