$(document).ready(function(event) {
	function isEmpty( el ){
      return !$.trim(el.html())
  }
  $('.job').each(function(){
  	  if ( isEmpty($(this).find('.employee li')) ) {
	      $(this).addClass('hidden');
	  }
  });

});