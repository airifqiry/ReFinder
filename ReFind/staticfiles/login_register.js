const loginForm = document.getElementById('login-form');
const registerForm = document.getElementById('register-form');
const formTitle = document.getElementById('form-title');
const toggleText = document.getElementById('toggle-text');

function toggleForms() {
  const isLoginVisible = loginForm.style.display !== 'none';

  loginForm.style.display = isLoginVisible ? 'none' : 'flex';
  registerForm.style.display = isLoginVisible ? 'flex' : 'none';
  formTitle.innerText = isLoginVisible ? 'Регистрация' : 'Вход';
  toggleText.innerHTML = isLoginVisible
    ? 'Вече имаш акаунт? <a onclick="toggleForms()">Влез</a>'
    : 'Нямаш акаунт? <a onclick="toggleForms()">Регистрирай се</a>';
}
