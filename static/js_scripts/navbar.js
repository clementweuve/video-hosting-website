const openMenu = document.querySelector('#show-menu')
const hideMenuIcon = document.querySelector('#hide-menu')
const blackBox = document.querySelector('#black-box')
const sideMenu = document.querySelector('#nav-menu')

openMenu.addEventListener('click', function() {
    sideMenu.classList.add('active')
    blackBox.classList.add('active')
})

hideMenuIcon.addEventListener('click', function() {
    sideMenu.classList.remove('active')
    blackBox.classList.remove('active')
})

blackBox.addEventListener('click', function() {
    sideMenu.classList.remove('active')
    blackBox.classList.remove('active')
})

