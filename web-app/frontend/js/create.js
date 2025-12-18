import { API_URL, getAccessToken } from "./api.js";

export async function createArticle(title, text, category) {
    const token = getAccessToken();
    if (!token) {
        throw new Error("Не авторизован");
    }

    const response = await fetch(`${API_URL}/articles/`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${token}`
        },
        body: JSON.stringify({ title, text, category })
    });

    if (!response.ok) {
        const err = await response.json();
        throw new Error(err.error || "Ошибка создания статьи");
    }
}
