// Verifica o estado de autenticação do usuário
firebase.auth().onAuthStateChanged((user) => {
    if (user) {
        // Se o usuário estiver autenticado, preenche os campos de nome e email com as informações do usuário
        $('#name').val(user.displayName);
        $('#email').val(user.email);
    }
});
