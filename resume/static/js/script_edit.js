$(document).ready(function() {
	//Adding,deleting competencies
	$('.competencies ').on('keydown','input', function(event){
		if (!$(this).val() && event.which == 13 ) {
			alert('Input something you posess');
			prevent.default;
		}
		else if (event.which == 13) {
			var value = $(this).val();
			$(this).parent().append('<span><i class="fa fa-times"></i> ' + value + '</span><input type="text" class="form-control input-xs" placeholder="Im good at" autofocus>');
			$(this).css('display', 'none');
			$('.competencies input:last-child').focus();
		}
	});
	$('.competencies').on('click','.fa-times',function(){
		$(this).parent().prev().remove();
		$(this).parent().remove();
	});

	//Adding,deleting achievements
	$('.achievements').on('keydown','input', function(event){
		if (!$(this).val() && event.which == 13 ) {
			alert('Input something');
			prevent.default;
		}
		else if (event.which == 13) {
			var value = $(this).val();
			$(this).parent().append('<span><i class="fa fa-times"></i> ' + value + '</span><input type="text" class="form-control input-xs" placeholder="I did" autofocus>');
			$(this).css('display', 'none');
			$('.achievements input:last-child').focus();
		}
	});
	$('.achievements').on('click','.fa-times',function(){
		$(this).parent().prev().remove();
		$(this).parent().remove();
	});

		//Adding,deleting other skills
	$('.other_skills').on('keydown','input', function(event){
		if (!$(this).val() && event.which == 13 ) {
			alert('Input something');
			prevent.default;
		}
		else if (event.which == 13) {
			var value = $(this).val();
			$(this).parent().append('<span><i class="fa fa-times"></i> ' + value + '</span><input type="text" class="form-control input-xs" placeholder="I did" autofocus>');
			$(this).css('display', 'none');
			$('.other_skills input:last-child').focus();
		}
	});
	$('.other_skills').on('click','.fa-times',function(){
		$(this).parent().prev().remove();
		$(this).parent().remove();
	});
	//study period check
	$('.form_fields').on('change','input[type="checkbox"]',function(){
		if ($(this).prop('checked') == true) {
			$(this).parent().prev().prop('disabled','true' );
		}
		else  {
			$(this).parent().prev().removeAttr('disabled');
		}
	});

	//Add field set to education
	$('.form_fields ').on('click','#add_study', function(event){
		event.preventDefault();
		var field_set = $(this).prev().clone();
		$(this).prev().after(field_set);
	});
	//Add field set to work experience
	$('.form_fields').on('click','#add_work', function(event){
		event.preventDefault();
		var field_set = $(this).prev().clone();
		$(this).prev().after(field_set);
	});
});