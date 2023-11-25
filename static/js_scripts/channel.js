const videos_btn = document.querySelector('#videos_channel_btn')
const about_btn = document.querySelector('#about_channel_btn')
const videos_list_page = document.querySelector('#videos_list_page')
const about_page = document.querySelector('#about_page')

videos_btn.addEventListener('click', function() {
    if (!videos_list_page.classList.contains('active')){
        videos_list_page.classList.add('active')
        videos_btn.classList.add('active')
        about_page.classList.remove('active')
        about_btn.classList.remove('active')
    }
})

about_btn.addEventListener('click', function() {
    if (!about_page.classList.contains('active')){
        videos_list_page.classList.remove('active')
        videos_btn.classList.remove('active')
        about_page.classList.add('active')
        about_btn.classList.add('active')
    }
})

