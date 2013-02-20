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
function doSimpleActionOnVarious(action){
    data = $('#actions-form').serialize();
    $(data).push({ action: action, as_row:'True' });
    $.ajax({
        url: window.ajax_url,
        type:'POST',
        data:data,
        success: ajaxUpdateRow
    });
}
function assignArticles(url, writer, article_id){
    if (article_id == undefined){
        data=$('#actions-form').serialize();
    } else {
        data="action-select="+String(article_id);
    }
    data+="&user="+writer
    data+="&as_row="+'True'

    // $(data).push({assign_to_user:writer, as_row:'True' });
    jQuery.post(url, data, success=ajaxUpdateRow);
}