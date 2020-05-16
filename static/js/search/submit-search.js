$(function () {
    $('#search-form').each(function () {
        $(this).find('input').keypress(function (e) {
            // Enter pressed?
            if (e.which == 10 || e.which == 13) {
                this.form.submit();
            }
        });
        $(this).find('input[type=submit]').hide();
    });
});