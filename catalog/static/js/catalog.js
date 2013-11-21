"use strict";

jQuery(function ($) {
    var catalog = {
        init: function () {
            catalog.cacheElements();
            catalog.bindEvents();
            catalog.setupCSRFProtection();
        },

        cacheElements: function () {
            catalog.$selectAllCheckbox = $('#id-all-checkbox');
            catalog.$checkboxes = $('.book-table-checkbox');
            catalog.$selectAllAuthorsCheckbox = $('#id-all-authors-checkbox');
            catalog.$authorCheckboxes = $('.author-table-checkbox');
            catalog.$editButton = $('.edit-button');
            catalog.$editAuthorButton = $('.edit-author-button');
            catalog.$editBox = $('.editable input');
            catalog.$addAuthorPlus = $('#id-add-author');
            catalog.$authorsList = $('#authors');
        },

        bindEvents: function () {
            catalog.$selectAllCheckbox.on('change', catalog.changeCheckboxes);
            catalog.$selectAllAuthorsCheckbox.on('change', catalog.changeAuthorCheckboxes);
            catalog.$editButton.on('click', catalog.editBook);
            catalog.$editAuthorButton.on('click', catalog.editAuthor);
            catalog.$editBox.on('keypress', catalog.editSubmit);
            catalog.$addAuthorPlus.on('click', catalog.addAuthorField);
        },

        setupCSRFProtection: function () {
            var csrftoken = $('meta[name=csrf-token]').attr('content')

            $.ajaxSetup({
                beforeSend: function(xhr, settings) {
                    if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type))
                        xhr.setRequestHeader("X-CSRFToken", csrftoken)
                }
            })
        },

        changeCheckboxes: function () {
            catalog.$checkboxes.prop('checked', $(this).is(':checked'));
        },

        changeAuthorCheckboxes: function () {
            catalog.$authorCheckboxes.prop('checked', $(this).is(':checked'));
        },

        editBook: function () {
            var editables = $(this).parents('tr').find('.editable');
            if (this.value == 'Edit') {
                this.value = 'Save';
            }
            else if (this.value == 'Save') {
                this.value = 'Edit';
                // save only if book title is not empty
                if ($(editables[1]).find('input').val().trim() != '') {
                    var data = {
                        'title': $(editables[1]).find('input').val()
                    };
                    var names = $(editables[0]).find('input').val().split(',');
                    for (var i in names) {
                        if (names[i].trim())
                            data['authors-'+i] = names[i].trim();
                    }

                    $.ajax({
                        url: '/edit/' + this.dataset.bookId + '/',
                        type: 'POST',
                        dataType: "json",
                        data: data,
                        success: function (data) {
                            // refresh author and title on page
                            $(editables[0]).find('span').text(data['authors']);
                            $(editables[1]).find('span').text(data['title']);
                        },
                        error: function (data) {
                            alert(data.statusText);
                        }
                    });
                }
            }

            for (var i = 0; i < editables.length; i++) {
                $(editables[i]).find('input').toggle();
                $(editables[i]).find('span').toggle();
            }
        },

        editAuthor: function() {
            var editable = $(this).parents('tr').find('.editable');
            if ($(this).val() == 'Edit') {
                this.value = 'Save';
            }

            else if ($(this).val() == 'Save') {
                this.value = 'Edit';
                // save only if author name is not empty
                if ($(editable).find('input').val().trim() != '') {
                    var data = {
                        'author_id': this.dataset.authorId,
                        'name': $(editable).find('input').val()
                    };

                    $.ajax({
                        url: '/authors/',
                        type: 'POST',
                        dataType: "json",
                        data: data,
                        success: function (data) {
                            // refresh author name on page
                            $(editable).find('span').text(data['name']);
                        },
                        error: function (data) {
                            alert(data.statusText);
                        }
                    });
                }
            }
            $(editable).find('input').toggle();
            $(editable).find('span').toggle();
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
