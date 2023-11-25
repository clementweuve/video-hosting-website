const Popup = document.querySelector("#popup");
function OpenPopup () {
    if (Popup.classList.contains('active')){
        Popup.classList.remove('active');
        blackBox.classList.remove('active');
        console.log("HIDE REPORT");
    }
    else{
        Popup.classList.add('active');
        blackBox.classList.add('active');
        console.log("SHOW REPORT");
    }
}
blackBox.addEventListener('click', function() {
    Popup.classList.remove('active');
    blackBox.classList.remove('active');
})