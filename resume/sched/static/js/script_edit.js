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
			var number_of_works = $(this).parent().parent().length;
			var value = $(this).val();
			if ($(number_of_works) == 1) {
				var number_of_works = $(this).parent().children('input').length;
				$(this).parent().append('<span><i class="fa fa-times"></i> ' + value + '</span><input type="text" id="work1_acievement" class="form-control input-xs" placeholder="Write a few sectence on what have you achieved">');
				$(this).css('display', 'none');
				$('.achievements input:last-child').focus();
			}
			else if ($(number_of_works) == 2) {
				var number_of_works = $(this).parent().children('input').length;
				$(this).parent().append('<span><i class="fa fa-times"></i> ' + value + '</span><input type="text" id="work1_acievement1" class="form-control input-xs" placeholder="Write a few sectence on what have you achieved">');
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
		var field_set = '<div class="form-group work_experience">'+
						'<h6>Work Experience</h6>'+
					    '<input type="text" class="form-control input-lg" id="company_name" placeholder="Company name" autofocus>'+
					    '<input type="text" class="form-control input-lg" id="location_company" placeholder="Company location">'+
					    '<input type="text" class="form-control input-lg" id="start_date_company" placeholder="Beginnig">'+
					    '<input type="text" class="form-control input-lg" id="end_date_company" placeholder="End">'+
					    '<input type="checkbox" id="work_currently" value="y"> Currently'+
					    '<textarea class="form-control" rows="5" id="company_summary" placeholder="Brief description of the Company"></textarea>'+
					    '<input type="text" class="form-control input-m" id="role" placeholder="Your position">'+
					    '<h6>Achievements</h6>'+
					    '<div class="achievements">'+
						'<input type="text" class="form-control input-xs" id="work_acievement_1" placeholder="Write a few sectence on what have you achieved">'+
					    '</div>'+
					'</div>';
		$(this).prev().after(field_set);
	});
});