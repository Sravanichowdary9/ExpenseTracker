document.addEventListener('DOMContentLoaded', function () {
    var expenses = [];
    var categoryColors = [
        '#FF5733', '#33FF57', '#3357FF', '#FF33A1', '#33FFF5',
        '#FF9633', '#FF3333', '#33FFBD', '#B833FF', '#FF33D4'
    ];

    var addExpenseBtn = document.getElementById('addExpenseBtn');
    var expenseForm = document.getElementById('expenseForm');
    var expenseList = document.getElementById('expenseItems');
    var categoryButtonsContainer = document.getElementById('categoryButtons');
    var dashboard = document.getElementById('dashboard');
    const generatedUrlElement = document.getElementById('generatedUrl');
    const copyIcon = document.querySelector('.copy-icon');

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
            updateExpenseList(expenses);
            updateDonutChart(expenses);
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
});
