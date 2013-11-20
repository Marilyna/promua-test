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
        },

        bindEvents: function () {
            catalog.$selectAllCheckbox.on('change', catalog.changeCheckboxes);
            catalog.$editButton.on('click', catalog.editBook);
            catalog.$editBox.on('keypress', catalog.editSubmit);
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

                $.ajax({
                    url: '/edit/',
                    type: 'POST',
                    dataType: "json",
                    data: {
                        'book_id': this.dataset.bookId,
                        'author': $(editables[0]).find('input').val(),
                        'title': $(editables[1]).find('input').val()
                    },
                    success: function (data) {
                        // refresh author and title on page
                        $(editables[0]).find('span').text(data['author']);
                        $(editables[1]).find('span').text(data['title']);
                    },
                    error: function (data) {
                        console.log(data['error']);
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
        }
    };
    catalog.init();
});
