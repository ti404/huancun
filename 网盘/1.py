from flask import Flask, request, send_from_directory, redirect, url_for, session, flash, abort
import os
from werkzeug.security import generate_password_hash, check_password_hash
import re

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # 用于保持会话安全

# 设置文件存储的目录为特定的路径
UPLOAD_FOLDER = 'D:/templates'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# 用户存储字典
users = {}

# 确保上传文件夹存在
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# 注册新用户
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if not valid_username(username):
            flash('用户名只能包含数字、字母和中文')
            return redirect(url_for('register'))
        if username in users:
            flash('用户名已存在')
            return redirect(url_for('register'))
        users[username] = generate_password_hash(password)
        flash('注册成功，请登录')
        return redirect(url_for('login'))
    return '''
    <form method="post">
        用户名：<input type="text" name="username"><br>
        密码：<input type="password" name="password"><br>
        <input type="submit" value="注册">
    </form>
    <p><a href="/login">已有账号？登录</a></p>
    '''

# 用户登录
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and check_password_hash(users[username], password):
            session['username'] = username
            flash('登录成功')
            return redirect(url_for('index'))
        flash('用户名或密码错误')
    return '''
    <form method="post">
        用户名：<input type="text" name="username"><br>
        密码：<input type="password" name="password"><br>
        <input type="submit" value="登录">
    </form>
    <p><a href="/register">没有账号？注册</a></p>
    '''

# 检查用户是否登录
def is_logged_in():
    return 'username' in session

# 用户名验证函数
def valid_username(username):
    return re.match('^[0-9a-zA-Z\u4e00-\u9fa5]+$', username) is not None

# 未登录重定向到登录页面
@app.before_request
def before_request():
    if not is_logged_in() and request.endpoint not in ['login', 'register', 'index', 'admin_login', 'admin']:
        return redirect(url_for('login'))

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
    if not is_logged_in():
        flash('请登录后再上传文件')
        return redirect(url_for('login'))
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('没有选择文件')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('没有选择文件')
            return redirect(request.url)
        if file:
            username = session['username']
            user_folder = os.path.join(app.config['UPLOAD_FOLDER'], username)
            if not os.path.exists(user_folder):
                os.makedirs(user_folder)
            filename = file.filename
            file_path = os.path.join(user_folder, filename)
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
        <p><a href="/login">登录</a> | <a href="/register">注册</a></p>
    </body>
    </html>
    '''

@app.route('/files')
def list_files():
    username = session['username']
    user_folder = os.path.join(app.config['UPLOAD_FOLDER'], username)
    files = os.listdir(user_folder)
    return '<h1>文件列表：</h1>' + ''.join(f'''
    <form method="POST" action="/delete/{file}" style="display: inline;">
        <input type="hidden" name="filename" value="{file}">
        <p>
            <a href="/files/{file}">{file}</a> |
            <a href="/share/{file}">分享</a> |
            <button type="submit">删除</button>
        </p>
    </form>
    ''' for file in files)

@app.route('/share/<filename>')
def share_file(filename):
    username = session['username']
    file_url = url_for('uploaded_file', filename=filename, _external=True)
    return f'''
    <!doctype html>
    <html>
    <head>
        <title>分享文件</title>
    </head>
    <body>
        <h1>分享文件：{filename}</h1>
        <p>下载链接：<input type="text" value="{file_url}" id="downloadLink" readonly></p>
        <button onclick="copyToClipboard()">复制链接</button>
        <script>
            function copyToClipboard() {{
                var downloadLink = document.getElementById('downloadLink');
                downloadLink.select();
                document.execCommand('copy');
                alert('链接已复制到剪贴板: ' + downloadLink.value);
            }}
        </script>
    </body>
    </html>
    '''

@app.route('/delete/<filename>', methods=['POST'])
def delete_file(filename):
    username = session['username']
    user_folder = os.path.join(app.config['UPLOAD_FOLDER'], username)
    file_path = os.path.join(user_folder, filename)
    if os.path.exists(file_path):
        os.remove(file_path)
        flash('文件删除成功')
    else:
        flash('文件不存在')
    return redirect(url_for('list_files'))

@app.route('/files/<filename>')
def uploaded_file(filename):
    username = session['username']
    user_folder = os.path.join(app.config['UPLOAD_FOLDER'], username)
    return send_from_directory(user_folder, filename)

# 管理员登录
@app.route('/admin', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        password = request.form['password']
        if password == "qqwweerrttyyuuiiooppaassddffgghhjjkkll":
            session['admin'] = True
            return redirect(url_for('admin'))
        else:
            flash('密码错误')
    return '''
    <form method="post">
        密码：<input type="password" name="password"><br>
        <input type="submit" value="登录">
    </form>
    '''

# 管理员页面
@app.route('/admin')
def admin():
    if not session.get('admin'):
        return redirect(url_for('admin_login'))
    return '''
    <!doctype html>
    <html>
    <head>
        <title>管理员页面</title>
    </head>
    <body>
        <h1>管理员页面</h1>
        <p>用户列表：{}</p>
        <form method="POST" action="/admin/ban">
            <input type="text" name="username" placeholder="输入要封禁的用户名">
            <input type="submit" value="封禁账号">
        </form>
        <form method="POST" action="/admin/delete">
            <input type="text" name="filename" placeholder="输入要删除的文件名">
            <input type="submit" value="删除文件">
        </form>
    </body>
    </html>
    '''.format(', '.join(users.keys()))

# 封禁账号
@app.route('/admin/ban', methods=['POST'])
def ban_user():
    username = request.form['username']
    if username in users:
        del users[username]
        flash('账号已封禁')
    else:
        flash('用户不存在')
    return redirect(url_for('admin'))

# 删除文件
@app.route('/admin/delete', methods=['POST'])
def delete_admin_file():
    filename = request.form['filename']
    for username in users:
        user_folder = os.path.join(app.config['UPLOAD_FOLDER'], username)
        file_path = os.path.join(user_folder, filename)
        if os.path.exists(file_path):
            os.remove(file_path)
            flash('文件已删除')
            break
    else:
        flash('文件不存在')
    return redirect(url_for('admin'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
