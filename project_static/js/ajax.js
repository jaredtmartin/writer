function saveDataInCache(data){
    $('#ajax-data').replaceWith('<div id="ajax-data" style="display: none;"></div>');   // Clear temp data cache
    return $('#ajax-data').append(data);                                               // Add new data to cache
}
function updateMessages(data){
    $('.message').remove();
    $('.message', d).appendTo($('#messages'))
}
function addRows(data){
    results=$('tr', data);                                                                 // Get list of items with given class
    results.each(function(i){                                                           // Go through each one
        obj_cls=$(this).attr('id').split('-')[0];
        if ($('#'+this.id+":visible").length>0){                                        // See if the item already exists on the page
            $('#'+this.id+":visible:first").replaceWith(this);                          // Replace it
        } else {
            $('#'+obj_cls+'s').append(this);                     // Otherwise add it to the top of the list
        }
    });
}
function runCode(){
    for (x in window.codeForRows){
        codeForRows[x]();
    }
}
function ajaxUpdateRow(data){                                               // Get last transaction id
    d=saveDataInCache(data);
    updateMessages(d);                                                                  // Add new messages
    addRows(d);
    runCode();
}
function sendAjaxPost(url, data){
    jQuery.post(url, data, success=ajaxUpdateRow);
}
function removeDeletedRows(data){
    results=$('.deleted', data);
    results.each(function(i){
        elmt_id=$(this).attr('code-delete-id');
        $('#'+elmt_id).remove();
    });
}