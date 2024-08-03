function toggleDropdown(button) {
    const dropdownContent = button.nextElementSibling;
    dropdownContent.style.display = dropdownContent.style.display === 'block' ? 'none' : 'block';
  }
  
  function selectOption(option) {
    const dropdownButton = option.closest('.device-group').querySelector('.dropdown-button');
    dropdownButton.innerHTML = option.innerHTML + ' <img class="chevron-down-1 chevron-down-3" src="{% static \'img/chevronDownBlack.svg\' %}" alt="Chevron down" />';
    option.parentElement.style.display = 'none';
  }
  
  // Close the dropdown if the user clicks outside of it
  window.onclick = function(event) {
    if (!event.target.matches('.dropdown-button')) {
      const dropdowns = document.querySelectorAll('.dropdown-content');
      dropdowns.forEach(dropdown => {
        dropdown.style.display = 'none';
      });
    }
  }
  