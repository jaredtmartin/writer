function showTagModal(article_id, default_value){
    window.article_id = article_id;
    if (article_id == undefined){
        $('#tag-instructions').html('List the tags to be added to the selected articles separated by commas.');
        $('#tag_input').val('');
    } else {
        $('#tag-instructions').html('List the tags for this article separated by commas.');
        $('#tag_input').val(default_value);
    }
    $('#tag-modal').modal('show');
}
function saveTags() {
    $('#tag-modal').modal('hide');
    data="&tags="+$('#tag_input').val();
    if (window.article_id==undefined){
        data+="&append=True"
    }else{
        data+="&append=False"
    }
    doActionOnArticles(window.tag_url, window.article_id, data);
}
function showDeleteModal(article_id){
    window.article_id = article_id;
    if (article_id == undefined){
        $('#delete-prompt-partial').html('the selected articles?');
    } else {
        $('#delete-prompt-partial').html('this article?');
    }
    $('#delete-modal').modal('show');
}
function rejectArticle(url, article_id){
    $('#reject-modal').modal('hide');
<<<<<<< HEAD
    data="&reason="+$('#reject_input').val();
    doActionOnArticles(url, article_id, data);
}
function assignArticles(url, writer, article_id){
    data="&user="+writer;
=======
    data = "&reason=" + $('#reject_input').val();
    doActionOnArticles(url, article_id, data);
}
function assignArticles(url, writer, article_id){
    data = "&user=" + writer;
>>>>>>> 2bc770fb80b8f1145abaafcb30ba4f80e0f36d9c
    doActionOnArticles(url, article_id, data);
}
function doActionOnArticles(url, article_id, extra){
    if (article_id == undefined){
<<<<<<< HEAD
        data=$('#actions-form').serialize();
    } else {
        data="action-select="+String(article_id);
        // data+="&select-across="+$('#select-across').val();
    }
    data+="&as_row="+'True';
    if (extra!=undefined){data+=extra}
    jQuery.post(url, data, success=ajaxUpdateRow);
=======
        data = $('#actions-form').serialize();
    } else {
        data = "action-select=" + String(article_id);
        // data+="&select-across="+$('#select-across').val();
    }
    data += "&as_row=" + 'True';
    if (extra != undefined){data += extra}
    jQuery.post(url, data, success = ajaxUpdateRow);
>>>>>>> 2bc770fb80b8f1145abaafcb30ba4f80e0f36d9c
}