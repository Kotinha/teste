// Simple client-side user system for demonstration purposes
function loadUsers() {
  return JSON.parse(localStorage.getItem('users') || '{}');
}

function saveUsers(users) {
  localStorage.setItem('users', JSON.stringify(users));
}

function register(event) {
  event.preventDefault();
  const form = event.target;
  const users = loadUsers();
  const email = form.email.value;
  if (users[email]) {
    alert('Email já registrado.');
    return;
  }
  users[email] = {
    name: form.nome.value,
    email,
    password: form.senha.value,
    phone: form.telefone.value,
    cpf: form.cpf.value,
    roles: {
      membro: form.membro.checked,
      administrador: form.administrador.checked
    },
    photo: '',
    verified: true // Simula verificação de email
  };
  saveUsers(users);
  alert('Cadastro realizado! Verifique seu email.');
  window.location.href = 'login.html';
}

function login(event) {
  event.preventDefault();
  const form = event.target;
  const users = loadUsers();
  const user = users[form.email.value];
  if (!user || user.password !== form.senha.value) {
    alert('Credenciais inválidas.');
    return;
  }
  if (!user.verified) {
    alert('Email não verificado.');
    return;
  }
  localStorage.setItem('currentUser', user.email);
  window.location.href = 'profile.html';
}

function recover(event) {
  event.preventDefault();
  const email = event.target.email.value;
  const users = loadUsers();
  if (users[email]) {
    alert('Email de recuperação enviado.');
  } else {
    alert('Email não encontrado.');
  }
  window.location.href = 'login.html';
}

function loadProfile() {
  const users = loadUsers();
  const email = localStorage.getItem('currentUser');
  if (!email || !users[email]) {
    window.location.href = 'login.html';
    return;
  }
  const user = users[email];
  const form = document.getElementById('profileForm');
  form.nome.value = user.name;
  form.email.value = user.email;
  form.telefone.value = user.phone;
  form.cpf.value = user.cpf;
  form.membro.checked = user.roles.membro;
  form.administrador.checked = user.roles.administrador;
  if (user.photo) {
    document.getElementById('fotoPreview').src = user.photo;
  }
}

function updateProfile(event) {
  event.preventDefault();
  const users = loadUsers();
  const email = localStorage.getItem('currentUser');
  const form = event.target;
  const user = users[email];
  user.name = form.nome.value;
  user.phone = form.telefone.value;
  user.cpf = form.cpf.value;
  user.roles.membro = form.membro.checked;
  user.roles.administrador = form.administrador.checked;
  const file = form.foto.files[0];
  if (file) {
    const reader = new FileReader();
    reader.onload = function(e) {
      user.photo = e.target.result;
      saveUsers(users);
      alert('Perfil atualizado!');
    };
    reader.readAsDataURL(file);
  } else {
    saveUsers(users);
    alert('Perfil atualizado!');
  }
}

function logout() {
  localStorage.removeItem('currentUser');
  window.location.href = 'index.html';
}
