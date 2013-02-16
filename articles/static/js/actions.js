function saveTags() {
    $('#tag-modal').modal('hide');
    $.ajax({
        url: window.ajax_url,
        type:'POST',
        data:{
            _tags: $('#tag_input').val(),
            as_row:'True',
        },
        success: ajaxUpdateRow
    });
}
// function updateTags(data){
//     $('#tag-cell-'+window.last_id).html(data);
// }
function rejectArticle() {
    $('#reject-modal').modal('hide');
    $.ajax({
        url: window.ajax_url,
        type:'POST',
        data:{
            reason: $('#reject_input').val(),
            as_row:'True',
        },
        success: ajaxUpdateRow
    });
}