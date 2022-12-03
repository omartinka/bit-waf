
async function view_logs() {
  log_elem = document.getElementById('logs')

  fetch('/api/admin/logs', {
    method: 'GET'
  }).then((r) => r.json())
    .then((data) => {
      let html = "<pre>\n";
      for (let log of data) {
        html += `${log.id}: ${log.timestamp} ${log.type} ${log.src} ${log.res} ${log.user_agent} <br>`
      }
      html += "</pre>\n";
      log_elem.innerHTML = html;
  })
}