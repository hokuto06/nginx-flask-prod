
let accessToken = null;
let refreshToken = null;

export async function registerUser(email, username, password) {
  const response = await fetch('/auth/users/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, username, password })
  });
  const data = await response.json();
  if (!response.ok) {
    alert('Error en registro: ' + JSON.stringify(data));
  } else {
    alert('Registro exitoso. Ahora podés iniciar sesión.');
  }
}

export async function login(email, password) {
  const response = await fetch('/api/auth/login', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password })
  });
  const data = await response.json();
  if (response.ok) {
    accessToken = data.access;
    refreshToken = data.refresh;
    alert('Login exitoso');
  } else {
    alert('Login inválido: ' + JSON.stringify(data));
  }
}

export function getAccessToken() {
  return accessToken;
}

export async function refreshAccessToken() {
  const response = await fetch('/auth/jwt/refresh/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ refresh: refreshToken })
  });
  const data = await response.json();
  if (response.ok) {
    accessToken = data.access;
    return true;
  } else {
    alert('No se pudo refrescar el token');
    return false;
  }
}
