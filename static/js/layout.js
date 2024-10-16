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
        console.log('Logado', user)
    } else {
        console.log('Não tá logado!')
    }
});

// Fazendo login
function login() {
    // Faz login pelo Google usando Popup
    firebase.auth().signInWithPopup(provider)
}

login()

/*


// logout
firebase.auth().signOut().then(() => {
  // Sign-out successful.
}).catch((error) => {
  // An error happened.
});

// Excluir conta do usuario
const user = firebase.auth().currentUser;

user.delete().then(() => {
  // User deleted.
}).catch((error) => {
  // An error ocurred
  // ...
});

*/
