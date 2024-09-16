const arrows = document.querySelectorAll('.arrow')
const sidebar = document.querySelector('.sidebar')
const sidebarBtn = document.querySelector('.home-content .icon')

arrows.forEach(arrow =>
	arrow.addEventListener('click', event => {
		const arrowParent = event.target.parentElement.parentElement

		arrowParent.classList.toggle('show-menu')
	})
)

sidebarBtn.addEventListener('click', () => {
	sidebar.classList.toggle('close')
})
