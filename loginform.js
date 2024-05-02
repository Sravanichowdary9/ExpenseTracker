function togglePassword(inputId, iconId) {
    var input = document.getElementById(inputId);
    var icon = document.getElementById(iconId);
    if (input.type === "password") {
        input.type = "text";
        icon.classList.remove("bi-eye-slash");
        icon.classList.add("bi-eye");
    } else {
        input.type = "password";
        icon.classList.remove("bi-eye");
        icon.classList.add("bi-eye-slash");
    }
}

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

function validatePasswords() {
    var password = document.getElementById("password").value;
    var confirmPassword = document.getElementById("confirmPassword").value;
    if (password !== confirmPassword) {
        alert("Passwords do not match.");
        return false; 
    }
    return true;
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