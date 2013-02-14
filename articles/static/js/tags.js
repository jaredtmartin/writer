function saveTags(url) {
    parent.$.fancybox.close();
    $.ajax({
        url: url,
        type:'POST',
        data:{
            _tags: $('#tag_input').val(),
        },
        success: updateTags
    });
    hidePopover();
}
function updateTags(data){
    $('#tag-cell').html(data);
}
function hidePopover(){
    $('.action-popover').popover('hide');
}