$(document).ready(function(event) {
	$('body').find('label').remove();
	//Adding,deleting competencies
	$('.competencies ').on('keydown','input', function(event){
		var fields_amount = $(this).parent().children('input').length;
		if (!$(this).val() && event.which == 13 ) {
			event.preventDefault();
			$(this).addClass('bad_input').focus().parent().prev().after('<p class="bad_input_message">Field cant be empty</p>');		
		}
		else if (event.which == 13 && fields_amount < 5 ) {
			event.preventDefault();
			var value = $(this).val();
			var id_number = $(this).parent().children('input').length;
			$(this).parent().append('<span><i class="fa fa-times"></i> ' + value + '</span><input type="text" id="core_compitencies'+id_number+'" class="form-control input-xs" placeholder="e.g. Java">');
			$(this).css('display', 'none');
			$('.competencies input:last-child').focus();
		}
		else if (event.which == 13 && fields_amount == 5 ) {
			event.preventDefault();
			var value = $(this).val();
			var id_number = $(this).parent().children('input').length;
			$(this).parent().append('<span><i class="fa fa-times"></i> ' + value + '</span>');
			$(this).css('display', 'none');
		}
	});
	$('.competencies').on('click','.fa-times',function(event){
		event.preventDefault();
		var span_elements_amount = $(this).parent().parent().children('span').length;

		if ( span_elements_amount == 5 ) {

			$(this).parent().prev().css('display', 'block').val('');
			$(this).parent().remove();
		}
		else {
			$(this).parent().prev().remove();
			$(this).parent().remove();
		}
		
		
	});

	//Adding,deleting achievements
	$(document).on('keydown','.achievements input', function(event){
		var fields_amount = $(this).parent().children('input').length;
		console.log(fields_amount);
		if (!$(this).val() && event.which == 13 ) {
			event.preventDefault();
			alert('Input something');
			return false;		
		}
		else if (event.which == 13 && fields_amount < 3 ) {
			event.preventDefault();
			var number_of_works = $(this).parent().parent();
			var value = $(this).val();
			if ($(number_of_works).hasClass('work_experience')) {
				var id_number = $(this).parent().children('input').length;
				$(this).parent().append('<span><i class="fa fa-times"></i> ' + value + '</span><input type="text" id="work1_achievement'+id_number+'" class="form-control input-xs" placeholder="Write a few sectence on what have you achieved">');
				$(this).css('display', 'none');
				$('.achievements input:last-child').focus();
			}
			else if ($(number_of_works).hasClass('work_experience1')) {
				var id_number = $(this).parent().children('input').length;
				$(this).parent().append('<span><i class="fa fa-times"></i> ' + value + '</span><input type="text" id="work2_achievement'+id_number+'" class="form-control input-xs" placeholder="Write a few sectence on what have you achieved">');
				$(this).css('display', 'none');
				$('.achievements input:last-child').focus();
			}
			else if ($(number_of_works).hasClass('work_experience2')) {
				var id_number = $(this).parent().children('input').length;
				$(this).parent().append('<span><i class="fa fa-times"></i> ' + value + '</span><input type="text" id="work3_achievement'+id_number+'" class="form-control input-xs" placeholder="Write a few sectence on what have you achieved">');
				$(this).css('display', 'none');
				$('.achievements input:last-child').focus();
			}
		}
		else if(event.which == 13 && fields_amount == 3) {
			event.preventDefault();
			$(this).parent().append('<span><i class="fa fa-times"></i> ' + value + '</span>');
			$(this).css('display', 'none');
		}
	});

	$(document).on('click','.achievements .fa-times',function(){
		var span_elements_amount = $(this).parent().parent().children('span').length;
		if ( span_elements_amount == 3 ) {
			$(this).parent().prev().css('display', 'block').val('');
			$(this).parent().remove();
		}
		else {
			$(this).parent().prev().remove();
			$(this).parent().remove();
		}

	});

		//Adding,deleting other skills
	$('.other_skills').on('keydown','input', function(event){
		var fields_amount = $(this).parent().children('input').length;
		if (!$(this).val() && event.which == 13) {
			event.preventDefault();
			alert('Input some of your other skills and hit Enter');

		}
		else if (event.which == 13  && fields_amount < 6) {
			event.preventDefault();
			var value = $(this).val();
			$(this).parent().append('<span><i class="fa fa-times"></i> ' + value + '</span><input type="text" class="form-control input-xs" placeholder="Another skill" autofocus>');
			$(this).css('display', 'none');
			$('.other_skills input:last-child').focus();
		}
		else if(event.which == 13  && fields_amount == 6) {
			event.preventDefault();
			var value = $(this).val();
			$(this).parent().append('<span><i class="fa fa-times"></i> ' + value + '</span>');
			$(this).css('display', 'none');
		}
	});
	$('.other_skills').on('click','.fa-times',function(){
		var span_elements_amount = $(this).parent().parent().children('span').length;
		if ( span_elements_amount == 6 ) {
			$(this).parent().prev().css('display', 'block').val('');
			$(this).parent().remove();				
		}
		else if (span_elements_amount < 6) {
			$(this).parent().prev().remove();
			$(this).parent().remove();	
		}

	});
	//study period check
	$('.form_fields').on('change','input[type="checkbox"]',function(){
		if ($(this).prop('checked') == true) {
			$(this).prev().prop('disabled','true' );
		}
		else  {
			$(this).prev().removeAttr('disabled');
		}
	});

	//Add field set to education
	$('.form_fields ').on('click','#add_study', function(event){
		event.preventDefault();
		

	});
	//Add field set to work experience
	$('.form_fields').on('click','#add_work', function(event){
		event.preventDefault();
		
		if ($(this).prev().prev().hasClass('hidden') && $(this).prev().hasClass('hidden')) {
			$(this).prev().prev().removeClass('hidden').addClass('visible');
		}
		else {
			$(this).prev().removeClass('hidden').addClass('visible');
			$(this).attr('id','remove_work').empty().prepend('<i class="fa fa-minus"></i> Remove last work place');
		}
	});
	$('.form_fields').on('click','#remove_work', function(event){
		event.preventDefault();		
		if ($(this).prev().prev().hasClass('visible') && $(this).prev().hasClass('visible') ) {
			$(this).prev().removeClass('visible').addClass('hidden');
		}
		else {
			$(this).prev().prev().removeClass('visible').addClass('hidden');
			$(this).attr('id','add_work').empty().prepend('<i class="fa fa-plus"></i> Add another work place');
		}
	});
});