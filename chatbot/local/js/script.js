$(document).ready( function() {

	$("#prikazi1").click( function() {
		$.each($(".poslanik-card"), function() {
			$(".poslanik-card").addClass("hidden");
		});
		$("#govor1").removeClass("hidden");
	});

	$("#prikazi2").click( function() {
		$.each($(".poslanik-card"), function() {
			$(".poslanik-card").addClass("hidden");
		});
		$("#govor2").removeClass("hidden");
	});

});