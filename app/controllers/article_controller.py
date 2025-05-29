from flask import Blueprint, render_template, request, redirect, url_for, flash, session, abort
from app.models.article_model import ArticleModel
from app.models.comment_model import CommentModel
from functools import wraps

article = Blueprint('article', __name__)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

@article.route('/article/new', methods=['GET', 'POST'])
@login_required
def create_article():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        subject = request.form.get('subject')
        
        if not title or not content or not subject:
            flash('Please fill all fields', 'error')
            return redirect(url_for('article.create_article'))
        
        article_model = ArticleModel()
        try:
            article_model.insert_article(title, content, subject, session['user_id'])
            article_model.close()
            flash('Article created successfully!', 'success')
            return redirect(url_for('routes.index'))
        except Exception as e:
            article_model.close()
            flash('Error creating article', 'error')
            return redirect(url_for('article.create_article'))
    
    return render_template('article/create.html')

@article.route('/article/<int:id>')
def view_article(id):
    article_model = ArticleModel()
    comment_model = CommentModel()
    
    article = article_model.get_article_by_id(id)
    if not article:
        article_model.close()
        comment_model.close()
        abort(404)
    
    comments = comment_model.get_comments_by_article(id)
    article_model.close()
    comment_model.close()
    
    return render_template('article/view.html', article=article, comments=comments)

@article.route('/article/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_article(id):
    article_model = ArticleModel()
    article = article_model.get_article_by_id(id)
    
    if not article:
        article_model.close()
        abort(404)
    
    if article['author_id'] != session['user_id'] and session.get('role') != 'admin':
        article_model.close()
        abort(403)
    
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        subject = request.form.get('subject')
        
        if not title or not content or not subject:
            flash('Please fill all fields', 'error')
            return redirect(url_for('article.edit_article', id=id))
        
        try:
            article_model.update_article(id, title, content, subject)
            article_model.close()
            flash('Article updated successfully!', 'success')
            return redirect(url_for('article.view_article', id=id))
        except:
            article_model.close()
            flash('Error updating article', 'error')
            return redirect(url_for('article.edit_article', id=id))
    
    article_model.close()
    return render_template('article/edit.html', article=article)

@article.route('/article/<int:article_id>/comment', methods=['POST'])
@login_required
def add_comment(article_id):
    comment_text = request.form.get('comment_text')
    
    if not comment_text:
        flash('Comment cannot be empty', 'error')
        return redirect(url_for('article.view_article', id=article_id))
    
    comment_model = CommentModel()
    try:
        comment_model.insert_comment(article_id, session['user_id'], comment_text)
        comment_model.close()
        flash('Comment added successfully!', 'success')
    except:
        comment_model.close()
        flash('Error adding comment', 'error')
    
    return redirect(url_for('article.view_article', id=article_id)) 