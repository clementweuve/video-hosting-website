const OpenAccountDropdown = document.querySelector('#account-button-header')
const Dropdown = document.querySelector('#account-dropdown')

OpenAccountDropdown.addEventListener('click', function() {
    if (Dropdown.classList.contains('active')){
        Dropdown.classList.remove('active')
    }
    else{
        Dropdown.classList.add('active')
    }
})