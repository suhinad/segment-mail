from flask import Flask, render_template, request, send_file
from segment import dict_segmentation
from main import segmentemail
import os

app = Flask(__name__)

# Словник з даними
items_dict = dict_segmentation()


# Головна сторінка з формою
@app.route('/')
def index():
    return render_template('index.html', items=items_dict)


# Обробник форми після вибору опції
@app.route('/submit', methods=['POST'])
def submit():
    selected_key = request.form.get('item')  # Отримуємо вибраний ключ зі списку
    selected_value = items_dict[int(selected_key)]  # Отримуємо значення за ключем

    file_path = segmentemail(selected_key, selected_value)

    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)

    return "Файл не знайдено або виникла помилка при його створенні."


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')
