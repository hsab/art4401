document.addEventListener("DOMContentLoaded", function () {
    addAnchors()
});
'[id*="cat"]'

function addAnchors() {
    links = $('a').filter(function () {
        return this.id.match(/x\d.*/);
    }).addClass("auto-anchor fas fa-link").click(function () {
        copy(this.id);
    }).html(function(){
        return `<span class="tooltiptext" id="`+this.id+`ttp">Copy to clipboard</span>`
    }).wrap(`<div class='tooltip'></div>`)
}

function copy(selector) {
    var scroll = $(window).scrollTop();
    var $temp = $("<div>");
    $("body").append($temp);
    $temp.attr("contenteditable", true)
        .html('https://' + window.location.host + window.location.pathname + '#' + selector).select()
        .on("focus", function () {
            document.execCommand('selectAll', false, null);
        })
        .focus();
    document.execCommand("copy");
    $temp.remove();
    $("html").scrollTop(scroll);

    var tooltip = $(`#${selector}ttp`);
    tooltip.html("Copied!")
}