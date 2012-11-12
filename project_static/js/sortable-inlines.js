$(function() {
    $( ".inline" ).sortable({
        update: function() {
            $(this).find('div.inlineform').each(function(i) {
                if ($(this).find('input[id$=name]').val()) {
                    $(this).find('input[id$=order]').val(i+1);
                }
            });
        }
    });
});
