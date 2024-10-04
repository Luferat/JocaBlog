// Configuração do Firebase
const firebaseConfig = {
    apiKey: "AIzaSyBp9sq1PWi3O_Yn1ndkYr0Y8L6OgCzeGXk",
    authDomain: "frontpython-8973e.firebaseapp.com",
    databaseURL: "https://frontpython-8973e-default-rtdb.firebaseio.com",
    projectId: "frontpython-8973e",
    storageBucket: "frontpython-8973e.appspot.com",
    messagingSenderId: "86581909149",
    appId: "1:86581909149:web:2805bf27a895c7c6c72674"
};

// Inicializa o Firebase
const firebaseApp = firebase.initializeApp(firebaseConfig);
const auth = firebaseApp.auth();
const provider = new firebase.auth.GoogleAuthProvider();

// Verifica o estado de autenticação do usuário
firebase.auth().onAuthStateChanged((user) => {
    if (user) {
        // Se o usuário estiver autenticado, atualiza o perfil com as informações do usuário
        $('#authUser').attr({ 'data-action': 'profile' });
        $('#authUser img').attr({ 'src': user.photoURL, 'alt': user.displayName });
    } else {
        // Se o usuário não estiver autenticado, define a ação para login
        $('#authUser').attr({ 'data-action': 'login' });
        $('#authUser img').attr({ 'src': '/static/img/user.png', 'alt': 'Logue-se!' });
    }
});

// Executa a função runApp quando o documento estiver pronto
$(document).ready(runApp);

function runApp() {
    // Adiciona um evento de clique ao botão de autenticação
    $('#authUser').click(toggleAuth);
}

function toggleAuth() {
    // Verifica a ação do botão de autenticação
    if ($('#authUser').attr('data-action') === 'login') {
        // Se a ação for login, inicia o processo de login com o provedor do Google
        firebase.auth().signInWithPopup(provider);
    } else {
        // Se a ação for perfil, redireciona para a página de perfil
        location.href = '/profile';
    }
}
