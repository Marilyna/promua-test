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
        },

        bindEvents: function () {
            catalog.$selectAllCheckbox.on('change', catalog.changeCheckboxes);
            catalog.$editButton.on('click', catalog.editBook);
        },

        changeCheckboxes: function () {
            catalog.$checkboxes.prop('checked', $(this).is(':checked'));
        },

        editBook: function (event) {
            var target = event.target;
            var editables = $(target).parents('tr').find('.editable');

            if (target.value == 'Edit') {
                target.value = 'Save';
            }
            else if (target.value == 'Save') {
                target.value = 'Edit';

                $.ajax({
                    url: '/edit/',
                    type: 'POST',
                    dataType: "html",
                    data: {'book_id': target.dataset.bookId,
                        'new_author': $(editables[0]).find('input').val(),
                        'new_title': $(editables[1]).find('input').val()
                    },
                    success: function (data) {

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
        }
    };
    catalog.init();
});
