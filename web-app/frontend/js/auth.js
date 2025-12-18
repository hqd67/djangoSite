import { API_URL } from "./api.js";

export async function login(email, password) {
    const response = await fetch(`${API_URL}/token/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password })
    });

    if (!response.ok) {
        throw new Error("Неверный email или пароль");
    }

    const data = await response.json();
    localStorage.setItem("access", data.access);
    localStorage.setItem("refresh", data.refresh);
}

export function logout() {
    localStorage.clear();
    window.location.href = "index.html";
}
