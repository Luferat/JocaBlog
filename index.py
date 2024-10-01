# Importa as dependências do aplicativo
from flask import Flask, render_template
from flask_mysqldb import MySQL, MySQLdb

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

    # Consulta SQL
    sql = '''
        -- Seleciona os campos abaixo
        SELECT art_id, art_title, art_resume, art_thumbnail
        -- desta tabela
        FROM article
        -- art_status é 'on'
        WHERE art_status = 'on'
            -- E art_date é menor ou igual à data atual
            -- Não obtém artigos com data futura (agendados)
            AND art_date <= NOW()
        -- Ordena pela data mais recente  
        ORDER BY art_date DESC;
    '''

    # Executa a query e obtém os dados na forma de DICT
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute(sql)
    articles = cur.fetchall()
    cur.close()

    # Somente para debug
    # print('\n\n\n', articles, '\n\n\n')

    # Passa parâmetros para o template
    # 'css' e 'js' são opcionais
    toPage = {
        # Título da página → <title></title>
        'site': SITE,
        'title': '',
        'css': 'home.css',  # Folhas de estilo desta página (opcional)
        # 'js': 'home.js',  # JavaScript desta página (opcional)
        # Outras chaves usadas pela página
        'articles': articles
    }

    # Renderiza template passando a variável local `toPage`
    # para o template como `page`.
    return render_template('home.html', page=toPage)


@app.route('/view/<artid>')  # Rota para a página que exibe o artigo completo
def view(artid):

    # Verifica se o artid é um número. Se não for, retorna um erro 404.
    if not artid.isdigit():
        return page_not_found(404)

    # Consulta SQL para obter os detalhes do artigo e do autor
    sql = '''
        SELECT art_id, art_date, art_title, art_content,
            -- Obtém a data em PT-BR pelo pseudo-campo `art_datebr`
            DATE_FORMAT(art_date, '%%d/%%m/%%Y às %%H:%%i') AS art_datebr,
            sta_id, sta_name, sta_image, sta_description, sta_type,
            -- Calcula a idade para `sta_age` considerando ano, mês e dia de nascimento
            TIMESTAMPDIFF(YEAR, sta_birth, CURDATE()) - 
                (DATE_FORMAT(CURDATE(), '%%m%%d') < DATE_FORMAT(sta_birth, '%%m%%d')) AS sta_age
        FROM article
        INNER JOIN staff ON art_author = sta_id
        WHERE art_id = %s
            AND art_status = 'on'
            AND art_date <= NOW();
    '''
    # Cria um cursor para executar a consulta SQL
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute(sql, (artid,))
    article = cur.fetchone()

    # Para debug: imprime o artigo no console
    # print('\n\n\n', article, '\n\n\n')

    # Se o artigo não for encontrado, retorna um erro 404
    if article is None:
        return page_not_found(404)

    # Atualiza o contador de visualizações do artigo
    sql = 'UPDATE article SET art_view = art_view + 1 WHERE art_id = %s'
    cur.execute(sql, (artid,))
    mysql.connection.commit()

    # Prepara os dados para renderizar a página
    toPage = {
        'site': SITE,
        'title': article['art_title'],
        'css': 'view.css',
        'article': article
    }

    # Fecha o cursor
    cur.close()

    # Renderiza o template 'view.html' com os dados do artigo
    return render_template('view.html', page=toPage)


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
    # Função para lidar com erros 404 (página não encontrada)
    toPage = {
        'title': 'Erro 404',  # Título da página de erro
        'site': SITE,         # Nome do site...
        'css': '404.css'      # Arquivo CSS específico para a página de erro
    }
    # Renderiza o template '404.html' com os dados da página e retorna o código de status 404
    return render_template('404.html', page=toPage), 404


if __name__ == '__main__':
    # Inicia a aplicação Flask em modo debug
    app.run(debug=True)
