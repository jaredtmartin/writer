function saveTags() {
    parent.$.fancybox.close();
    $.ajax({
        url: window.ajax_url,
        type:'POST',
        data:{
            _tags: $('#tag_input').val(),
        },
        success: updateTags
    });
    $('#tag-modal').modal('hide');
}
function updateTags(data){
    $('#tag-cell-'+window.last_id).html(data);
}
function rejectArticle() {
    parent.$.fancybox.close();
    $.ajax({
        url: window.ajax_url,
        type:'POST',
        data:{
            _tags: $('#reject_input').val(),
        },
        success: updateTags
    });
    $('#tag-modal').modal('hide');
}