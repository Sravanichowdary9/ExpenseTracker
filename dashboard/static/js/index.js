document.addEventListener('DOMContentLoaded', function () {
    var expenses = [];
    var categoryColors = [
        '#FF6384', // Red
        '#36A2EB', // Blue
        '#FFCE56', // Yellow
        '#4BC0C0', // Cyan
        '#9966FF', // Purple
        '#FF9F40', // Orange
        '#2E8B57', // Sea Green
        '#FFD700', // Gold
        '#CD5C5C', // Indian Red
        '#7B68EE'  // Medium Slate Blue
    ];

    var addExpenseBtn = document.getElementById('addExpenseBtn');
    var expenseForm = document.getElementById('expenseForm');
    var expenseList = document.getElementById('expenseItems');
    var categoryButtonsContainer = document.getElementById('categoryButtons'); // Reference to category buttons container

    addExpenseBtn.addEventListener('click', function () {
        expenseForm.style.display = 'block';
        // Generate category buttons
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
            updatePieChart(expenses);   
            // You can add further logic here to store data in the database
        }
        expenseForm.reset();
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

    function updatePieChart(expenses) {
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

        // Assign colors to categories
        var colors = categoryColors.slice(0, categories.length);

        categoryChart = new Chart(categoryCtx, {
            type: 'pie',
            data: {
                labels: categories,
                datasets: [{
                    label: 'Expense Categories',
                    data: amounts,
                    backgroundColor: colors,
                }]
            },
            options: {
                responsive: true
            }
        });
    }

    // Function to generate category buttons dynamically
    function generateCategoryButtons() {
        categoryButtonsContainer.innerHTML = ''; // Clear existing buttons
        var categories = ['Food', 'Transportation', 'Utilities', 'Entertainment']; // Define categories
        categories.forEach(function (category) {
            var button = document.createElement('button');
            button.textContent = category;
            button.addEventListener('click', function () {
                document.getElementById('expenseCategory').value = category; // Set category in input field when button is clicked
            });
            categoryButtonsContainer.appendChild(button);
        });
    }
});

document.addEventListener("DOMContentLoaded", function() {
    document.getElementById("createGroupForm").addEventListener("submit", function(event) {
        event.preventDefault(); // Prevent default form submission

        fetch("/create_group", {
            method: "POST"
        })
        .then(response => response.text()) // Expecting plain text response
        .then(data => {
            document.getElementById("generatedUrl").innerText = data; // Update the URL display
            document.getElementById("urlDisplay").style.display = 'block'; // Show the URL display area
        })
        .catch(error => console.error("Error:", error));
    });
});