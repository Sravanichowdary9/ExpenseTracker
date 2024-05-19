function validateDOB() {
    var dobInput = document.getElementById('dob');
    var dob = new Date(dobInput.value);
    var today = new Date();
    today.setHours(0, 0, 0, 0); 

    if (dob > today) {
        alert('Please check your Date of Birth!');
        dobInput.value = ''; 
    }
}

function checkPasswordsMatch() {
    var password = document.getElementById("password").value;
    var confirmPassword = document.getElementById("confirmPassword").value;
    var message = document.getElementById("passwordMatchMessage");
    if (password !== confirmPassword) {
        message.textContent = "Passwords do not match.";
    } else {
        message.textContent = ""; 
    }
}