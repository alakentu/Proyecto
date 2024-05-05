/*!
  * Vanilla JS Octingenti Framework Script
  * Copyright 2021 Gonzalo R. Meneses A.
  * Licensed under GNU General Public License version 2 or later; see LICENSE.txt
  */
(function () {
    'use strict';
    const anchors = document.getElementsByTagName('a'),
        selects = document.querySelectorAll('select');

    const selectLists = () => {
        for (const select of selects) {
            const options = select.options,
                multiple = select.hasAttribute('multiple')

            select.addEventListener('change', function (ele) {
                if (multiple) {
                    for (var i = 0; i < options.length; i++) {
                        const option = options[i]
                        if (option.selected) {
                            option.setAttribute('selected', 'selected')
                        } else {
                            option.removeAttribute('selected')
                        }
                    }
                } else {
                    for (i = 0; i < options.length; i++) {
                        const option = options[i]
                        Array.prototype.filter.call(option.parentNode.children, function () {
                            if (option.selected) {
                                option.setAttribute('selected', 'selected')
                            } else {
                                option.removeAttribute('selected')
                            }
                        })
                    }
                }
            })
        }
    }

    const checkRadiosCb = () => {
        const allInputs = [...document.querySelectorAll('input')]

        if (allInputs.length > 0) {
            [].forEach.call(allInputs, function (el, i, input) {
                el.addEventListener('click', function () {
                    [].forEach.call(input, function (el) {
                        var type = el.type
                        if (type == 'checkbox') {
                            if (this.checked) {
                                this.checked = true
                                this.setAttribute('checked', 'checked')
                            } else {
                                this.checked = false
                                this.removeAttribute('checked')
                            }
                        } else {
                            if (this.checked) {
                                this.checked = true
                                this.setAttribute('checked', 'checked')
                                if (this.checked !== el.checked) {
                                    el.checked = false
                                    el.removeAttribute('checked')
                                }
                            }
                        }
                    }, this)
                })
            })
        }
    }

    const onBoot = () => {
        for (var i = 0, len = anchors.length; i < len; i++) {
            anchors[i].addEventListener('click', function (e) {
                e.preventDefault()
            });
        }

        // Tooltips and popovers
        if (document.querySelectorAll('[data-bs-toggle="tooltip"]').length) {
            var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
            var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
                return new bootstrap.Tooltip(tooltipTriggerEl)
            })
        }

        if (document.querySelectorAll('[data-bs-toggle="popover"]').length) {
            var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'))
            var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
                return new bootstrap.Popover(popoverTriggerEl)
            })
        }

        if (document.querySelectorAll('toast').length) {
            var toastElList = [].slice.call(document.querySelectorAll('.toast'))
            var toastList = toastElList.map(function (toastEl) {
                return new bootstrap.Toast(toastEl)
            })
        }

        if (document.querySelectorAll("form").length > 0) {
            document.querySelector("form").reset()
        }

        selectLists()
        checkRadiosCb()
    }

    document.addEventListener('DOMContentLoaded', onBoot)
})();

(function ($) {
    var user_lang = navigator.language || navigator.userLanguage;
    $(function () {
        $("#inputDateInit,#inputDateEnd").gmDateTimePicker({
            format: "DD-MM-YYYY",
            lang: user_lang.split('-')[0],
            nowButton: true,
            weekStart: 1,
            time: false,
            clearButton: true
        });

        $('#message').fadeOut(4000, function () {
            $(this).empty();
            $('form[name="record_generator"]')[0].reset();
            $('form[name="record_generator"]').trigger('reset');
            location.href = location.href
        });
    });
})(jQuery);