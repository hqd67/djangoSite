import { API_URL } from "./api.js";

export async function getArticles(category = "") {
    const url = category
        ? `${API_URL}/articles/${category}/`
        : `${API_URL}/articles/`;

    const response = await fetch(url);
    return await response.json();
}
