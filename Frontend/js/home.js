document.addEventListener('DOMContentLoaded', () => {
    const openModalButton = document.getElementById('open-modal');
    const closeModalButton = document.getElementById('close-modal');
    const cardAviso = document.querySelector('.card-aviso');

    // Ao abrir, esconde o botão de abrir e mostra o de fechar e a div
    openModalButton.addEventListener('click', () => {
        cardAviso.classList.remove('hide');
        openModalButton.classList.add('hide');
        closeModalButton.classList.remove('hide');
    });

    // Ao fechar, mostra o botão de abrir e esconde o de fechar e a div
    closeModalButton.addEventListener('click', () => {
        cardAviso.classList.add('hide');
        openModalButton.classList.remove('hide');
        closeModalButton.classList.add('hide');
    });
});