document.addEventListener('DOMContentLoaded', function() {
    const selectField = document.querySelector('.select-field.select-7');
    const dropdownMenu = selectField.querySelector('.dropdown-menu');
    const selectDisplay = selectField.querySelector('.v.v-30');
  
    selectField.addEventListener('click', function(event) {
      event.stopPropagation(); // Verhindert das Schließen des Menüs beim Klicken auf das Feld
      dropdownMenu.style.display = dropdownMenu.style.display === 'block' ? 'none' : 'block';
    });
  
    dropdownMenu.addEventListener('click', function(event) {
      if (event.target.classList.contains('dropdown-option')) {
        selectDisplay.textContent = event.target.textContent;
        dropdownMenu.style.display = 'none';
      }
    });
  
    document.addEventListener('click', function(event) {
      if (!selectField.contains(event.target)) {
        dropdownMenu.style.display = 'none';
      }
    });
  });