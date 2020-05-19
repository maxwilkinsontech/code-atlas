/* Highlight any block on code in the template*/
hljs.initHighlightingOnLoad();
var content;
$(".note-content").each(function () {
    content = $(this).html();
    // Escape code blocks.
    tokens = marked.lexer(content);
    tokens.forEach(function (token) {
        if (token.type === "code") {
            token.escaped = true;
        }
    });

    parsed = marked.parser(tokens);
    $(this).html(parsed);
});