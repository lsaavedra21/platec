const arrows = document.querySelectorAll('.arrow');
const sidebar = document.querySelector('.sidebar');
const sidebarBtn = document.querySelector('.home-content .icon');
const content = document.querySelector('.content');

arrows.forEach(arrow =>
    arrow.addEventListener('click', event => {
        const arrowParent = event.target.parentElement.parentElement;
        arrowParent.classList.toggle('show-menu');

        // Atualiza a margem esquerda da .content quando o tamanho da barra lateral muda
        content.style.marginLeft = sidebar.classList.contains('close') ? 'var(--sidebar-sw)' : 'var(--sidebar-dw)';
    })
);

sidebarBtn.addEventListener('click', () => {
    sidebar.classList.toggle('close');

    // Atualiza a margem esquerda da .content quando o tamanho da barra lateral muda
    content.style.marginLeft = sidebar.classList.contains('close') ? 'var(--sidebar-sw)' : 'var(--sidebar-dw)';
});
