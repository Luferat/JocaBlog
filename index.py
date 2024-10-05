# Importa as dependências do aplicativo
from flask import Flask, redirect, render_template, request, url_for
from flask_mysqldb import MySQL
from functions.articles import *
from functions.comments import *
from functions.contacts import *
from functions.search import *
import html


# Constantes do site
SITE = {
    'name': 'JocaBlog',
    'owner': 'Joca da Silva',
    'logo': '/static/img/logo01.png',
    'favicon': '/static/img/favicon.png',
    'social': (
        {
            'name': 'Facebook',
            'link': 'https://facebook.com/pyblog',
            'icon': '<i class="fa-brands fa-facebook fa-fw fa-3x" style="color: #1877f2"></i>'
        }, {
            'name': 'LinkedIn',
            'link': 'https://linkedin.com/Pyblog',
            'icon': '<i class="fa-brands fa-linkedin-in fa-fw fa-3x" style="color: #b24020"></i>'
        }, {
            'name': 'Youtube',
            'link': 'https://youtube.com/PyBlog',
            'icon': '<i class="fa-brands fa-youtube fa-fw fa-3x" style="color: #ff0000;"></i>'
        }, {
            'name': 'GitHub',
            'link': 'https://github.com/PyBlog',
            'icon': '<i class="fa-brands fa-github fa-fw fa-3x" style="color: #6e5494;"></i>'
        }
    )
}


# Cria uma aplicação Flask usando uma instância do Flask
app = Flask(__name__)

# Configurações de acesso ao MySQL
app.config['MYSQL_HOST'] = 'localhost'          # Servidor do MySQL
app.config['MYSQL_USER'] = 'root'               # Usuário do MySQL
app.config['MYSQL_PASSWORD'] = ''               # Senha do MySQL
app.config['MYSQL_DB'] = 'jocablogdb'           # Nome da base de dados
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'  # REtorna dados como DICT

# Variável de conexão com o MySQL
mysql = MySQL(app)


# Configura a conexão com o MySQL para usar utf8mb4 e português do Brasil
@app.before_request
def before_request():
    cur = mysql.connection.cursor()
    cur.execute("SET NAMES utf8mb4")
    cur.execute("SET character_set_connection=utf8mb4")
    cur.execute("SET character_set_client=utf8mb4")
    cur.execute("SET character_set_results=utf8mb4")
    cur.execute("SET lc_time_names = 'pt_BR'")
    cur.close()


######################
# Rotas da aplicação #
######################

@app.route('/')
def home():

    articles = get_all(mysql)

    most_viewed = get_most_viewed(mysql, 4)

    most_commented = get_most_commented(mysql, 4, True)

    toPage = {
        'site': SITE,
        'title': '',
        'css': 'home.css',
        # 'js': 'home.js',
        'articles': articles,
        'most_viewed': most_viewed,
        'most_commented': most_commented
    }

    return render_template('home.html', page=toPage)


@app.route('/view/<artid>')
def view(artid):

    if not artid.isdigit():
        return page_not_found(404)

    article = get_one(mysql, artid)

    if article is None:
        return page_not_found(404)

    update_views(mysql, artid)

    match article['sta_type']:
        case 'admin':
            article['type'] = 'Administrador(a)'
        case 'author':
            article['type'] = 'Autor(a)'
        case 'moderator':
            article['type'] = 'Moderador(a)'
        case _:
            article['type'] = 'Colaborador(a)'

    article['sta_first'] = article['sta_name'].split()[0]

    articles = get_by_author(mysql, article['sta_id'], article['art_id'], 4)

    # Obtém todos os comentários deste artigo
    comments = get_comments(mysql, article['art_id'])

    # Total de comentários
    total_comments = len(comments)

    toPage = {
        'site': SITE,
        'title': article['art_title'],
        'css': 'view.css',
        'js': 'view.js',
        'article': article,  # Artigo a ser exibido
        'articles': articles,  # Artigos do autor
        'comments': comments,  # Comentários
        'total_comments': total_comments  # Total de comentários
    }

    return render_template('view.html', page=toPage)


@app.route('/comment', methods=['POST'])
def comment():

    # Obtém dados do formulario
    form = dict(request.form)

    if len(form['name'].strip()) > 3 and len(form['email'].strip()) > 3:

        # Salva comentário no banco de dados
        save_comment(mysql, form)

    return redirect(f"{url_for('view', artid=form['artid'])}#comments")


@app.route('/contacts', methods=['GET', 'POST'])
def contacts():

    sended = False
    first_name = ''

    if request.method == 'POST':
        form = dict(request.form)
        save_contact(mysql, form)
        first_name = form['name'].split()[0]
        sended = True

    toPage = {
        'site': SITE,
        'title': 'Faça contato',
        'css': 'contacts.css',
        'js': 'contacts.js',
        'sended': sended,
        'first_name': first_name
    }
    return render_template('contacts.html', page=toPage)


@app.route('/profile')
def profile():

    toPage = {
        'site': SITE,
        'title': 'Perfil do usuário',
        'css': 'profile.css',
        'js': 'profile.js'
    }

    return render_template('profile.html', page=toPage)


@app.route('/about')
def about():
    toPage = {
        'site': SITE,
        'title': 'Sobre',
        'css': 'about.css'
    }

    return render_template('about.html', page=toPage)


@app.route('/search')
def search():

    query = html.escape(request.args.get('q').strip())

    if len(query) == 0:
        return page_not_found(404)

    articles = search_articles(mysql, query)

    comments = search_comments(mysql, query)

    toPage = {
        'site': SITE,
        'title': f'Resultados de "{query}"',
        'css': 'search.css',
        'query': query,
        'articles': articles,
        'comments': comments
    }

    return render_template('search.html', page=toPage)


@app.errorhandler(404)
def page_not_found(e):
    toPage = {
        'title': 'Erro 404',
        'site': SITE,
        'css': '404.css'
    }
    return render_template('404.html', page=toPage), 404


@app.errorhandler(405)
def not_permited(e):
    return page_not_found(404)


if __name__ == '__main__':
    app.run(debug=True)
