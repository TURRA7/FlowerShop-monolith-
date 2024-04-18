document.addEventListener("DOMContentLoaded", function () {
  const menuBtn = document.querySelector('.menu_btn');
  const menu = document.querySelector('.menu');
  const menuLinks = document.querySelectorAll('.menu a');

  menuBtn.addEventListener('click', function () {
    menuBtn.classList.toggle('active');
    menu.classList.toggle('active');
  });

  // Добавляем обработчик события для каждого пункта меню
  menuLinks.forEach(function (link) {
    link.addEventListener('click', function () {
      // Скрываем меню после клика на пункте меню
      menuBtn.classList.remove('active');
      menu.classList.remove('active');
    });
  });
});


function previewImage() {
            // Получите элементы инпута и тега img
            var fileInput = document.getElementById('photo');
            var imagePreview = document.getElementById('preview');

            // Проверьте, был ли выбран файл
            if (fileInput.files && fileInput.files[0]) {
                // Создайте объект FileReader
                var reader = new FileReader();

                // Установите обработчик события для завершения чтения файла
                reader.onload = function(e) {
                    // Установите атрибут src тега img для отображения загруженной фотографии
                    imagePreview.src = e.target.result;
                };

                // Считайте выбранный файл как URL-адрес данных (base64)
                reader.readAsDataURL(fileInput.files[0]);
            }
        }


function previewImage_article() {
            // Получите элементы инпута и тега img
            var fileInput = document.getElementById('add_photo');
            var imagePreview = document.getElementById('preview_article');

            // Проверьте, был ли выбран файл
            if (fileInput.files && fileInput.files[0]) {
                // Создайте объект FileReader
                var reader = new FileReader();

                // Установите обработчик события для завершения чтения файла
                reader.onload = function(e) {
                    // Установите атрибут src тега img для отображения загруженной фотографии
                    imagePreview.src = e.target.result;
                };

                // Считайте выбранный файл как URL-адрес данных (base64)
                reader.readAsDataURL(fileInput.files[0]);
            }
        }
