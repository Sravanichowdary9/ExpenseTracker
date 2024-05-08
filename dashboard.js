document.addEventListener('DOMContentLoaded', function () {
    var ctx = document.getElementById('expenseChart').getContext('2d');
    var expenseChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['Groceries', 'Dining Out', 'Transportation', 'Utilities', 'Entertainment'],
            datasets: [{
                label: 'Weekly Expenses',
                data: [50, 30, 20, 10, 40],
                backgroundColor: [
                    'rgba(255, 99, 132, 0.2)',
                    'rgba(54, 162, 235, 0.2)',
                    'rgba(255, 206, 86, 0.2)',
                    'rgba(75, 192, 192, 0.2)',
                    'rgba(153, 102, 255, 0.2)'
                ],
                borderColor: [
                    'rgba(255, 99, 132, 1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)',
                    'rgba(75, 192, 192, 1)',
                    'rgba(153, 102, 255, 1)'
                ],
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });

    var categoryCtx = document.getElementById('categoryChart').getContext('2d');
    var categoryChart = new Chart(categoryCtx, {
        type: 'pie',
        data: {
            labels: ['Groceries', 'Dining Out', 'Transportation', 'Utilities', 'Entertainment'],
            datasets: [{
                label: 'Expense Categories',
                data: [300, 200, 150, 100, 250],
                backgroundColor: [
                    'rgba(255, 99, 132, 0.5)',
                    'rgba(54, 162, 235, 0.5)',
                    'rgba(255, 206, 86, 0.5)',
                    'rgba(75, 192, 192, 0.5)',
                    'rgba(153, 102, 255, 0.5)'
                ]
            }]
        },
        options: {
            responsive: true
        }
    });

    var trendCtx = document.getElementById('trendChart').getContext('2d');
    var trendChart = new Chart(trendCtx, {
        type: 'line',
        data: {
            labels: ['Week 1', 'Week 2', 'Week 3', 'Week 4'],
            datasets: [{
                label: 'Weekly Spending',
                data: [450, 400, 500, 600],
                backgroundColor: 'rgba(54, 162, 235, 0.2)',
                borderColor: 'rgba(54, 162, 235, 1)',
                borderWidth: 2
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
});
