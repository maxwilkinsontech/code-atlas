/* Highlight any block on code in the template*/
hljs.initHighlightingOnLoad();
var content;
$(".note-content").each(function () {
    content = $(this).html();
    $(this).html(marked(content));
});