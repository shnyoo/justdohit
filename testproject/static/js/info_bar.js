// ================= MENU SHOW Y HIDDEN =================
const navMenu = document.getElementById('nav-menu'),
    navToggle = document.getElementById('nav-toggle'),
    navClose = document.getElementById('nav-close'),
    searchBar = document.querySelector('.search');
    

// ========= MENU SHOW ============
if(navToggle){
    navToggle.addEventListener('click', () => {
        navMenu.classList.add('show-menu');
    })
}

// ========= MENU Hidden ==========
if(navClose){
    navClose.addEventListener('click', () => {
        navMenu.classList.remove('show-menu');
    })
}




// Removing MENU Mobile when clicking nav__link
const navLink = document.querySelectorAll('.nav__link');

function linkAction(){
    const navMenu = document.getElementById('nav-menu');
    navMenu.classList.remove('show-menu');
}
navLink.forEach(x => x.addEventListener('click', linkAction));
