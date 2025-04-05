import { useState } from "react";

const UpdateProfilePhoto = () => {
    const [loading, setLoading] = useState(false);
    const [file, setFile] = useState("");
    const [avatar, setAvatar] = useState(null);

    const token = localStorage.getItem("token");

    // const data = 
    try {
        await axios.post(`http://127.0.0.1:8000/users/me/avatar`,
                        formData,
                        { headers: { "Content-Type": "multipart/form-data" },
                                    Authorization: `Bearer ${token}`}
        );
    } catch (err){

    }
    


    return ( 
        <>
            <main className="section">
                <div className="container">
                    <h1>Загрузите или обновите свою фотографию</h1>
                    <form className="photo-form">
                        <label>
                            <input type="file" accept="image/*" onChange={""} required></input>
                        </label>

                        <button type="submit" disabled={!avatar}>
                            {loading ? "Отправка..." : "Обновите фотографию профиля"}
                        </button>
                    </form>
                </div>
            </main>
        </>
     );
}
 
export default UpdateProfilePhoto;