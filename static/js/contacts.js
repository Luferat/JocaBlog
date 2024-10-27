firebase.auth().onAuthStateChanged((user) => {
    // Se ususário está logado
    if (user) {
        // Preenche o nome e o email do formulário
        $('#name').val(user.displayName);
        $('#email').val(user.email);
    } else {
        // Preenche o nome e o email do formulário
        $('#name').val('');
        $('#email').val('');
    }
});