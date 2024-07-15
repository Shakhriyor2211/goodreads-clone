const user_dropdown_btn = document.querySelector('#drop_down_btn');
const user_dropdown = document.querySelector('#drop_down');
const user_dropdown_close = document.querySelector('#drop_down_close');

if(user_dropdown_btn && user_dropdown && user_dropdown_close){
    user_dropdown_btn.addEventListener('click', () => {
    user_dropdown.classList.toggle('hidden');
    user_dropdown_close.classList.toggle('hidden');
});
user_dropdown_close.addEventListener('click', () => {
    user_dropdown.classList.toggle('hidden');
    user_dropdown_close.classList.toggle('hidden');
});
}