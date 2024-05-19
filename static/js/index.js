document.addEventListener('DOMContentLoaded', function () {
    var expenses = [];
    var yearlyExpenses = {};
    var categoryColors = [
        '#FF5733', '#33FF57', '#3357FF', '#FF33A1', '#33FFF5',
        '#FF9633', '#FF3333', '#33FFBD', '#B833FF', '#FF33D4'
    ];
    var monthColors = [
        '#FF5733', '#FF9633', '#FFC300', '#DAF7A6', '#33FF57',
        '#33FFF5', '#3357FF', '#B833FF', '#FF33D4', '#C70039',
        '#900C3F', '#581845'
    ];

    var addExpenseBtn = document.getElementById('addExpenseBtn');
    var expenseForm = document.getElementById('expenseForm');
    var expenseList = document.getElementById('expenseItems');
    var categoryButtonsContainer = document.getElementById('categoryButtons');
    var dashboard = document.getElementById('dashboard');
    const generatedUrlElement = document.getElementById('generatedUrl');
    const copyIcon = document.querySelector('.copy-icon');
    var monthSelect = document.getElementById('monthSelect');
    var yearSelect = document.getElementById('yearSelect');

    monthSelect.addEventListener('change', resetMonthlyExpenses);
    yearSelect.addEventListener('change', switchYear);

    addExpenseBtn.addEventListener('click', function () {
        expenseForm.style.display = 'block';
        generateCategoryButtons();
    });

    var submitExpenseBtn = document.getElementById('submitExpenseBtn');
    submitExpenseBtn.addEventListener('click', function (event) {
        event.preventDefault();
        var category = document.getElementById('expenseCategory').value;
        var amount = parseFloat(document.getElementById('expenseAmount').value);
        if (category && !isNaN(amount)) {
            expenses.push({ category: category, amount: amount });
            if (!yearlyExpenses[yearSelect.value]) {
                yearlyExpenses[yearSelect.value] = [];
            }
            yearlyExpenses[yearSelect.value].push({ category: category, amount: amount, month: monthSelect.value, year: yearSelect.value });
            updateExpenseList(expenses);
            updateDonutChart(expenses);
            updateYTDChart(yearlyExpenses[yearSelect.value]);
            if (dashboard.classList.contains('small')) {
                dashboard.classList.remove('small');
                dashboard.classList.add('expanded');
            }
        }
        document.getElementById('expenseCategory').value = '';
        document.getElementById('expenseAmount').value = '';
    });

    function updateExpenseList(expenses) {
        expenseList.innerHTML = '';
        expenses.forEach(function (expense) {
            var listItem = document.createElement('li');
            listItem.textContent = `${expense.category}: $${expense.amount.toFixed(2)}`;
            expenseList.appendChild(listItem);
        });
    }

    var categoryCtx = document.getElementById('categoryChart').getContext('2d');
    var categoryChart;

    function updateDonutChart(expenses) {
        if (categoryChart) {
            categoryChart.destroy();
        }
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

        categoryChart = new Chart(categoryCtx, {
            type: 'doughnut', // Change to 'doughnut' for donut chart
            data: {
                labels: categories,
                datasets: [{
                    label: 'Expense Categories',
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
                cutout: '60%' // Adjust the cutout percentage for donut hole size
            }
        });
    }

    function generateCategoryButtons() {
        categoryButtonsContainer.innerHTML = '';
        var categories = ['Rent', 'Transportation', 'Utilities', 'Groceries', 'Eating Out', 'Other'];
        categories.forEach(function (category) {
            var button = document.createElement('button');
            button.textContent = category;
            button.addEventListener('click', function () {
                document.getElementById('expenseCategory').value = category;
            });
            categoryButtonsContainer.appendChild(button);
        });
    }

    function copyLink() {
        const linkText = generatedUrlElement.textContent;
        navigator.clipboard.writeText(linkText)
            .then(() => {
                console.log('Link copied to clipboard');
            })
            .catch((error) => {
                console.error('Failed to copy link:', error);
            });
    }

    copyIcon.addEventListener('click', copyLink);

    document.getElementById("createGroupForm").addEventListener("submit", function (event) {
        event.preventDefault();

        fetch("/create_group", {
            method: "POST"
        })
        .then(response => response.text())
        .then(data => {
            generatedUrlElement.innerText = data;
            document.getElementById("urlDisplay").style.display = 'block';
        })
        .catch(error => console.error("Error:", error));
    });

    var ytdCtx = document.getElementById('expenditureYTDChart').getContext('2d');
    var ytdChart;

    function updateYTDChart(ytdExpenses) {
        if (ytdChart) {
            ytdChart.destroy();
        }
        
        var monthlyExpenses = Array(12).fill(0);

        ytdExpenses.forEach(function (expense) {
            if (expense.year == yearSelect.value) {
                var month = parseInt(expense.month);
                monthlyExpenses[month] += expense.amount;
            }
        });

        ytdChart = new Chart(ytdCtx, {
            type: 'bar',
            data: {
                labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
                datasets: [{
                    label: 'Expenditure YTD',
                    data: monthlyExpenses,
                    backgroundColor: monthColors,
                    borderColor: monthColors,
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'bottom'
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
    }

    function resetMonthlyExpenses() {
        expenses = [];
        updateExpenseList(expenses);
        updateDonutChart(expenses);
        expenseForm.style.display = 'none';
        if (dashboard.classList.contains('expanded')) {
            dashboard.classList.remove('expanded');
            dashboard.classList.add('small');
        }
    }

    function switchYear() {
        var selectedYear = yearSelect.value;

        resetMonthlyExpenses();

        if (yearlyExpenses[selectedYear]) {
            expenses = yearlyExpenses[selectedYear].filter(expense => expense.year == selectedYear && expense.month == monthSelect.value);
            updateExpenseList(expenses);
            updateDonutChart(expenses);
        } else {
            yearlyExpenses[selectedYear] = [];
        }

        updateYTDChart(yearlyExpenses[selectedYear]);
    }
});
