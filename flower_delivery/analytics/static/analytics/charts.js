document.addEventListener('DOMContentLoaded', () => {
    // Получаем данные для графиков из скрытых тегов script
    const orderStatusData = JSON.parse(document.getElementById('orderStatusData').textContent);
    const popularItemsData = JSON.parse(document.getElementById('popularItemsData').textContent);

    // Преобразуем данные для графика статуса заказов
    const orderStatusLabels = orderStatusData.map(item => item.status);
    const orderStatusCounts = orderStatusData.map(item => item.count);

    // График статуса заказов
    const orderStatusCtx = document.getElementById('orderStatusChart').getContext('2d');
    new Chart(orderStatusCtx, {
        type: 'doughnut',
        data: {
            labels: orderStatusLabels,
            datasets: [{
                label: 'Количество заказов по статусам',
                data: orderStatusCounts,
                backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF']  // Разные цвета для каждой секции
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false
        }
    });

    // Преобразуем данные для графика популярных товаров
    const popularItemsLabels = popularItemsData.map(item => item.flower__name);
    const popularItemsQuantities = popularItemsData.map(item => item.total_quantity);

    // Генерируем разные цвета для каждого столбца
    const barColors = popularItemsLabels.map((_, index) => `hsl(${index * 40}, 70%, 60%)`);

    // График популярных товаров
    const popularItemsCtx = document.getElementById('popularItemsChart').getContext('2d');
    new Chart(popularItemsCtx, {
        type: 'bar',
        data: {
            labels: popularItemsLabels,
            datasets: [{
                label: 'Популярные товары',
                data: popularItemsQuantities,
                backgroundColor: barColors  // Разные цвета для столбцов
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                x: {
                    ticks: {
                        autoSkip: false,
                        maxRotation: 45,
                        minRotation: 45
                    }
                }
            }
        }
    });
});
