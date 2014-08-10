$(document).ready(function(event) {
  if ($('body').find('.header').hasClass('about')) {
    $('body').find('.navigation li').removeClass('active');
    $('body').find('.navigation li:nth-child(2)').addClass('active');
  }	
  else if ($('body').find('.header').hasClass('policy')) {
    $('body').find('.navigation li').removeClass('active');
    $('body').find('.navigation li:nth-child(4)').addClass('active');
  }
});