// TUTAJ WKLEJ LINK ZE STRONY RENDER.COM (zamiast mojego przykładowego poniżej):
const API_URL = "https://bot-lso-1.onrender.com";

// 1. Funkcja do pobierania danych z bota (ministranci, zbiórki itp.)
async function pobierzDane() {
    try {
        const response = await fetch(`${API_URL}/api/data`);
        const data = await response.json();
        console.log("Pobrane dane z bota:", data);
        return data;
    } catch (error) {
        console.error("Błąd podczas pobierania danych z bota:", error);
    }
}

// 2. Funkcja do wysyłania wiadomości na dany kanał Discorda
async function wyslijWiadomosc(kanalId, tresc) {
    try {
        const response = await fetch(`${API_URL}/api/send_message?channel_id=${kanalId}&message=${encodeURIComponent(tresc)}`, {
            method: 'POST'
        });
        const result = await response.json();
        console.log("Odpowiedź API:", result);
    } catch (error) {
        console.error("Błąd wysyłania wiadomości:", error);
    }
}
