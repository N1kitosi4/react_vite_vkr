// import { useEffect, useState} from 'react';

// const [reviews, setReviews] = useState([]); // Состояние для хранения отзывов
// const [loading, setLoading] = useState(true); // Состояние для отслеживания процесса загрузки

// useEffect(() => {
//     const fetchReviews = async () => {
//         try {
//             const response = await fetch("http://localhost:8000/review/"); // Поменяйте на актуальный адрес вашего API
//             const data = await response.json();
//             setReviews(data); // Обновляем состояние с отзывами
//         } catch (error) {
//             console.error("Ошибка при загрузке отзывов:", error);
//         } finally {
//             setLoading(false); // Завершаем загрузку
//         }
//     };

//     fetchReviews();
// }, []); // Эффект срабатывает при монтировании компонента


// const images = reviews.length > 0 ? (
//     reviews.map((review) => (
//         review.img
//     ))
// ) : (
//     <p>Отзывов нет.</p>
// )