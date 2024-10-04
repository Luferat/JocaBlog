// Verifica o estado de autenticação do usuário
firebase.auth().onAuthStateChanged((user) => {
    if (user) {
        // Se o usuário estiver autenticado, exibe o formulário de comentários e preenche os campos com as informações do usuário
        $('#commentLogin').hide();
        $('#commentForm').show();
        $('#name').val(user.displayName);
        $('#email').val(user.email);
    } else {
        // Se o usuário não estiver autenticado, exibe a opção de login e limpa os campos do formulário
        $('#commentForm').hide();
        $('#commentLogin').show();
        $('#name').removeAttr('value');
        $('#email').removeAttr('value');
    }
});

// Executa a função runContacts quando o documento estiver pronto
$(document).ready(runContacts);

function runContacts() {
    // Adiciona um evento de clique ao botão de login
    $('#btnLogin').click(doLogin);
}

function doLogin() {
    // Inicia o processo de login com o provedor do Google
    firebase.auth().signInWithPopup(provider);
}
