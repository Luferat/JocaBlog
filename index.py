# Importa as dependências do aplicativo
from flask import Flask, render_template

# Constantes do site
SITE = {
    'NAME': 'JocaBlog',
    'OWNER': 'Joca da Silva',
    'LOGO': '/static/img/logo.png'
}

# Cria uma aplicação Flask usando uma instância do Flask
app = Flask(__name__)


######################
# Rotas da aplicação #
######################

@app.route('/')  # Rota para a página inicial → raiz
def home():
    # Passa parâmetros para o template
    # 'css' e 'js' são opcionais
    toPage = {
        # Título da página → <title></title>
        'site': SITE,
        'title': '',
        'css': 'home.css',  # Folhas de estilo desta página (opcional)
        'js': 'home.js',  # JavaScript desta página (opcional)
        # Outras chaves usadas pela página
        'coisas': ('casa', 'carro', 'moto', 'peteca')
    }

    # Renderiza template passando a variável local `toPage`
    # para o template como `page`.
    return render_template('home.html', page=toPage)


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


if __name__ == '__main__':
    app.run(debug=True)
