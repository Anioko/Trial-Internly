$(document).ready(function(event) {
	$('body').find('label').remove();
	//Adding,deleting competencies
	$('.competencies ').on('keydown','input', function(event){
		if (!$(this).val() && event.which == 13 ) {
			event.preventDefault();
			alert('Input something you posess');
			
		}
		else if (event.which == 13) {
			event.preventDefault();
			var value = $(this).val();
			var id_number = $(this).parent().children('input').length;
			$(this).parent().append('<span><i class="fa fa-times"></i> ' + value + '</span><input type="text" id="core_compitencies'+id_number+'" class="form-control input-xs" placeholder="e.g. Java">');
			$(this).css('display', 'none');
			$('.competencies input:last-child').focus();
		}
	});
	$('.competencies').on('click','.fa-times',function(event){
		event.preventDefault();
		$(this).parent().prev().remove();
		$(this).parent().remove();
	});

	//Adding,deleting achievements
	$(document).on('keydown','.achievements input', function(event){
		if (!$(this).val() && event.which == 13 ) {
			event.preventDefault();
			alert('Input something');
			
		}
		else if (event.which == 13) {
			event.preventDefault();
			var number_of_works = $(this).parent().parent();
			var value = $(this).val();
			if ($(number_of_works).hasClass('work_experience')) {
				var id_number = $(this).parent().children('input').length;
				$(this).parent().append('<span><i class="fa fa-times"></i> ' + value + '</span><input type="text" id="work1_acievement'+id_number+'" class="form-control input-xs" placeholder="Write a few sectence on what have you achieved">');
				$(this).css('display', 'none');
				$('.achievements input:last-child').focus();
			}
			else if ($(number_of_works).hasClass('work_experience1')) {
				var id_number = $(this).parent().children('input').length;
				$(this).parent().append('<span><i class="fa fa-times"></i> ' + value + '</span><input type="text" id="work2_acievement'+id_number+'" class="form-control input-xs" placeholder="Write a few sectence on what have you achieved">');
				$(this).css('display', 'none');
				$('.achievements input:last-child').focus();
			}
			else if ($(number_of_works).hasClass('work_experience2')) {
				var id_number = $(this).parent().children('input').length;
				$(this).parent().append('<span><i class="fa fa-times"></i> ' + value + '</span><input type="text" id="work3_acievement'+id_number+'" class="form-control input-xs" placeholder="Write a few sectence on what have you achieved">');
				$(this).css('display', 'none');
				$('.achievements input:last-child').focus();
			}
		}
	});
	$(document).on('click','.achievements .fa-times',function(){
		$(this).parent().prev().remove();
		$(this).parent().remove();
	});

		//Adding,deleting other skills
	$('.other_skills').on('keydown','input', function(event){
		if (!$(this).val() && event.which == 13 ) {
			prevent.default;
			alert('Input something');
			
		}
		else if (event.which == 13) {
			event.preventDefault();
			var value = $(this).val();
			$(this).parent().append('<span><i class="fa fa-times"></i> ' + value + '</span><input type="text" class="form-control input-xs" placeholder="I did" autofocus>');
			$(this).css('display', 'none');
			$('.other_skills input:last-child').focus();
		}
	});
	$('.other_skills').on('click','.fa-times',function(){
		event.preventDefault();
		$(this).parent().prev().remove();
		$(this).parent().remove();
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
		var field_set = '<div class="form-group study_pace">'+
						'<h6>Education</h6>'+				    
					    '<input type="text" class="form-control input-m" id="degree_description" placeholder="Name of a Degree" autofocus>'+
					    '<input type="text" class="form-control input-m" id="school_name" placeholder="Name of a University">'+
					    '<input type="text" class="form-control input-m" id="location_school" placeholder="Location of a University">'+
					    '<input type="text" class="form-control input-m" id="start_date_school" placeholder="Beginnig">'+
					    '<input type="text" class="form-control input-m" id="end_date_school" placeholder="End">'+
					    '<input type="checkbox" id="school_currently"> Currently'+
					    '</div>';
		$(this).prev().after(field_set);
	});
	//Add field set to work experience
	$('.form_fields').on('click','#add_work', function(event){
		event.preventDefault();
		
		if ($(this).prev().prev().hasClass('hidden') && $(this).prev().hasClass('hidden') ) {
			$(this).prev().prev().removeClass('hidden').addClass('visible');
		}
		else {
			$(this).prev().removeClass('hidden').addClass('visible');
			$(this).attr('id','remove_work').text('Remove last work place');
		}
	});
	$('.form_fields').on('click','#remove_work', function(event){
		event.preventDefault();		
		if ($(this).prev().prev().hasClass('visible') && $(this).prev().hasClass('visible') ) {
			$(this).prev().removeClass('visible').addClass('hidden');
		}
		else {
			$(this).prev().prev().removeClass('visible').addClass('hidden');
			$(this).attr('id','add_work').text('Add another work place');
		}
	});
});