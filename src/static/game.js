function getPlayerBalls() {
	// TODO: HTTP GET here	
	// TODO: some jQuery effect to identify own balls
}

$(document).ready(function() {
	var ballRemoved = {
		"ball-one" : false,
		"ball-two" : false,
		"ball-three" : false,
		"ball-four" : false,
		"ball-five" : false,
		"ball-six" : false,
		"ball-seven" : false,
		"ball-eight" : false,
		"ball-nine" : false,
		"ball-ten" : false,
		"ball-eleven" : false,
		"ball-twelve" : false,
		"ball-thirteen" : false,
		"ball-fourteen" : false,
		"ball-fifteeh" : false
	};

	getPlayerBalls();

	$('div.poolball').dblclick(function() {
		var id = $(this).attr('id');
		if(!ballRemoved[id]) {
			$(this).fadeTo(700, 0.3);
			ballRemoved[id] = true;
		}
		else {
			$(this).fadeTo(700, 1);
			ballRemoved[id] = false;
		}	
	});
});
