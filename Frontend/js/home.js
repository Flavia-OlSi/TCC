document.addEventListener('DOMContentLoaded', () => {
    const openModalButton = document.getElementById('open-modal');
    const closeModalButton = document.getElementById('close-modal');
    const partidaPesquisada = document.querySelector('.partida-pesquisada');

    // Ao abrir, esconde o botão de abrir e mostra o de fechar e a div
    openModalButton.addEventListener('click', () => {
        partidaPesquisada.classList.remove('hide');
        openModalButton.classList.add('hide');
        closeModalButton.classList.remove('hide');
    });

    // Ao fechar, mostra o botão de abrir e esconde o de fechar e a div
    closeModalButton.addEventListener('click', () => {
        partidaPesquisada.classList.add('hide');
        openModalButton.classList.remove('hide');
        closeModalButton.classList.add('hide');
    });
});