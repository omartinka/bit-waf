async function login() {
  n = document.getElementById('auth_name').value
  p = document.getElementById('auth_pass').value
  fetch('/api/login', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      "name": n,
      "pass": p
    })
  }).then((response) => response.json())
    .then((data) => {
      if (Object.keys(data).includes('error') && data['error'] == true) {
        document.getElementById('error').innerHTML = 'Request blocked. Reason: ' + data['reason'];
      } else {
        window.location.href = '/';
      }
    });
}

async function register() {
  n = document.getElementById('auth_name').value
  p = document.getElementById('auth_pass').value

  console.log(n,p)

  fetch('/api/register', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      "name": n,
      "pass": p
    })
  }).then((response) => response.json())
    .then((data) => {
      if (Object.keys(data).includes('error') && data['error'] == true) {
        document.getElementById('error').innerHTML = 'Request blocked. Reason: ' + data['reason'];
      }
      console.log(data)
    });
}

async function logout() {
  document.cookie=document.cookie+";max-age=0";   
  window.location.href = '/';
}