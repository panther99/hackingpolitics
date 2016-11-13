$(document).ready(function(){
		$('#1').hide();
		$('#2').hide();
		$('#3').hide();
		$('#4').hide();	
		$('#5').hide();
		$('#6').hide();	
		$('#7').hide();
		$('#8').hide();			
/*var myVar = setInterval(myTimer, 1000);//tajmer koji se odvija svake sekunde(postavi na 2 sekunde kasnije)
function myTimer() {
	//start <---
    br=br+1; //brojac se uvecava svake sekunde, ako je prva sekunda, brojac je jedan, ako je druga sekunda dva itd.
	if(br=1) //ako je prva sekunda onda
	{
		//fade in first picture
	}
	if(br=2) //ako je druga sekunda onda
	{
		//fade in second picture
	}
	//...	
	if(br=9)
	{
		//break from timer(da ne bi bilo bagova)
	}
	//end <--- */
});
window.onload = startInterval();
var br=0;
function startInterval() {
var myVar = setInterval(pojava,2000);
}

function pojava() {
	br=br+1;
		if(br==1) {
		$('#1').fadeIn(1000);
	}
		else if(br==2) {
		$('#2').fadeIn(1000);
	}
		else if(br==3) {
		$('#3').fadeIn(1000);
	}
		else if(br==4) {
		$('#4').fadeIn(1000);
	}
		else if(br==5) {
		$('#5').fadeIn(1000);
	}
		else if(br==6) {
		$('#6').fadeIn(1000);
	}
		else if(br==7) {
		$('#7').fadeIn(1000);
	}
		else if(br==8) {
		$('#8').fadeIn(1000);
	}
	else if(br==9) {
		stop();
	}
}

 function stop() {
	 clearInterval(myVar);
 }
   // jQuery methods go here...

//Tajmer se ovako pise, a ovo izmedju "start" i "end" unutar tajmera nisam siguran ali po toj logici sam mislio da se radi