from flask import Flask, render_template, url_for,request,redirect, flash,jsonify

from functions.create_tool_func import create_tool_template
from functions.utils import slugify
from tool import forex_sessions,pip_value_calc,timezone, economic_calendar,forex_corelation,risk_calc
from models import Tool, db, User, Post
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_migrate import Migrate
from decorators import role_required
from werkzeug.utils import secure_filename
import os
from flask_login import LoginManager, login_user, logout_user, current_user,login_required
from bs4 import BeautifulSoup


TOOL_DISPATCH = {
    "forex_sessions" : forex_sessions,
    "pip_value_calculator" : pip_value_calc,
    "timezone_converter" : timezone,
    "economic_calendar" : economic_calendar,
    "forex_co-relation" : forex_corelation,
    "risk_calculator" : risk_calc
}

app = Flask(__name__)
app.secret_key='steezy2025'

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#initialize db
db.init_app(app)

#create admin
admin = Admin(app, name='Site Admin', template_mode='bootstrap4')
admin.add_view(ModelView(Tool, db.session))

migrate = Migrate(app,db)

with app.app_context():
    
    db.create_all()

login_manager = LoginManager()
login_manager.login_view ='login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("login"))
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = User.query.filter_by(email=request.form["email"]).first()
        if user and user.check_password(request.form["password"]):
            login_user(user)
            if user.role=='writer':
                return redirect(url_for("writers_dashboard"))
            if user.role=='admin':
                return redirect(url_for("admin"))
            if user.role=='super_admin':
                return redirect(url_for("admin"))
            if user.role=='user':
                return redirect(url_for("user_dashboard"))
            
    return render_template("login.html")
@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')

@app.route("/education")
def education():
    return 'education page! learn here'

@app.route("/tools/<slug>", methods=['GET','POST'])
def render_tool(slug):
    tool =Tool.query.filter_by(slug=slug).first()
    context ={}
    if slug in TOOL_DISPATCH:
        context = TOOL_DISPATCH[slug](tool, request)
    if tool:
        
        return render_template(f"tools/{slug}.html", tool=tool, **context)
    else:
        return 'Tool not found', 404

@app.route("/tools")
def tools():
    all_tools = Tool.query.all()
    return render_template('tools.html', title='TOOLS', tools= all_tools)

@app.route("/blog")
def blog():
    all_posts = Post.query.all()
    for post in all_posts:
        soup = BeautifulSoup(post.content,'html.parser')
        first_img= soup.find('img')
        post.cover_img= first_img['src'] if first_img else None
        text = soup.get_text()
        post.excerpt = text[:150] +"..." if len(text) > 150 else text

    return render_template('blog.html', title='Blog', posts= all_posts)

@app.route("/blog/<slug>")
def view_post(slug):
    post = Post.query.filter_by(slug=slug).first_or_404()
    return render_template("view_post.html", post=post)

#Admin routes

@app.route("/admin")
@login_required
@role_required("admin","super_admin")
def admin():
    
    return render_template('admin/list.html')

@app.route("/admin/tools")
@login_required
@role_required("admin","super_admin")
def admin_tools():
    tools = Tool.query.all()
    return render_template('admin/tools.html', tools=tools)

@app.route("/admin/tools/add", methods=['GET','POST'])
@login_required
@role_required("admin","super_admin")
def add_tool():
    if request.method == 'POST':
        name= request.form['name']

        description = request.form['description']
        url =request.form['url']
        lucide_icon =request.form['lucide_icon']
        is_premium =request.form.get('is_premium') == 'on'
        slug = name.lower().replace(" ","_")
        if Tool.query.filter_by(slug=slug).first():
            flash("Tool with similar name exists.")
            return redirect('admin/add_tool.html')
        new_tool = Tool(name=name, slug=slug, description=description, url=url, lucide_icon=lucide_icon, is_premium=is_premium)
        db.session.add(new_tool)
        db.session.commit()

        create_tool_template(slug)
        return redirect(url_for('admin_tools'))
    return render_template('admin/add_tool.html', tools=tools)

@app.route("/admin/tools/edit/<int:id>", methods=['GET','POST'])
@login_required
@role_required("admin","super_admin")
def edit_tool(id):
    tool = Tool.query.get_or_404(id)
    if request.method == 'POST':
        tool.name= request.form['name']
        tool.description = request.form['description']
        tool.url =request.form['url']
        tool.lucide_icon =request.form['lucide_icon']
        tool.is_premium =request.form.get('is_premium') == 'on'
        
        db.session.commit()
        return redirect(url_for('admin_tools'))
    return render_template("admin/edit_tool.html", tool=tool)

@app.route("/admin/tools/delete/<int:id>", methods=['GET','POST'])
@login_required
@role_required("admin","super_admin")
def delete_tool(id):
    tool = Tool.query.get_or_404(id)
    db.session.delete(tool)
    db.session.commit()
    return redirect(url_for('admin_tools'))

@app.route("/admin/users")
@login_required
@role_required("admin","super_admin")
def users_page():
    all_users = User.query.all()
    return render_template('admin/users.html',users=all_users)

@app.route("/admin/users/add_user", methods=['GET','POST'])
@login_required
@role_required("admin","super_admin")
def add_user():
    if request.method == 'POST':
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        role = request.form["role"]
        user = User(username=username, email=email, role=role)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('users_page'))
    return render_template('admin/add_user.html')

@app.route("/admin/users/edit_user/<int:id>", methods=['GET','POST'])
@login_required
@role_required("admin","super_admin")
def edit_user(id):
    user = User.query.get_or_404(id)
    if request.method == 'POST':
        user.username = request.form["username"]
        user.email = request.form["email"]
        user.role = request.form["role"]
        db.session.commit()
        return redirect(url_for('users_page'))
    return render_template('admin/edit_user.html',user=user)

@app.route("/admin/users/delete/<int:id>", methods=['GET','POST'])
@login_required
@role_required("admin","super_admin")
def delete_user(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('users_page'))


#Writers dashboard

@app.route("/writer")
@login_required
@role_required("admin","super_admin","writer")
def writers_dashboard():
    return render_template('writer/writer.html')

@app.route("/writer/create_post", methods=['GET','POST'])
@login_required
@role_required("admin","super_admin","writer")
def create_post():
    if request.method == 'POST':
        title= request.form.get("title")
        content= request.form.get("content")
        slug = slugify(title)
        #ensure slug is unique
        existing = Post.query.filter_by(slug=slug).first()
        if existing:
            slug = f"{slug}-{Post.query.count() + 1}"
        new_post = Post(title=title, slug=slug, content=content, author_id=current_user.id)
        db.session.add(new_post)
        db.session.commit()
        flash("Post published!", "success")
        print(content)
        return redirect(url_for("writers_dashboard"))
        
    return render_template('/writer/create_post.html')

@app.route("/upload-image", methods=["POST"])
def upload_image():
    file = request.files.get("file")
    if file:
        filename = secure_filename(file.filename)
        upload_path = os.path.join("static", "uploads", filename)
        
        # Optionally handle duplicate filenames
        if os.path.exists(upload_path):
            filename = f"{os.path.splitext(filename)[0]}_1{os.path.splitext(filename)[1]}"
            upload_path = os.path.join("static", "uploads", filename)
        
        file.save(upload_path)
        
        # Return URL to be used by Trix
        return jsonify({
            "url": url_for("static", filename=f"uploads/{filename}")
        })
    
    return jsonify({"error": "No file received"}), 400


@app.route("/writers_blogs")
@login_required
@role_required("admin","super_admin","writer")
def writers_blogs():
    
    posts = Post.query.filter_by(author_id=current_user.id)
    return render_template('writer/writers_blogs.html',posts=posts)

@app.route("/writers_blogs/edit_blog/<int:id>", methods=['GET','POST'])
@login_required
@role_required("admin","super_admin","writer")
def edit_blog(id):
    post = Post.query.get_or_404(id)
    if request.method == 'POST':
        post.title= request.form.get("title")
        post.content= request.form.get("content")
        db.session.commit()
        return redirect(url_for('writers_blogs'))
    return render_template('writer/edit_blog.html',post=post)

@app.route("/writers_blogs/delete_blog/<int:id>", methods=['GET','POST'])
@login_required
@role_required("admin","super_admin","writer")
def delete_blog(id):
    post = Post.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('writers_blogs'))
#users dashboard

@app.route("/user_dashboard")
@login_required
@role_required("admin","super_admin","user")
def user_dashboard():
    
    return 'user bazuu'

if __name__ == '__main__':
    app.run(debug=True)