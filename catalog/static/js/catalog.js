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
//            catalog.$switchTab = $('#id-switch-tab');
        },

        bindEvents: function () {
            catalog.$selectAllCheckbox.on('change', catalog.changeCheckboxes);
            catalog.$editButton.on('click', catalog.editBook);
//            catalog.$switchTab.on('click', catalog.switchEditTab);
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
                    dataType: "html",
                    data: {'book_id': this.dataset.bookId,
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
        },

//        switchEditTab: function (event) {
//            $(this).tab('show');
//        }
    };
    catalog.init();
});
