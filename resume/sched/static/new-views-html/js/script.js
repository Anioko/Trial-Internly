$(document).ready(function(){
	//Values on loading

	var name = $('.resume_edit input#name').val();
	var email = $('.resume_edit input#email').val();
	var phone = $('.resume_edit input#phone').val();
	var location = $('.resume_edit input#user_location').val();
	var linkedin = $('.resume_edit input#linkedin_link').val();
	$('.resume_edit .user_name').text(name);
	$('.resume_edit #email').prev().children('span').text(email);
	$('.resume_edit #phone').prev().children('span').text(phone);
	$('.resume_edit #user_location').prev().children('span').text(location);
	$('.resume_edit #linkedin_link').prev().children('span').text(linkedin);

	//Action on blur and enter
	$('.resume_edit input').on('blur', function(){
		$(this).fadeOut(150).prev().delay(300).fadeIn('fast');				
	});

	//Name
	$('.resume_edit input#name').keypress(function(event) {
		if ( event.which == 13 ) {
	        var name = $('.resume_edit input#name').val();
			$('.resume_edit .user_name').text(name);
			$(this).fadeOut(200).prev('.user_name').fadeIn('fast');		
	    }		
	});
	//Contacts
	$('.resume_edit ul li input').keypress(function(event) {
		if ( event.which == 13 ) {
	        var value = $(this).val();
			$(this).prev().text(' '+ value);
			$(this).fadeOut(200).prev('.user_name').fadeIn('fast');		
	    }		
	});

	// Input fields on click
	$('.resume_edit h2').on('click', function(e){
		$(this).fadeOut(200).next('input').delay(190).fadeIn('fast');
	});
	$('.resume_edit .contacts ul li i').on('click', function(e){
		$(this).children('span').fadeOut(200);
		$(this).next('input').delay(190).fadeIn('fast');
	});
});