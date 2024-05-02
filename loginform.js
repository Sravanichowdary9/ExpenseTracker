function togglePassword() {
    var x = document.getElementById("pwd");
    var y = document.getElementById("toggleIcon");
    if (x.type === "password") {
        x.type = "text";
        y.classList.add("bi-eye");
        y.classList.remove("bi-eye-slash");
    } else {
        x.type = "password";
        y.classList.add("bi-eye-slash");
        y.classList.remove("bi-eye");
    }
}
