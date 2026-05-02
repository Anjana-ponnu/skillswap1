// Sidebar toggle functionality
function toggleSidebar() {
  const sidebar = document.getElementById('sidebar');
  const mainContent = document.getElementById('mainContent');
  const toggleIcon = document.getElementById('toggle-icon');

  sidebar.classList.toggle('collapsed');
  mainContent.classList.toggle('expanded');

  if (sidebar.classList.contains('collapsed')) {
    toggleIcon.className = 'fas fa-chevron-right';
  } else {
    toggleIcon.className = 'fas fa-chevron-left';
  }
}

// Profile dropdown toggle (optional)
function toggleProfileDropdown() {
  console.log('Profile dropdown clicked');
}

// If you want to highlight clicked nav-link (optional)
document.querySelectorAll('.nav-link').forEach(link => {
  link.addEventListener('click', function () {
    document.querySelectorAll('.nav-link').forEach(l => l.classList.remove('active'));
    this.classList.add('active');
  });
});
