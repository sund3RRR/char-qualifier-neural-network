# Characater qualifier neural network

Проект представляет собой нейронную сеть, определяющую цифры и буквы русского алфавита по картинкам.
Нейросеть написана на `python`, в качестве бэкенда выступает `django`, визуализация - `html`, `js`, `css`.
## Клонирование репозитория
```
git clone https://github.com/kabachoke/char-qualifier-neural-network.git
cd char-qualifier-neural-network
```
## Настройка venv Linux
```
python -m venv venv
source ./venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

## Настройка venv Windows
```
python -m venv venv
venv\scripts\activate
python.exe -m pip install --upgrade pip
pip install -r requirements.txt
```

## Запуск сервера
`python char_qualifier_neural_network/manage.py runserver`

# Contributors
- Огромное спасибо <a href="https://github.com/TokArsi" target="_blank">Arsen</a> за реализацию визуальной части проекта на `html`, `css` и `js`