from flask import Flask, request, send_from_directory, render_template, redirect, url_for, flash
import os

app = Flask(__name__)
app.secret_key = 'super_secret_key'
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# 简单的内存数据库
file_database = {}

@app.route('/')
def index():
    files = os.listdir(UPLOAD_FOLDER)
    # 仅显示在数据库中有记录的文件
    valid_files = [f for f in files if f in file_database]
    # 修改点：这里改为 render_template 引用 index.html
    return render_template('index.html', files=valid_files)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    
    file = request.files['file']
    invite_code = request.form.get('invite_code')

    if file.filename == '':
        return redirect(request.url)

    if file and invite_code:
        file.save(os.path.join(UPLOAD_FOLDER, file.filename))
        file_database[file.filename] = invite_code
        return redirect(url_for('index'))
    
    return redirect(url_for('index'))

@app.route('/access/<filename>', methods=['GET', 'POST'])
def access_file(filename):
    if filename not in file_database or not os.path.exists(os.path.join(UPLOAD_FOLDER, filename)):
        return redirect(url_for('index'))

    if request.method == 'POST':
        user_input_code = request.form.get('code')
        correct_code = file_database.get(filename)

        if user_input_code == correct_code:
            return send_from_directory(UPLOAD_FOLDER, filename, as_attachment=True)
        else:
            # 修改点：这里改为 render_template 引用 verify.html
            return render_template('verify.html', filename=filename, error="提取码错误，请重试")

    # 修改点：这里改为 render_template 引用 verify.html
    return render_template('verify.html', filename=filename, error="")

if __name__ == '__main__':
    app.run(debug=True, port=5000)
