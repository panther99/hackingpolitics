$(document).ready(function(){

	var truth=false;
	var audio1 = document.createElement('audio');
	audio1.setAttribute('src','sound1.mp3');
	
	var condition1=false;
	var condition2=false;
	var condition3=false;
	var condition4=false;
	
        $('#prva').hide();
		$('#prva').fadeIn(2700);
		$('#druga').hide();
		$('#treca').hide();
		$('#cetvrta').hide();
		
		
		$(document).keydown(function(e) {
			if(e.which > 0) {
				$('#druga').fadeIn(2700);
				truth=true;
			}
			if(truth==true) {
		$(document).keydown(function(e) {
			if(e.which > 0) {
				$('#treca').fadeIn(2700);
				truth=false;
			}
		}); }
	});
		
		
}); 