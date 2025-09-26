async function attemptLoginAndRedirect(openInNewTab) {
  const username = document.getElementById('username').value || "";

  const messageEl = document.getElementById('message');
  messageEl.textContent = 'Preparing redirect...';
  messageEl.className = 'message info';

  try {
    const resp = await fetch('/attempt-login', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({ username })
    });

    const data = await resp.json();
    if (data && data.redirect_url) {
      messageEl.textContent = data.message || 'Redirecting...';
      messageEl.className = 'message success';

      if (openInNewTab) {
        window.open(data.redirect_url, '_blank', 'noopener,noreferrer');
      } else {
        window.location.href = data.redirect_url;
      }
    } else {
      messageEl.textContent = 'Unexpected response from server.';
      messageEl.className = 'message error';
    }
  } catch (err) {
    console.error(err);
    messageEl.textContent = 'Error contacting server. Check console.';
    messageEl.className = 'message error';
  }
}

function onSubmit(e) {
  e.preventDefault();
  // Prefer explicit buttons to choose new tab or same tab actions
  return false;
}

document.getElementById('newtabBtn').addEventListener('click', function(e){ e.preventDefault(); attemptLoginAndRedirect(true); });
document.getElementById('sametabBtn').addEventListener('click', function(e){ e.preventDefault(); attemptLoginAndRedirect(false); });
