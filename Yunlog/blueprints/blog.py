from flask import render_template,Blueprint,request,current_app,redirect,url_for
from Yunlog.models import Post, Category, Comment
from Yunlog.forms import CommentForm, AdminCommentForm
from Yunlog.extensions import db

blog_bp = Blueprint('blog', __name__)

@blog_bp.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['BLUELOG_POST_PER_PAGE']
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(page, per_page=per_page)
    posts = pagination.items
    return render_template('blog/index.html', pagination=pagination, posts=posts)

@blog_bp.route('/about')
def about():
    return render_template('blog/about.html')

@blog_bp.route('/post/<int:post_id>', methods=['GET', 'POST'])
def show_post(post_id):
    post = Post.query.get_or_404(post_id)
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['BLUELOG_COMMENT_PER_PAGE']
    pagination = Comment.query.with_parent(post).filter_by(reviewed=True).order_by(Comment.timestamp.asc()).paginate(
        page, per_page)
    comments = pagination.items


    form = CommentForm()
    from_admin = False
    reviewed = True

    if form.validate_on_submit():
        author = form.author.data
        email = form.email.data
        site = form.site.data
        body = form.body.data
        comment = Comment(
            author=author, email=email, site=site, body=body,
            from_admin=from_admin, post=post, reviewed=reviewed)
        replied_id = request.args.get('reply')
        if replied_id:
            print(replied_id)
            replied_comment = Comment.query.get_or_404(replied_id)
            print(replied_comment.author)
            print(replied_comment)
            comment.replied = replied_comment
        db.session.add(comment)
        db.session.commit()
        print('save ok')
        return redirect(url_for('.show_post', post_id=post_id))
    return render_template('blog/post.html', post=post, pagination=pagination, form=form, comments=comments)

@blog_bp.route('/category/<int:category_id>')
def show_category(category_id):
    category = Category.query.get_or_404(category_id)
    page = request.args.get('page',1,type=int)
    per_page = current_app.config['BLUELOG_COMMENT_PER_PAGE']
    pagination = Post.query.with_parent(category).order_by(Post.timestamp.asc()).paginate(
        page, per_page)
    posts = pagination.items
    return render_template('blog/category.html',category=category,pagination=pagination,posts=posts)

@blog_bp.route('/reply/comment/<int:comment_id>')
def reply_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    return redirect(
        url_for('.show_post', post_id=comment.post_id, reply=comment_id, author=comment.author) + '#comment-form')