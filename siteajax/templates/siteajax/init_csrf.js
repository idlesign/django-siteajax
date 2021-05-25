
function getCsrfToken(name) {
    let value = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                value = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return value;
}
const csrfToken = getCsrfToken('csrftoken');

htmx.on('htmx:configRequest', (e) => {
    if (csrfToken) {
        e.detail.headers['X-CSRFToken'] = csrfToken;
    }
});
