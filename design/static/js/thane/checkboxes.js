
function toggleRows(rows){
    rows.toggleClass('selected-row');
    showOrHideActionBar();
    updateMasterCheckbox();
}
function selectRows(rows){
    // This highlights the rows
    rows.addClass('selected-row');
    // This is necisary for when we click on the master checkbox at the top
    // This checks the actual checkbox
    rows.find(':checkbox').prop("checked", "checked"); 
    // This checks FlatUI's checkbox
    rows.find('label.checkbox').addClass('checked');

    showOrHideActionBar();
}
function deselectRows(rows){
    rows.removeClass('selected-row');
    // This is necisary for when we click on the master checkbox at the top
    rows.find(':checkbox').prop("checked", false); 
    showOrHideActionBar();
    // This checks FlatUI's checkbox
    rows.find('label.checkbox').removeClass('checked');
}
function showOrHideActionBar(){
    // if ($(window.row_selector+' :checked').length>0){$('#action_bar').show();}
    // else {$('#action_bar').hide();}
    if ($(window.row_selector+' :checked').length>0){$('.multiaction').show();}
    else {$('.multiaction').hide();}
}
function updateMasterCheckbox(){
    value=($(window.row_selector+' :checkbox:not(:checked)').length==0);
    $('#checkall').prop("checked", value);
    if(value){
        $('#checkall').parent().addClass("checked");
    }else{
        $('#checkall').parent().removeClass("checked");
    }
    checkHidden(value);
}
function checkHidden(value){
    if (value){
        $('#select-across').val('1');
    }else{
        $('#select-across').val('0');
    }
}
function toggleMaster(){
    if($('#checkall').prop("checked")) {
        selectRows($(window.row_selector));
        checkHidden(true);
    }
    else {
        deselectRows($(window.row_selector)); 
        checkHidden(false);
    }
}
