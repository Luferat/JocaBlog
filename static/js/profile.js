$(document).ready(runProfile)

firebase.auth().onAuthStateChanged((user) => {
    // Se ususário está logado
    if (user) {
        $('#logged img').attr({
            'src': user.photoURL,
            'alt': user.displayName
        })
        $('#logged h2').html(user.displayName)
        $('#id').html('ID → ' + user.uid)
        $('#email').html(user.email)
        $('#registered').html('Cadastrado em ' + dateConvert(user.metadata.creationTime))
        $('#lastLogin').html('Último login em ' + dateConvert(user.metadata.lastSignInTime))
        $('#notLogged').hide()
        $('#logged').show()
    } else {
        $('#logged').hide()
        $('#notLogged').show()
    }
});

function runProfile() {
    // Mostra o perfil do usuário no Google
    $('#toGoogle').click(() => {
        window.open('https://myaccount.google.com/', '_blank');
    })

    // Faz logout 
    $('#btnLogout').click(logout);

    // Faz login
    $('#btnLogin').click(login);
}


function dateConvert(date) {
    // Cria uma nova instância do objeto Date com base no valor de date
    const dateObj = new Date(date);

    // Obtém o dia do mês e adiciona um zero à esquerda caso tenha um dígito
    const day = dateObj.getDate().toString().padStart(2, '0');

    // Obtém o mês (0-11), adiciona 1 para ajustar ao formato humano (1-12) e adiciona um zero à esquerda
    const month = (dateObj.getMonth() + 1).toString().padStart(2, '0');

    // Obtém o ano completo
    const year = dateObj.getFullYear();

    // Formata a data como dd/mm/yyyy
    const formattedDate = `${day}/${month}/${year}`;

    // Retorna a data formatada
    return formattedDate;
}
