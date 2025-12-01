document.addEventListener('DOMContentLoaded', function() {
    const button = document.getElementById('load-api');
    if (button) {
        button.addEventListener('click', function() {
            const resultDiv = document.getElementById('api-result');
            resultDiv.innerHTML = '<p>Загрузка...</p>';

            fetch('/api/consumables/')
                .then(response => {
                    if (!response.ok) {
                        throw new Error('Ошибка: ' + response.status);
                    }
                    return response.json();
                })
                .then(data => {
                    if (data.length === 0) {
                        resultDiv.innerHTML = '<p>Нет расходников.</p>';
                        return;
                    }
                    let html = '<ul class="list-group">';
                    data.forEach(item => {
                        html += `<li class="list-group-item">
                            <strong>${item.name}</strong> — ${item.quantity} ${item.unit}
                        </li>`;
                    });
                    html += '</ul>';
                    resultDiv.innerHTML = html;
                })
                .catch(error => {
                    resultDiv.innerHTML = `<div class="alert alert-danger">${error.message}</div>`;
                });
        });
    }
});