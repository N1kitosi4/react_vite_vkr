// const prevBtn = document.querySelector('.prev-btn');
// const nextBtn = document.querySelector('.next-btn');
// const sliderWrapper = document.querySelector('.slider-wrapper');
// const reviewCards = document.querySelectorAll('.review-card');
// let currentIndex = 0;

// const maxIndex = reviewCards.length - 3;

// function updateSliderPosition() {
//     const offset = -currentIndex * 390; // 370px (ширина карточки) + 20px (отступ между карточками)
//     sliderWrapper.style.transform = `translateX(${offset}px)`;
// }

// nextBtn.addEventListener('click', () => {
//     if (currentIndex < maxIndex) {
//         currentIndex++;
//         updateSliderPosition();
//     }
// });

// prevBtn.addEventListener('click', () => {
//     if (currentIndex > 0) {
//         currentIndex--;
//         updateSliderPosition();
//     }
// });

const prevBtn = document.querySelector('.prev-btn');
console.log(prevBtn)
const nextBtn = document.querySelector('.next-btn');
console.log(nextBtn)
const sliderWrapper = document.querySelector('.slider-wrapper');
const reviewCards = document.querySelectorAll('.review-card');
let currentIndex = 0;

const maxIndex = reviewCards.length - 3; // Макс. индекс для прокрутки 3-х карточек

function updateSliderPosition() {
    const offset = -currentIndex * (reviewCards[0].offsetWidth + 20); // Рассчитываем с учетом отступов
    console.log(offset)
    sliderWrapper.style.transform = `translateX(${offset}px)`;
}

nextBtn.addEventListener('click', () => {
    if (currentIndex < maxIndex) {
        currentIndex++;
        updateSliderPosition();
    }
});

prevBtn.addEventListener('click', () => {
    if (currentIndex > 0) {
        currentIndex--;
        updateSliderPosition();
    }
});

// Изначальная позиция
updateSliderPosition();
