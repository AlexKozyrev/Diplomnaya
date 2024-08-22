function openTab(tabName) {
    var i, tabContent, tabButtons;
    tabContent = document.getElementsByClassName("tab-content");
    for (i = 0; i < tabContent.length; i++) {
        tabContent[i].style.display = "none";
    }
    tabButtons = document.getElementsByClassName("tab-button");
    for (i = 0; i < tabButtons.length; i++) {
        tabButtons[i].className = tabButtons[i].className.replace(" active", "");
    }
    document.getElementById(tabName).style.display = "block";
    event.currentTarget.className += " active";
}

function showDescription(category, name) {
    fetch(`/api/reference-description/?category=${category}&name=${name}`)
        .then(response => response.json())
        .then(data => {
            const modal = document.getElementById('descriptionModal');
            const descriptionText = document.getElementById('descriptionText');
            descriptionText.textContent = data.description;
            modal.style.display = 'block';
        });
}

function closeModal() {
    const modal = document.getElementById('descriptionModal');
    modal.style.display = 'none';
}

document.querySelectorAll('.reference-link').forEach(link => {
    link.addEventListener('click', function(e) {
        e.preventDefault();
        fetch(this.href)
            .then(response => response.json())
            .then(data => {
                // Display the description in a modal or tooltip
                alert(data.description);  // Simple example with alert
            });
    });
});