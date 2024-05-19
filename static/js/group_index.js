document.addEventListener('DOMContentLoaded', function () {
    var categoryColors = [
        '#FF5733', '#33FF57', '#3357FF', '#FF33A1', '#33FFF5',
        '#FF9633', '#FF3333', '#33FFBD', '#B833FF', '#FF33D4'
    ];

    function fetchGroupExpenses() {
        fetch('/get_group_expenses')
            .then(response => response.json())
            .then(data => {
                updateMemberCharts(data);
                updateInsights(data);
            })
            .catch(error => console.error('Error fetching group expenses:', error));
    }

    function updateMemberCharts(groupMembers) {
        var memberChartsContainer = document.getElementById('memberCharts');
        memberChartsContainer.innerHTML = '';

        groupMembers.forEach(member => {
            var memberChartDiv = document.createElement('div');
            memberChartDiv.classList.add('memberChart');

            var memberNameHeading = document.createElement('h3');
            memberNameHeading.textContent = member.name;
            memberChartDiv.appendChild(memberNameHeading);

            var chartCanvas = document.createElement('canvas');
            chartCanvas.width = 400;
            chartCanvas.height = 400;

            memberChartDiv.appendChild(chartCanvas);
            memberChartsContainer.appendChild(memberChartDiv);

            createDonutChart(chartCanvas.getContext('2d'), member.expenses, `${member.name}'s Expenses`);
        });
    }

    function createDonutChart(ctx, expenses, title) {
        var categories = [];
        var amounts = [];

        expenses.forEach(function (expense) {
            if (categories.includes(expense.category)) {
                var index = categories.indexOf(expense.category);
                amounts[index] += expense.amount;
            } else {
                categories.push(expense.category);
                amounts.push(expense.amount);
            }
        });

        var colors = categoryColors.slice(0, categories.length);

        new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: categories,
                datasets: [{
                    label: title,
                    data: amounts,
                    backgroundColor: colors,
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'bottom'
                    }
                },
                cutout: '60%'
            }
        });
    }

    function updateInsights(groupMembers) {
        var totalExpenses = groupMembers.reduce((total, member) => {
            return total + member.expenses.reduce((memberTotal, expense) => memberTotal + expense.amount, 0);
        }, 0);

        var highestSpender = groupMembers.reduce((max, member) => {
            var memberTotal = member.expenses.reduce((memberTotal, expense) => memberTotal + expense.amount, 0);
            return memberTotal > max.amount ? { name: member.name, amount: memberTotal } : max;
        }, { name: '', amount: 0 });

        var insights = [
            { title: 'Total Group Expenses', value: `$${totalExpenses.toFixed(2)}` },
            { title: 'Highest Spender', value: `${highestSpender.name}: $${highestSpender.amount.toFixed(2)}` }
        ];

        var insightCardsContainer = document.getElementById('insightCards');
        insightCardsContainer.innerHTML = '';

        insights.forEach(insight => {
            var card = document.createElement('div');
            card.classList.add('insightCard');
            card.innerHTML = `<h3>${insight.title}</h3><p>${insight.value}</p>`;
            insightCardsContainer.appendChild(card);
        });
    }

    fetchGroupExpenses();
});
