# Importa as dependências do aplicativo
from flask import Flask, redirect, render_template, request, url_for
from flask_mysqldb import MySQL

# Importa as funções do banco de dados
from functions.db_articles import *
from functions.db_comments import *
from functions.db_contacts import save_contact

import json

# Constantes do site
SITE = {
    'name': 'JocaBlog',
    'owner': 'Joca da Silva',
    'logo': '/static/img/logo01.png',
    'favicon': '/static/img/favicon.png'
}

# Lista de redes sociais
SOCIAL = (
    {
        'name': 'Facebook',
        'link': 'https://facebook.com/jocablog',
        'icon': '<i class="fa-brands fa-square-facebook fa-fw"></i>'
    },
    {
        'name': 'Linkedin',
        'link': 'https://linkedin.com/in/jocablog',
        'icon': '<i class="fa-brands fa-linkedin fa-fw"></i>'
    },
    {
        'name': 'Youtube',
        'link': 'https://youtube.com/jocablog',
        'icon': '<i class="fa-brands fa-square-youtube fa-fw"></i>'
    }, {
        'name': 'GitHub.com',
        'link': 'https://github.com/jocablog',
        'icon': '<i class="fa-brands fa-square-github fa-fw"></i>'
    },
)

# Cria uma aplicação Flask usando uma instância do Flask
app = Flask(__name__)

# Configurações de acesso ao MySQL
app.config['MYSQL_HOST'] = 'localhost'  # Servidor do MySQL
app.config['MYSQL_USER'] = 'root'       # Usuário do MySQL
app.config['MYSQL_PASSWORD'] = ''       # Senha do MySQL
app.config['MYSQL_DB'] = 'jocablogdb'   # Nome da base de dados

'''
# Configurações de acesso ao MySQL do provedor
app.config['MYSQL_HOST'] = 'Luferat.mysql.pythonanywhere-services.com'
app.config['MYSQL_USER'] = 'Luferat'
app.config['MYSQL_PASSWORD'] = 'Mysqlp4ssw0rd'
app.config['MYSQL_DB'] = 'Luferat$default'
'''

# Variável de conexão com o MySQL
mysql = MySQL(app)

######################
# Rotas da aplicação #
######################


@app.route('/')  # Rota para a página inicial → raiz
def home():

    # Obtém todos os artigos
    articles = get_all(mysql)

    # Obtém artigos mais comentados
    commenteds = most_commented(mysql)

    # Artigos mais visitados
    vieweds = most_viewed(mysql)

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
        'articles': articles,
        'commenteds': commenteds,
        'vieweds': vieweds
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
        'js': 'view.js',
        'article': article,
        'articles': articles,
        'comments': comments,
        'total_comments': total_comments
    }

    return render_template('view.html', page=toPage)


@app.route('/comment', methods=['POST'])
def comment():

    # Obtém dados do formulario
    form = dict(request.form)

    # Se o form está vazio
    if form['name'] != None and form['name'] != '' and form['email'] != None and form['email'] != '':

        # Salva comentário no banco de dados
        save_comment(mysql, form)

    return redirect(f"{url_for('view', artid=form['artid'])}#comments")


# Rota para a página de contatos → /contacts
@app.route('/contacts', methods=['GET', 'POST'])
def contacts():

    # Formulário enviado com sucesso
    success = False

    # Primeiro nome do remetente
    first_name = ''

    # Se o formulário foi enviado...
    if request.method == 'POST':

        # Obtém os dados do formulário
        form = dict(request.form)

        # Teste de "mesa"
        # print('\n\n\n', form, '\n\n\n')

        # Salva os dados no banco de dados
        success = save_contact(mysql, form)

        # Otém o primeiro nome do remetente
        first_name = form['name'].split()[0]

    toPage = {
        'site': SITE,
        'title': 'Faça contato',
        'css': 'contacts.css',
        'js': 'contacts.js',
        'success': success,
        'first_name': first_name,
        'social': SOCIAL
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


@app.route('/privacy')
def privacy():
    toPage = {
        'site': SITE,
        'title': 'Políticas de Privacidade'
    }
    return render_template('privacy.html', page=toPage)


@app.route('/profile')
def profile():

    # recebe o cookie do front-end
    userJSON = request.cookies.get('userData') 

    # converte o cookie para DICT
    user = json.loads(userJSON)

    # Obtém todos os comentários deste email
    comments = user_coments(mysql, user['email'], 6)

    # print('\n\n\n', comments, '\n\n\n')

    toPage = {
        'site': SITE,
        'title': 'Pefil do usuário',
        'css': 'profile.css',
        'js': 'profile.js',
        'comments': comments
    }

    return render_template('profile.html', page=toPage)


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


@app.route('/search')
def search():

    # Obtém o termo a ser procurado
    query = request.args.get('q')

    # Obtém todos o artigos contendo o termo
    articles = articles_search(mysql, query)

    # Quantos resultados foram encontrados
    total = len(articles)

    # Artigos mais recentes para a aside
    recents = get_all(mysql, 4)

    # print('\n\n\n', total, articles, '\n\n\n')

    toPage = {
        'title': 'Procura',
        'site': SITE,
        'css': 'home.css',
        'articles': articles,
        'total': total,
        'query': query,
        'recents': recents
    }

    return render_template('/search.html', page=toPage)


if __name__ == '__main__':
    app.run(debug=True)
