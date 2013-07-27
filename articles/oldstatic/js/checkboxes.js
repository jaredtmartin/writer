
function toggleRows(rows){
    rows.toggleClass('selected-row');
    showOrHideActionBar();
    updateMasterCheckbox();
}
function selectRows(rows){
    rows.addClass('selected-row');
    // This is necisary for when we click on the master checkbox at the top
    rows.find(':checkbox').prop("checked", true); 
    showOrHideActionBar();
}
function deselectRows(rows){
    rows.removeClass('selected-row');
    // This is necisary for when we click on the master checkbox at the top
    rows.find(':checkbox').prop("checked", false); 
    showOrHideActionBar();
}
function showOrHideActionBar(){
    if ($(window.row_selector+' :checked').length>0){$('#action_bar').show();}
    else {$('#action_bar').hide();}
}
function updateMasterCheckbox(){
    value=($(window.row_selector+' :checkbox:not(:checked)').length==0);
    $('#checkall').prop("checked", value);
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
