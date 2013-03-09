function checkallTheBox()
	{
		if(document.actions-form["checkall"].checked)
		{
			//alert("nowchecked");
			checkAllBoxes();
			var acdiv = document.getElementById('topactionbar');
			acdiv.style.display='block';
			for (var i=0; i < 10; i++)
			{
				document.actions-form["checkboxes[]"][i].checked;
				var idnumber = i+1;
				var maketr = "rw" + idnumber;
				//alert(maketr);
				document.getElementById(maketr).style.background = "#0072C6";
				document.getElementById(maketr).style.color = "#FFFFFF";
			}
			
		}
		else
		{
			//alert("checkedoff");
			uncheckcheckAllBoxes();
			var acdiv = document.getElementById('topactionbar');
			acdiv.style.display='none';
			for (var i=0; i < 10; i++)
			{
				document.actions-form["checkboxes[]"][i].checked;
				var idnumber = i+1;
				var maketr = "rw" + idnumber;
				//alert(maketr);
				document.getElementById(maketr).style.background = "";
				document.getElementById(maketr).style.color = "#000000";
			}
		}
	}
	
	function checkBoxes()
	{
		var flag = 0;
		var acdiv = document.getElementById('topactionbar');
		for (var i=0; i < 10; i++)
		{
			if(document.actions-form["checkboxes[]"][i].checked)
			{
				document.actions-form["checkboxes[]"][i].checked;
				var idnumber = i+1;
				var maketr = "rw" + idnumber;
				//alert(maketr);
				document.getElementById(maketr).style.background = "#0072C6";
				document.getElementById(maketr).style.color = "#FFFFFF";
				flag ++;
			}
			else
			{
				var idnumber = i+1;
				var maketr = "rw" + idnumber;
				document.getElementById(maketr).style.background = "";
				document.getElementById(maketr).style.color = "#000000";
			}
		}
		if (flag > 0){ acdiv.style.display='block'; }
		if (flag==0){ 
		    document.actions-form["checkall"].checked = false; 
		    acdiv.style.display='none';
		}
	}
	
	function checkAllBoxes()
	{
		for (var i=0; i < 10; i++)
		{
			document.actions-form["checkboxes[]"][i].checked=true;
		}	
	}
	
	function uncheckcheckAllBoxes()
	{
		for (var i=0; i < 10; i++)
		{
			document.actions-form["checkboxes[]"][i].checked=false;
		}
	}

	function onbox(str2)
	{ checkthis(str2); }
	
	function checkthis(str)
	{
		if(document.getElementById(str).checked)
		{ document.getElementById(str).checked=false; }
		else
		{ document.getElementById(str).checked=true; }
	}
	
	function showsact(str3)
	{
		var newrow="action_" + str3;
		document.getElementById(str3).style.display = "block";
		document.getElementById(newrow).style.display = "block";
	}
	
	function hidesact(str2)
	{
		var newrow="action_" + str2;
		document.getElementById(str2).style.display = "none";
		document.getElementById(newrow).style.display = "none";
	}
