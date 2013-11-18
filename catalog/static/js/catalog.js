jQuery(function ($) {
    var catalog = {
        init: function () {
            catalog.cacheElements();
            catalog.bindEvents();
        },

        cacheElements: function () {
            catalog.$selectAllCheckbox = $('#id-select-all-checkbox')
            catalog.$checkboxes = $('.book-table-checkbox');
            catalog.$editButton = $('.edit-button');
        },

        bindEvents: function () {
            catalog.$selectAllCheckbox.on('change', catalog.changeCheckboxes);
            catalog.$editButton.on('click', catalog.startEditBook);
        },

        changeCheckboxes: function () {
            catalog.$checkboxes.prop('checked', $(this).is(':checked'));
        },

        startEditBook: function (event) {
            var target = event.target;
            var editables = $(target).parents('tr').find('.editable');

            if (target.value == 'Edit') {
                target.value = 'Save';
            }
            else if (target.value == 'Save') {
                target.value = 'Edit';
            }

            for (var i=0; i<editables.length; i++) {
                $(editables[i]).find('input').toggleClass('hidden');
                $(editables[i]).find('span').toggleClass('hidden');
            }
            $(target).toggleClass('edit-button');
            $(target).toggleClass('save-button');
        }
    }
    catalog.init();
});