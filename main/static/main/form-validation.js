(function () {
    'use strict';

    var INVALID_CLASS = 'form-field-invalid';

    function clearInvalid(form) {
        form.querySelectorAll('.' + INVALID_CLASS).forEach(function (el) {
            el.classList.remove(INVALID_CLASS);
        });
    }

    function markInvalid(el) {
        if (el) el.classList.add(INVALID_CLASS);
    }

    function isFieldEmpty(field) {
        if (field.disabled || field.type === 'hidden') return false;
        if (field.type === 'checkbox') return !field.checked;
        if (field.type === 'file') {
            return !field.files || field.files.length === 0;
        }
        if (field.tagName === 'SELECT') return !String(field.value || '').trim();
        if (field.tagName === 'TEXTAREA') return !String(field.value || '').trim();
        if (field.type === 'password' || field.type === 'text' || field.type === 'tel' || field.type === 'email' || field.type === 'search' || field.type === 'url') {
            return !String(field.value || '').trim();
        }
        return false;
    }

    function collectFields(form) {
        var required = Array.prototype.slice.call(form.querySelectorAll('[required]'));
        if (required.length) return required;

        if (form.closest('.admin-login-card')) {
            return Array.prototype.slice.call(
                form.querySelectorAll('input[name="username"], input[name="password"]')
            );
        }

        return [];
    }

    function validateForm(form) {
        clearInvalid(form);
        var fields = collectFields(form);
        var ok = true;

        fields.forEach(function (field) {
            if (isFieldEmpty(field)) {
                ok = false;
                markInvalid(field);
            }
        });

        return ok;
    }

    function onFieldChange(e) {
        var t = e.target;
        if (!t || !t.closest) return;
        if (!t.matches('input, textarea, select')) return;
        t.classList.remove(INVALID_CLASS);
    }

    function initForm(form) {
        form.setAttribute('novalidate', '');
        form.addEventListener('submit', function (e) {
            if (!validateForm(form)) e.preventDefault();
        });
        form.addEventListener('input', onFieldChange, true);
        form.addEventListener('change', onFieldChange, true);
    }

    function init() {
        document.querySelectorAll('form').forEach(initForm);
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
