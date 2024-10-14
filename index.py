# Importa as dependências do aplicativo
from flask import Flask, redirect, render_template, request, url_for
from flask_mysqldb import MySQL, MySQLdb

# Importa as funções do banco de dados, tabela article
from functions.db_articles import *

# Importa as funções do banco de dados, tabela comment
from functions.db_comments import *

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

@app.route('/')  # Rota para a página inicial → raiz
def home():

    # Obtém todos os artigos
    articles = get_all(mysql)

    # Somente para debug
    # print('\n\n\n', articles, '\n\n\n')

    # Passa parâmetros para o template
    # 'css' e 'js' são opcionais
    toPage = {
        # Título da página → <title></title>
        'site': SITE,
        'title': '',
        'css': 'home.css',  # Folhas de estilo desta página (opcional)
        'js': 'home.js',  # JavaScript desta página (opcional)
        # Outras chaves usadas pela página
        'articles': articles
    }

    # Renderiza template passando a variável local `toPage`
    # para o template como `page`.
    return render_template('home.html', page=toPage)


@app.route('/view/<artid>')  # Rota para a página que exibe o artigo completo
def view(artid):

    # Se o ID do artigo não é um número, mostra 404
    if not artid.isdigit():
        return page_not_found(404)

    # Obtém um artigo único
    article = get_one(mysql, artid)

    # Para debug
    # print('\n\n\n', article, '\n\n\n')

    # Se o artigo não existe, mostra 404
    if article is None:
        return page_not_found(404)

    # Atualiza as visualizações do artigo
    update_views(mysql, artid)

    # Traduz o `type` do autor
    if article['sta_type'] == 'admin':
        article['sta_pt_type'] = 'Administrador(a)'
    elif article['sta_type'] == 'author':
        article['sta_pt_type'] = 'Autor(a)'
    else:
        article['sta_pt_type'] = 'Moderador(a)'

    # Obtém mais artigos do author
    articles = get_author(mysql, article['sta_id'], article['art_id'], 4)

    # print('\n\n\n', articles, '\n\n\n')

    # Somente o primeiro nome do autor
    article['sta_first'] = article['sta_name'].split()[0]

    # Obtém todos os comentários deste artigo
    comments = get_comments(mysql, article['art_id'])

    # Total de comentários
    total_comments = len(comments)

    # print('\n\n\n', comments, '\n\n\n')

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


@app.route('/comment', methods=['POST'])
def comment():

    # Obtém dados do formulario
    form = request.form

    # Salva comentário no banco de dados
    save_comment(mysql, form)

    return redirect(f"{url_for('view', artid=form['artid'])}#comments")


@app.route('/contacts')  # Rota para a página de contatos → /contacts
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


@app.errorhandler(405)
def page_not_found(e):
    return 'Bizonhou!!'


if __name__ == '__main__':
    app.run(debug=True)
