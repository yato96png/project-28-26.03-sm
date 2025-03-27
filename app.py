from flask import Flask, render_template, request, redirect, url_for, send_from_directory, flash
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.secret_key = 'supersecretkey' 

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

@app.route('/')
def index():
    files = []
    for filename in os.listdir(app.config['UPLOAD_FOLDER']):
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        if os.path.isfile(filepath):
            files.append({
                'name': filename,
                'size': os.path.getsize(filepath) // 1024 
            })
    return render_template('index.html', files=files)

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('Нет файла в запросе')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('Файл не выбран')
            return redirect(request.url)
        if file:
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)
            flash(f'Файл "{file.filename}" успешно загружен')
            return redirect(url_for('index'))
    return render_template('upload.html')

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

@app.route('/delete/<filename>')
def delete_file(filename):
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if os.path.exists(filepath):
        os.remove(filepath)
        flash(f'Файл "{filename}" удален')
    else:
        flash(f'Файл "{filename}" не найден')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
