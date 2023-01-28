
const findCar = document.getElementById('find-car'),
findCarHeader = document.getElementById('findCar-Header');

if(findCar){
    findCar.addEventListener('click', ()=>{
        findCarHeader.classList.toggle('show-header');
    })
}