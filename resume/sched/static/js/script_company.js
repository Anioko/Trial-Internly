$(document).ready(function(event) {
  if ($('body').find('.header').hasClass('about')) {
    $('body').find('.navigation li').removeClass('active');
    $('body').find('.navigation li:nth-child(2)').addClass('active');
  }	
  else if ($('body').find('.header').hasClass('policy')) {
    $('body').find('.navigation li').removeClass('active');
    $('body').find('.navigation li:nth-child(4)').addClass('active');
  }
  else if ($('body').find('.container').hasClass('signup')) {
    $('body').addClass('blue_background');
  }
  else if ($('body').find('.container').hasClass('login')) {
    $('body').addClass('green_background');
  }

  //CHANGE BACKGROUND ON SIGN UP FORM
  $('.signup .checkbox').on('change','input[type="checkbox"]',function(){
    if ($(this).prop('checked') == true) {
      $('#submit').removeClass('hover_blue');
      $('body').removeClass('blue_background');
      $('body').addClass('green_background');
      $('#submit').addClass('hover_green');
    }
    else  {
      $('#submit').removeClass('hover_green');
      $('body').removeClass('green_background');
      $('body').addClass('blue_background');
      $('#submit').addClass('hover_blue');
    }
  });

  
 
});