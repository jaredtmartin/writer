function updateOrder(event, ui){
    $(this).find('div.inlineform').each(function(i) {
        if ($(this).find('input[id$=name]').val()) {
            $(this).find('input[id$=order]').val(i+1);
        }
    });
}
function replaceToolbarElement(event, ui){
//    ui.item.clone().prependTo('.toolbar-elements');
    item=$('.inline .toolbar-element');
    new_id_number=$('#id_elements-TOTAL_FORMS').val();
    item.find('input, select').each(function(){
        if ($(this).attr("id")){
            $(this).attr('id', "id_elements-".concat(new_id_number, "-", $(this).attr('id').substr(3)));
            $(this).attr('name', "elements-".concat(new_id_number, "-", $(this).attr('name')));
        }        
    });
    new_id_number=$('#id_elements-TOTAL_FORMS').val(parseInt(new_id_number)+1);
    item.replaceWith(item.find(".inlineform"));
    updateOrder();
}
$(function() {
    $( ".inline" ).sortable({
        revert: true,
//        connectWith: $(".connected-trash"),
        update: updateOrder,
        receive:replaceToolbarElement,
    }).draggable({
        connectToSortable: "#trash-can",
//        snap: true,
        revert: false
    });
    $("#trash-can").droppable({
//        hoverClass: "droppable-hover",
        drop: function(event, ui) {
            var element = ui.draggable.css('position', '');
            $(this).append(element);
            $(ui.draggable).hide();
            $(ui.draggable).find('input[name$="DELETE"]').attr('checked',true)
        }
    });
    $(".toolbar-element").draggable({
        connectToSortable: ".inline",
        helper: "clone",
        revert: false,
//        remove:replaceToolbarElement,
    });
    $("ul, li").disableSelection();
//    $( ".toolbar-elements" ).sortable({
//        connectWith: $(".inline"),
//        remove:replaceToolbarElement,
//    });
//    $( ".toolbar-elements" ).disableSelection();
});

//=====================================================================

//$(function() {
//    $("#sortable, #sortable2").sortable({
//        revert: true,
//        update: function(event, ui) {
//            var basketItems = $(this).sortable('toArray').toString();
//            $.jnotify(basketItems, 5000);
//        }
//    }).draggable({
//        connectToSortable: "#trash-can",
//        snap: true,
//        revert: false
//    });
//    $("#trash-can").droppable({
//        hoverClass: "droppable-hover",
//        drop: function(event, ui) {
//            var element = ui.draggable.css('position', '');
//            $(this).append(element);
//            $(ui.draggable).fadeOut(1000);
//        }
//    });

//    $(".draggable").draggable({
//        connectToSortable: "#sortable, #sortable2",
//        helper: "clone",
//        revert: false
//    });
//    $("ul, li").disableSelection();
//});
