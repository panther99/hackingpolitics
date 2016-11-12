$(document).ready(function(){
	var condition2=true;
	var condition3=false;
	var condition4=false;
	var condition6=true;
	var condition7=false;
	var condition8=false;
	var condition10=true;
	var condition11=false;
	var condition12=false;
	var condition14=true;
	var condition15=false;
	var condition16=false;
	var audio1 = document.createElement('audio');
		audio1.setAttribute('src', 'sound1.mp3');
	var audio2 = document.createElement('audio');
		audio2.setAttribute('src', 'sound2.mp3');
	var audio3 = document.createElement('audio');
		audio3.setAttribute('src', 'sound3.mp3');
	
		$('#1').hide();
		$('#1').fadeIn(1200);
		$('#2').hide();
		$('#3').hide();
		$('#4').hide();
		$('#5').hide();
		$('#5').fadeIn(1200);
		$('#6').hide();
		$('#7').hide();
		$('#8').hide();
		$('#9').hide();
		$('#9').fadeIn(1200);
		$('#10').hide();
		$('#11').hide();
		$('#12').hide();
		$('#13').hide();
		$('#13').fadeIn(1200);
		$('#14').hide();
		$('#15').hide();
		$('#16').hide();
	
	$('#strip1').on('click',function(){
	
	if(condition2==true) {
				$('#2').fadeIn(1200);
				condition2=false;
				condition3=true;
	}
	else if(condition3==true) {
			$('#3').fadeIn(1200);
				condition3=false;
				condition4=true;
	}
	else if(condition4==true) {
			$('#4').fadeIn(1200);
			condition4=false;
	}
	});

 
	
	$('#strip2').on('click',function(){
	
	if(condition6==true) {
				$('#6').fadeIn(1200);
				condition6=false;
				condition7=true;
	}
	else if(condition7==true) {
			$('#7').fadeIn(1200);
				condition7=false;
				condition8=true;
	}
	else if(condition8==true) {
			$('#8').fadeIn(1200);
			condition8=false;
	}
	});
	
	
		$('#strip3').on('click',function(){
	
	if(condition10==true) {
				$('#10').fadeIn(1200);
				condition10=false;
				condition11=true;
	}
	else if(condition11==true) {
			$('#11').fadeIn(1200);
				condition11=false;
				condition12=true;
	}
	else if(condition12==true) {
			$('#12').fadeIn(1200);
			condition12=false;
	}
	});
	
	
		$('#strip4').on('click',function(){
	
	if(condition14==true) {
				$('#14').fadeIn(1200);
				condition14=false;
				condition15=true;
	}
	else if(condition15==true) {
			$('#15').fadeIn(1200);
				condition15=false;
				condition16=true;
	}
	else if(condition16==true) {
			$('#16').fadeIn(1200);
			condition16=false;
	}
	});
	});