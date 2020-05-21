$(document).ready(function () {
    // var csrfToken = Cookies.get('crsftoken');
    var csrfToken = $('input[name=csrfmiddlewaretoken]').val();
    var numChecked = 0;
    // Update numNotesSelected text
    function updateNumNotesSelectedText() {
        var numNotesSelected = $('#numNotesSelected');
        var text = (numChecked == 1) ? ' Note Selected' : ' Notes Selected'
        numNotesSelected.html(numChecked + text);
    }
    // Return dictionary of ids of selected Notes
    function getSelectedIds() {
        var numNotesSelected = document.querySelectorAll('.custom-control-input');
        var ids = { ids: [] };
        var id;

        numNotesSelected.forEach(note => {
            id = note.id;
            if (id != 'checkAll' && note.checked) {
                ids['ids'].push(id);
            }
        });
        return ids;
    }

    function postData(url, data) {
        $.ajax({
            traditional: true,
            url: url,
            type: 'POST',
            data: data,
            beforeSend: function (xhr, settings) {
                xhr.setRequestHeader("X-CSRFToken", csrfToken);
            },
            success: function (data) {
                window.location.reload();
            }
        });
    }
    // Toggle all inputs
    $('#checkAll').on('input', function () {
        var checked = $(this).is(":checked");
        var allCheckBoxes = $('.custom-control-input');

        if (checked) {
            allCheckBoxes.prop('checked', true);
            numChecked = allCheckBoxes.length - 1;
        } else {
            allCheckBoxes.prop('checked', false);
            numChecked = 0;
        }
        updateNumNotesSelectedText()
    });
    // Toggle individual input
    $('.custom-control-input').on('input', function () {
        var id = $(this).attr('id');
        var checked = $(this).is(":checked");

        if (id != 'checkAll') {
            if (checked) {
                numChecked += 1;
            } else {
                numChecked -= 1;
            }
        }
        updateNumNotesSelectedText()
    });

    $('#actionsSelect').on('change', function () {
        var value = this.value;
        if (numChecked > 0) {
            var data = getSelectedIds();
            var url;

            if (value == 'public') {
                if (confirm('Are you sure you want to make the selected Notes public?')) {
                    url = '/notes/api/public/';
                }
            } else if (value == 'private') {
                if (confirm('Are you sure you want to make the selected Notes private?')) {
                    url = '/notes/api/private/';
                }
            } else if (value == 'tag') {
                var tags = prompt('Enter the tags you want to add to the selected Notes.');
                if (tags != null) {
                    data['tags'] = tags;
                }
                url = '/notes/api/tags/';
            } else if (value == 'delete') {
                if (confirm('Are you sure that you want to delete the selected Notes? This cannot be undone.')) {
                    url = '/notes/api/delete/';

                }
            } else {
                return;
            }
            postData(url, data);
        }
    });
    $('#orderingSelect').on('change', function () {
        var value = this.value;
        var url = '/notes/mode/edit/?ordering='

        if (value == '1') {
            url += 'date_created';
        } else if (value == '2') {
            url += '-date_created';
        } else if (value == '3') {
            url += 'last_edited';
        } else if (value == '4') {
            url += '-last_edited';
        } else if (value == '5') {
            url += 'title';
        } else if (value == '6') {
            url += '-title';
        } else if (value == '7') {
            url += 'public';
        } else if (value == '8') {
            url += 'private';
        } else {
            return;
        }
        window.location.replace(url);
    });
});