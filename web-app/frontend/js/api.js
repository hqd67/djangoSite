export const API_URL = "http://127.0.0.1:8000/api";

export function getAccessToken() {
    return localStorage.getItem("access");
}

export function isAuthenticated() {
    return !!getAccessToken();
}

export function requireAuth() {
    if (!isAuthenticated()) {
        window.location.href = "login.html";
    }
}
