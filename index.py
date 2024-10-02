# Importa as dependências do aplicativo
from flask import Flask, redirect, render_template, request, url_for
from flask_mysqldb import MySQL, MySQLdb
from functions.db_articles import *

# Constantes do site
SITE = {
    'name': 'JocaBlog',
    'owner': 'Joca da Silva',
    'logo': '/static/img/logo01.png',
    'favicon': '/static/img/favicon.png'
}

# Cria uma aplicação Flask usando uma instância do Flask
app = Flask(__name__)

# Configurações de acesso ao MySQL
app.config['MYSQL_HOST'] = 'localhost'  # Servidor do MySQL
app.config['MYSQL_USER'] = 'root'       # Usuário do MySQL
app.config['MYSQL_PASSWORD'] = ''       # Senha do MySQL
app.config['MYSQL_DB'] = 'jocablogdb'   # Nome da base de dados

# Variável de conexão com o MySQL
mysql = MySQL(app)


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

    if article['sta_type'] == 'admin':
        article['type'] = 'Administrador(a)'
    elif article['sta_type'] == 'author':
        article['type'] = 'Author(a)'
    else:
        article['type'] = 'Moderador(a)'

    article['sta_first'] = article['sta_name'].split()[0]

    articles = get_by_author(mysql, article['sta_id'], article['art_id'], 4)

    comments = all_comments(mysql, article['art_id'])

    total_comments = len(comments)

    toPage = {
        'site': SITE,
        'title': article['art_title'],
        'css': 'view.css',
        'article': article,
        'articles': articles,
        'comments': comments,
        'total_comments': total_comments
    }

    return render_template('view.html', page=toPage)


@app.route('/comment', methods=['GET', 'POST'])
def comment():
    form = dict(request.form)

    sql = '''
        INSERT INTO comment (
            com_article, com_author_name, com_author_email, com_comment
        ) VALUES (
            %s, %s, %s, %s
        )
    '''
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute(sql, (form['article'], form['name'],
                form['email'], form['comment'],))
    mysql.connection.commit()
    cur.close()

    return redirect(f"{url_for('view', artid=form['article'])}#comments")


@app.route('/contacts')
def contacts():

    toPage = {
        'site': SITE,
        'title': 'Faça contato',
        'css': 'home.css'
    }
    return render_template('contacts.html', page=toPage)


@app.route('/about')
def about():
    toPage = {
        'site': SITE,
        'title': 'Sobre',
        'css': 'about.css'
    }
    return render_template('about.html', page=toPage)


@app.errorhandler(404)
def page_not_found(e):
    toPage = {
        'title': 'Erro 404',
        'site': SITE,
        'css': '404.css'
    }
    return render_template('404.html', page=toPage), 404


if __name__ == '__main__':
    app.run(debug=True)
