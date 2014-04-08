'use strict';

(function() {
    function canocalize(input) {
        return input.replace(/ /g, '-').replace(/[^a-zA-Z0-9-]/g, '').toLowerCase();
    }

    var titleElement = document.getElementById('title');
    var linkTextElement = document.getElementById('link_text');
    titleElement.onkeyup = function() {
        linkTextElement.value = canocalize(titleElement.value);
    };
    titleElement.onblur = titleElement.onkeyup;
})();
