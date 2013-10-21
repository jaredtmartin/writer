$(function() {
    $('.toggle-text').each(function(i) {
        toggleText($(this), false);
        $(this).click(function() {
            toggleText($(this), true);
        });
    });
});
function toggleText(element,flip) {
    var checked=element.find('input').is(':checked');
    var result= !(flip == checked); // A little bit of Boolean magic    
    element.find('input').attr('checked',result);
    updateToggleText(element, result);
}

function updateToggleText(element, toggled){
    if (toggled){
        element.find('a').css('color',element.attr('toggled-color'));
        element.find('a').html(element.attr('toggled-text'));
    } else {
        element.find('a').css('color',element.attr('untoggled-color'));
        element.find('a').html(element.attr('untoggled-text'));
    }
}
