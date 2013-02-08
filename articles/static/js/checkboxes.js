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
    if ($(window.row_selector+' :checked').length>0){$('#action_bar').slideDown();}
    else {$('#action_bar').slideUp();}
}
function updateMasterCheckbox(){
    if ($(window.row_selector+' :checked').length==0){$('#checkall').prop("checked", false);}
    if ($(window.row_selector+' :checkbox:not(:checked)').length==0){$('#checkall').prop("checked", true);}
}
function toggleMaster(){
    if($('#checkall').prop("checked")) {selectRows($(window.row_selector))}
    else {deselectRows($(window.row_selector))}
}


//	function showsact(str3)
//	{
//		var newrow="action_" + str3;
//		document.getElementById(str3).style.display = "block";
//		document.getElementById(newrow).style.display = "block";
//	}
//	
//	function hidesact(str2)
//	{
//		var newrow="action_" + str2;
//		document.getElementById(str2).style.display = "none";
//		document.getElementById(newrow).style.display = "none";
//	}
