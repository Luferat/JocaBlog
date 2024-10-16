/********************
Dados de conexão ao Firebase 
ATENÇÃO!
Troque as chaves abaixo pelas chaves do SEU Firebase!
 ********************/
const firebaseConfig = {
    apiKey: "AIzaSyADxXuzy9CItHJFp-LDuG-p8X8ba0pNKjU",
    authDomain: "flaskblog-8dc0f.firebaseapp.com",
    projectId: "flaskblog-8dc0f",
    storageBucket: "flaskblog-8dc0f.appspot.com",
    messagingSenderId: "360990466844",
    appId: "1:360990466844:web:bddb03806806061dfc10d9"
};

// Conexão com o firebase usando os dados acima
const app = firebase.initializeApp(firebaseConfig);

// Seleciona o provedor de autenticação → Google
var provider = new firebase.auth.GoogleAuthProvider();

firebase.auth().onAuthStateChanged((user) => {
    if (user) {
        // Troca a ação do botão para 'profile'
        $('#btnUser').attr({ 'data-action': 'profile' });
        // Troca para a imagem do usuário
        $('#btnUser img').attr({
            'src': user.photoURL,
            'alt': user.displayName
        });
    } else {
        // Troca a ação do botão para 'login'
        $('#btnUser').attr({ 'data-action': 'login' });
        // Troca para a imagem do usuário
        $('#btnUser img').attr({
            'src': '/static/img/user.png',
            'alt': 'Logue-se'
        });
    }
});

// Fazendo login
function login() {
    // Faz login pelo Google usando Popup
    firebase.auth().signInWithPopup(provider);
}

// Fazendo logout
function logout() {
    firebase.auth().signOut();
}

// Excluir conta do uduário
function userRemove() {
    const user = firebase.auth().currentUser;
    user.delete();
}

// Iniciaiza jQuery
$(document).ready(myApp);

// Aplicativo principal
function myApp() {

    // Monitora cliques no botão login/logout
    $('#btnUser').click(userToggle);

}

// Login / Logout do usuário
function userToggle() {
    // Lê o atributo 'data-action' do elemento '#btnUser'
    if ($('#btnUser').attr('data-action') == 'login') {

        // Se for login, executa o login
        login();
    } else {

        // Temporário: faz logout
        // logout();

        // Mostra o perfil do usuário
        location.href = '/profile';
    }
}