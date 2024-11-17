from flask import Flask, request, send_from_directory, redirect, url_for, flash
import os

app = Flask(__name__)
# 移除了 app.secret_key

# 设置文件存储的目录为特定的路径
UPLOAD_FOLDER = 'C:/huancun'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# 确保上传文件夹存在
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def index():
    return '''
    <!doctype html>
    <html>
    <head>
        <title>超简易网盘</title>
    </head>
    <body>
        <h1>超简易网盘</h1>
        <p><a href="/upload">上传文件</a></p>
        <p><a href="/files">下载文件</a></p>
    </body>
    </html>
    '''

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('没有选择文件')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('没有选择文件')
            return redirect(request.url)
        if file:
            filename = file.filename
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            flash('文件上传成功')
            return redirect(url_for('list_files'))
    return '''
    <!doctype html>
    <html>
    <head>
        <title>上传新文件</title>
    </head>
    <body>
        <h1>上传新文件</h1>
        <form method=post enctype=multipart/form-data>
          <input type=file name=file>
          <input type=submit value=上传>
        </form>
    </body>
    </html>
    '''

@app.route('/files')
def list_files():
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    return '<h1>文件列表：</h1>' + ''.join(f'''
    <form method="POST" action="/delete/{file}" style="display: inline;">
        <input type="hidden" name="filename" value="{file}">
        <p>
            <a href="/files/{file}">{file}</a> | 
            <button type="submit">删除</button>
        </p>
    </form>
    ''' for file in files)

@app.route('/files/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/delete/<filename>', methods=['POST'])
def delete_file(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if os.path.exists(file_path):
        os.remove(file_path)
        flash('文件删除成功')
    else:
        flash('文件不存在')
    return redirect(url_for('list_files'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=30774, debug=True)