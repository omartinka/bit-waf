const params = new URLSearchParams(location.search);
if (params.get('name') !== null) {
  elem = document.getElementById('name')
  elem.innerHTML += params.get('name') 
  console.log(params.get('name  '))
}

