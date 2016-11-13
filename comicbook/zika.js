$(document).ready(function(){	
document.getElementById("1").style.opacity = "0";
document.getElementById("2").style.opacity = "0";
document.getElementById("3").style.opacity = "0";
document.getElementById("4").style.opacity = "0";
document.getElementById("5").style.opacity = "0";
document.getElementById("6").style.opacity = "0";
document.getElementById("7").style.opacity = "0";
document.getElementById("8").style.opacity = "0";
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
var myVar = setInterval(pojava,350);
}

function pojava() {
	br=br+1;
		if(br==1) {
		document.getElementById("1").style.opacity = "1";	
	}
		else if(br==2) {
		document.getElementById("2").style.opacity = "1";
	}
		else if(br==3) {
		document.getElementById("3").style.opacity = "1";
	}
		else if(br==4) {
		document.getElementById("4").style.opacity = "1";
	}
		else if(br==5) {
		document.getElementById("8").style.opacity = "1";
	}
		else if(br==6) {
		document.getElementById("7").style.opacity = "1";
	}
		else if(br==7) {
		document.getElementById("6").style.opacity = "1";
	}
		else if(br==8) {
		document.getElementById("5").style.opacity = "1";
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


	/* When the user clicks on the button, 
toggle between hiding and showing the dropdown content */
function myFunction() {
    document.getElementById("myDropdown").classList.toggle("show");
}

// Close the dropdown menu if the user clicks outside of it
window.onclick = function(event) {
  if (!event.target.matches('.dropbtn')) {

    var dropdowns = document.getElementsByClassName("dropdown-content");
    var i;
    for (i = 0; i < dropdowns.length; i++) {
      var openDropdown = dropdowns[i];
      if (openDropdown.classList.contains('show')) {
        openDropdown.classList.remove('show');
      }
    }
  }
}