jQuery(function ($) {
    var catalog = {
        init: function () {
            catalog.cacheElements();
            catalog.bindEvents();
        },

        cacheElements: function () {
            catalog.$selectAllCheckbox = $('#id-select-all-checkbox');
            catalog.$checkboxes = $('.book-table-checkbox');
            catalog.$editButton = $('.edit-button');
            catalog.$editBox = $('.editable input');
            catalog.$addAuthorPlus = $('#id-add-author');
            catalog.$authorsList = $('#authors');
        },

        bindEvents: function () {
            catalog.$selectAllCheckbox.on('change', catalog.changeCheckboxes);
            catalog.$editButton.on('click', catalog.editBook);
            catalog.$editBox.on('keypress', catalog.editSubmit);
            catalog.$addAuthorPlus.on('click', catalog.addAuthorField);
        },

        changeCheckboxes: function () {
            catalog.$checkboxes.prop('checked', $(this).is(':checked'));
        },

        editBook: function () {
            var editables = $(this).parents('tr').find('.editable');
            if ($(this).val() == 'Edit') {
                this.value = 'Save';
            }
            else if ($(this).val() == 'Save') {
                this.value = 'Edit';

                var data = {
                    'book_id': this.dataset.bookId,
                    'title': $(editables[1]).find('input').val()
                };
                var names = $(editables[0]).find('input').val().split(',');
                for (var i in names) {
                    data['authors-'+i] = names[i].trim();
                }

                $.ajax({
                    url: '/edit/',
                    type: 'POST',
                    dataType: "json",
                    data: data,
                    success: function (data) {
                        // refresh author and title on page
                        $(editables[0]).find('span').text(data['authors']);
                        $(editables[1]).find('span').text(data['title']);
                        if (data['error']) {
                            alert(data['error']);
                        }
                    },
                    error: function (data) {
                        alert(data.statusText);
                    }
                });
            }

            for (var i = 0; i < editables.length; i++) {
                $(editables[i]).find('input').toggle();
                $(editables[i]).find('span').toggle();
            }
        },

        editSubmit: function (event) {
            var code = event.keyCode || event.which;
            if (code == 13) { //Enter keycode
                event.stopPropagation();
                event.preventDefault();
            }
        },

        addAuthorField: function() {
            var $newAuthorField = catalog.$authorsList.find('li:first-child').clone();
            $newAuthorField.find('label').attr('for', 'authors-'+catalog.$authorsList.children().length);
            $newAuthorField.find('input').attr('id', 'authors-'+catalog.$authorsList.children().length);
            $newAuthorField.find('input').attr('name', 'authors-'+catalog.$authorsList.children().length);
            catalog.$authorsList.append($newAuthorField);
        }
    };
    catalog.init();
});
