// Verifica o estado de autenticação do usuário
firebase.auth().onAuthStateChanged((user) => {
    if (user) {
        // Se o usuário estiver autenticado, atualiza o perfil com as informações do usuário
        $('#profile img').attr({ 'src': user.photoURL, 'alt': user.displayName });
        $('#profile h4').html(user.displayName);
        $("#email").html(user.email);
        $("#uid").html(user.uid);
    } else {
        // Se o usuário não estiver autenticado, redireciona para a página inicial
        location.href = '/';
    }
});

// Executa a função runProfile quando o documento estiver pronto
$(document).ready(runProfile);

function runProfile() {
    // Adiciona um evento de clique ao botão de perfil para abrir a página de conta do Google em uma nova guia
    $('#toProfile').click(() => {
        window.open('https://myaccount.google.com/', '_blank');
    });

    // Adiciona um evento de clique ao botão de logout para desconectar o usuário
    $('#toLogout').click(() => {
        firebase.auth().signOut().then(() => {
            // Redireciona para a página inicial após o logout
            location.href = '/';
        }).catch((error) => {
            console.error('Erro ao fazer logout:', error);
        });
    });
}
