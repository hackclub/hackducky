function toggleOverlay() {
  var overlay = document.getElementById('overlay');
  if (overlay.style.display === 'none' || overlay.style.display === '') {
    overlay.style.display = 'flex';
  } else {
    overlay.style.display = 'none';
  }
}

// Initialize overlay on page load
if (document.getElementById('overlay')) {
  toggleOverlay();
}
