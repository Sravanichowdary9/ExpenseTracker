document.addEventListener("DOMContentLoaded", function() {
    fetch('/api/users')
        .then(response => response.json())
        .then(users => {
            updateLeaderboard(users);
        })
        .catch(error => console.error('Error fetching user data:', error));

    function updateLeaderboard(users) {
        const leaderboard = document.getElementById('leaderboard');
        leaderboard.innerHTML = '';  

        users.forEach((user, index) => {
            const li = document.createElement('li');
            li.className = 'list-group-item custom-list-group-item';

            let rank = '';
            let medalImage = '';

            if (index === 0) {
                medalImage = `<div class="medal"><img src="../static/images/first.png" alt="Gold Medal"></div>`;
            } else if (index === 1) {
                medalImage = `<div class="medal"><img src="../static/images/second.png" alt="Silver Medal"></div>`;
            } else if (index === 2) {
                medalImage = `<div class="medal"><img src="../static/images/third.png" alt="Bronze Medal"></div>`;
            } else {
                rank = `<div class="rank">${index + 1}</div>`;  
            }

            li.innerHTML = `
                ${rank}
                ${medalImage}
                <div class="name">${user.name}</div>
                <div class="float-end">${user.score}</div>
            `;
            leaderboard.appendChild(li);
        });
    }
});
