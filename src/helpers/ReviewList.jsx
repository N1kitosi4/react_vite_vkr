// import React, { useEffect, useState } from "react";
// import HomeReview from "./HomeReview"; // Импорт компонента с карточкой отзыва

// const ReviewsList = () => {
//     const [reviews, setReviews] = useState([]); // Состояние для хранения отзывов
//     const [loading, setLoading] = useState(true); // Состояние для отслеживания загрузки

//     useEffect(() => {
//         const fetchReviews = async () => {
//             try {
//                 const response = await fetch("http://127.0.0.1:8000/reviews/"); // Замените URL на актуальный
//                 const data = await response.json();
//                 setReviews(data); // Обновляем состояние с отзывами
//             } catch (error) {
//                 console.error("Ошибка при загрузке отзывов:", error);
//             } finally {
//                 setLoading(false); // Завершаем загрузку
//             }
//         };

//         fetchReviews();
//     }, []); // Эффект выполнится только один раз при монтировании компонента

//     if (loading) {
//         return <div>Загрузка...</div>;
//     }

//     if (reviews) {
//         return console.log(reviews)
//     }

    

//     return (
//         <ul className="reviews-list">
//             {reviews.length > 0 ? (
//                 reviews.map((review) => (
//                     <HomeReview key={review.id} review={review} />
                
//                 ))
//             ) : (
//                 <p>Отзывов нет.</p>
//             )}
//         </ul>
//     );
// }

// export default ReviewsList;
