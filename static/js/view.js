firebase.auth().onAuthStateChanged((user) => {
    if (user) {
        // Oculta o login
        $('#makeLogin').hide();

        // Preenche os campos nome e email com dadoos do logado
        $('#commentName').val(user.displayName)
        $('#commentEmail').val(user.email)

        // Mostra o formuário de comentário
        $('#commentForm').show();

    } else {
        // Oculta o formulário de comentário
        $('#commentForm').hide();

        // Preenche os campos nome e email com dadoos do logado
        $('#commentName').val('')
        $('#commentEmail').val('')

        // Mostra o login
        $('#makeLogin').show();
    }
});