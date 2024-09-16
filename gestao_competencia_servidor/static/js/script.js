
const expand_btn = document.querySelector(".expand-btn");

let activeIndex;

expand_btn.addEventListener("click", () => {
  const iconImage = expand_btn.querySelector('img');

  document.body.classList.toggle("collapsed");
});

const current = window.location.href;

const allLinks = document.querySelectorAll(".sidebar-links a")

allLinks.forEach((elem) => {
  elem.addEventListener('click', function() {
    const hrefLinkClick = elem.href;

    allLinks.forEach((link) => {
      if (link.href == hrefLinkClick){
        link.classList.add("active");
      } else {
        link.classList.remove('active');
      }
    });
  })
});

document.addEventListener("DOMContentLoaded", function () {
    const allLinks = document.querySelectorAll(".sidebar-links a");
    const contentDiv = document.getElementById("content");
    const contentWrapper = document.querySelector(".content-wrapper");

    allLinks.forEach((link) => {
        link.addEventListener("click", function (event) {
            event.preventDefault(); // Impede o comportamento padrão do link

            const pageToLoad = link.getAttribute("href");

            // Use AJAX para buscar o conteúdo da página
            fetch(pageToLoad)
                .then((response) => response.text())
                .then((data) => {
                    contentDiv.innerHTML = data;

                    // Após o carregamento do conteúdo, ajuste o tamanho da content-wrapper
                    const contentHeight = contentDiv.clientHeight;
                    contentWrapper.style.height = contentHeight + "px";

                    // Certifique-se de que a altura da main seja ajustada também
                    const windowHeight = window.innerHeight;
                    contentWrapper.style.minHeight = windowHeight - 20 + "px"; // Ajuste o valor conforme necessário
                })
                .catch((error) => {
                    console.error("Erro ao carregar a página: " + error);
                });
        });
    });
});

