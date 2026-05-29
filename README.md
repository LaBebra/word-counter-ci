# Word Counter

Python-скрипт, який зчитує вміст `.txt` файлу, знаходить **10 найпопулярніших слів** та записує результат у новий файл у форматі `слово-кількість`.

## Структура проєкту

```
word_counter/
├── word_counter.py          # Основний модуль
├── test_word_counter.py     # Unit-тести (pytest)
├── sample_input.txt         # Приклад вхідного файлу
├── requirements.txt         # Залежності проєкту
├── pytest.ini               # Конфігурація pytest
├── .gitignore
└── .github/
    └── workflows/
        └── ci.yml           # GitHub Actions CI
```

## Встановлення

```bash
pip install -r requirements.txt
```

## Використання

```bash
python word_counter.py sample_input.txt output.txt
```

Результат у `output.txt`:

```
the-12
fox-7
dog-6
quick-4
...
```

## Запуск тестів

```bash
pytest
```

Звіт буде збережено у файл `report.html`.

## CI/CD

GitHub Actions автоматично:
- перевіряє код на відповідність **PEP8** (flake8)
- запускає всі **unit-тести** (pytest)
- зберігає **HTML-звіт** як артефакт
