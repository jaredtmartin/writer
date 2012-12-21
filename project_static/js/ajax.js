function ajaxUpdateRow(data){
    $('.message').remove();                                                             // Remove old messages
//    object_id=jQuery("#last_id").val();                                               // Get last transaction id
    $('#ajax-data').replaceWith('<div id="ajax-data" style="display: none;"></div>');   // Clear temp data cache
    var d = $('#ajax-data').append(data);                                               // Add new data to cache
    $('.message', d).appendTo($('#messages')) //.hide().slideDown('slow');              // Add new messages
    results=$('tr', d);                                                                 // Get list of items with given class
    results.each(function(i){                                                           // Go through each one
        if ($('#'+this.id+":visible").length>0){                                        // See if the item already exists on the page
            $('#'+this.id+":visible:first").replaceWith(this);                          // Replace it
        } else {
            $('#'+$(this).attr('id').split('-')+'s').prepend(this);                     // Otherwise add it to the top of the list
        }
    });
    for (x in window.codeForRows){
        codeForRows[x]();
    }
}
