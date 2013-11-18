jQuery(function ($) {
    var catalog = {
        init:function () {
            catalog.cacheElements();
            catalog.bindEvents();
        },

        cacheElements:function () {
            catalog.$selectAllCheckbox = $('#id-select-all-checkbox')
            catalog.$checkboxes = $('.book-table-checkbox');
        },

        bindEvents:function () {
            catalog.$selectAllCheckbox.on('change', catalog.changeCheckboxes);
        },

        changeCheckboxes:function () {
            catalog.$checkboxes.prop('checked', $(this).is(':checked'));
        }
    }
    catalog.init();
});