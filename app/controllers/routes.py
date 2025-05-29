from flask import Blueprint, render_template, request, redirect, session, url_for
from app.models.user_model import UserModel
from app.models.article_model import ArticleModel
from app.models.comment_model import CommentModel

routes_blueprint = Blueprint('routes', __name__)

@routes_blueprint.route('/')
def index():
    article_model = ArticleModel()
    articles = article_model.get_all_articles()
    article_model.close()
    return render_template('index.html', articles=articles)


@routes_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user_model = UserModel()
        user = user_model.get_user_by_username(username)

        if user and user['password'] == password:
            session['user'] = {
                'id': user['id'],
                'username': user['username']
            }
            user_model.close()
            return redirect(url_for('routes.index'))
        else:
            error = "Username atau password salah"
            user_model.close()

    return render_template('login.html', error=error)


@routes_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user_model = UserModel()
        existing_user = user_model.get_user_by_username(username)

        if existing_user:
            error = "Username telah digunakan"
        else:
            user_model.insert_user(username, password)
            user_model.close()
            return redirect(url_for('routes.login'))

        user_model.close()

    return render_template('register.html', error=error)

@routes_blueprint.route('/change_password', methods=['GET', 'POST'])
def change_password():
    if 'user' not in session:
        return redirect(url_for('routes.login'))

    error = None
    success = None
    if request.method == 'POST':
        current = request.form['current_password']
        new = request.form['new_password']

        user_model = UserModel()
        user = user_model.get_user_by_username(session['user']['username'])

        if user['password'] != current:
            error = "Password lama salah"
        else:
            user_model.update_password(user['id'], new)
            success = "Password berhasil diubah"

        user_model.close()

    return render_template('change_password.html', error=error, success=success)

@routes_blueprint.route('/article_list')
def article_list():
    article_model = ArticleModel()
    articles = article_model.get_all_articles()
    article_model.close()
    return render_template('article_list.html', articles=articles)


@routes_blueprint.route('/add_article', methods=['GET', 'POST'])
def add_article():
    if request.method == 'POST':
        title = request.form['title']
        subject = request.form['subject']
        content = request.form['content']
        author_id = session['user']['id']
        article = ArticleModel()
        article.insert_article(title, content, subject, author_id)
        return redirect(url_for('routes.article_list'))

    return render_template('article_form.html')


@routes_blueprint.route('/article/<int:article_id>/edit', methods=['GET', 'POST'])
def edit_article(article_id):
    if 'user' not in session:
        return redirect(url_for('routes.login'))

    article_model = ArticleModel()
    article = article_model.get_article_by_id(article_id)

    if not article:
        article_model.close()
        return "Artikel tidak ditemukan", 404

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        subject = request.form['subject']

        article_model.update_article(article_id, title, content, subject)
        article_model.close()
        return redirect(url_for('routes.article_detail', article_id=article_id))

    article_model.close()
    return render_template('edit_article.html', article=article)

@routes_blueprint.route('/comment/<int:comment_id>/edit', methods=['GET', 'POST'])
def edit_comment(comment_id):
    if 'user' not in session:
        return redirect(url_for('routes.login'))

    comment_model = CommentModel()
    comment = comment_model.get_by_id(comment_id)

    if not comment or comment['user_id'] != session['user']['id']:
        comment_model.close()
        return "Komentar tidak ditemukan atau Anda tidak memiliki izin untuk mengedit", 403

    if request.method == 'POST':
        new_text = request.form['comment_text']
        comment_model.update_comment(comment_id, new_text)
        comment_model.close()
        return redirect(url_for('routes.article_detail', article_id=comment['article_id']))

    comment_model.close()
    return render_template('edit_comment.html', comment=comment)

@routes_blueprint.route('/article/<int:article_id>', methods=['GET', 'POST'])
def article_detail(article_id):
    article_model = ArticleModel()
    comment_model = CommentModel()
    
    article = article_model.get_article_by_id(article_id)
    if not article:
        article_model.close()
        comment_model.close()
        return "Artikel tidak ditemukan", 404

    if request.method == 'POST' and session.get('user'):
        comment_text = request.form['comment_text']
        user_id = session['user']['id']
        comment_model.insert_comment(article_id, user_id, comment_text)
        return redirect(url_for('routes.article_detail', article_id=article_id))

    comments = comment_model.get_comments_by_article(article_id)
    
    article_model.close()
    comment_model.close()
    
    return render_template('article_detail.html', article=article, comments=comments)

@routes_blueprint.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('routes.index'))