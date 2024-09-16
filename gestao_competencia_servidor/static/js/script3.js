document.addEventListener('DOMContentLoaded', function () {
    var contentArea = document.querySelector('.content');
    var menuItems = document.querySelectorAll('.menu-item');

    menuItems.forEach(function (menuItem) {
        menuItem.addEventListener('click', function () {
            var page = menuItem.dataset.page;
            loadPage(page);
        });
    });

    function loadPage(page) {
        var xhttp = new XMLHttpRequest();
        xhttp.onreadystatechange = function () {
            if (this.readyState == 4 && this.status == 200) {
                contentArea.innerHTML = this.responseText;
            }
        };
        xhttp.open('GET', page, true);
        xhttp.send();
    }
});
