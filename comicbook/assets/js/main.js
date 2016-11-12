$(document).ready(function(){
	
	var condition2=true;
	var condition3=false;
	var condition4=false;
	
		$('#jedan').hide();
		$('#jedan').fadeIn(1200);
		$('#dva').hide();
		$('#tri').hide();
		$('#cetri').hide();
		
	
	$('#strip1').on('click',function(){
	
	if(condition2==true) {
				$('#dva').fadeIn(1200);
				condition2=false;
				condition3=true;
	}
	else if(condition3==true) {
			$('#tri').fadeIn(1200);
				condition3=false;
				condition4=true;
	}
	else if(condition4==true) {
			$('#cetri').fadeIn(1200);
			condition4=false;
	}
	});

}); 