/* Make call to API to get public Notes matching query */

$(document).ready(function () {
    var csrfToken = Cookies.get('crsftoken');
    var resultDiv = $('#publicNotesResults');
    var notesHTML = '';

    function getSearchPath() {
        const urlParams = new URLSearchParams(window.location.search);
        var basePath = '/search/api/';
        var query = urlParams.get('q');
        var path = basePath + '?q=' + query;
        return path
    }

    $.ajax({
        url: getSearchPath(),
        type: 'GET',
        beforeSend: function (xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", csrfToken);
        },
        success: function (data) {
            var results = data['results'];
            for (var i = 0; i < results.length; i++) {
                // Add "Show more results button"
                if (i == 6) {
                    notesHTML += `<button class="btn btn-primary mx-auto my-2" onclick="$('#moreResultsPublicButton').hide();" data-toggle="collapse" id="moreResultsPublicButton" href="#morePublicResults" role="button" aria-expanded="false">
                                    Show more results</button><div class="collapse row" id="morePublicResults">`;
                }
                // Create Note card.
                notesHTML += `<div class="col-sm-12 col-md-6 col-lg-4 my-2">
                                <a href="/notes/view/${results[i]['id']}/" class="card card-body hover-box-shadow p-4 h-100">
                                    <h4>${results[i]['title']}</h4>
                                    <div style="height: 250px; overflow: hidden;" class="note-content">${results[i]['content']}</div>
                                </a>
                              </div>`;
                // Close hidden div.
                if (i == results.length - 1) {
                    notesHTML += '</div>';
                }
            }
            if (results.length == 0) {
                resultDiv.html('<div class="ml-3">No public Notes matching your query.</div>');
            } else {
                resultDiv.html(notesHTML);
            }
        }
    });
});

