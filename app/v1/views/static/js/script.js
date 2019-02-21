$(document).ready(function () {

  $('.js_sell_section').waypoint(function (direction) {

    if (direction == "down") {
      $('nav').addClass('sticky_nav');
    } else {
      $('nav').removeClass('sticky_nav');
    }
  },
  //Enable the sticky_nav 60px before hitting the 'js_sell_section'
  { offset: '60px;' });
  
  $('.js_nav_icon').click(function() {
    // This will hold the result of selecting the navigation
    var nav = $('.js_main_nav');
    var icon = $('.js_nav_icon i');
    // This opens and close the mobile nav within 200 miliseconds
    nav.slideToggle(200);
    // Switches the icon for the mobile nav depending on the status of the nav
      // i.e if open or close
    if (icon.hasClass('ion-navicon-round')) {
      icon.addClass('ion-close-round');
      icon.removeClass('ion-navicon-round');
    } else {
      icon.addClass('ion-navicon-round');
      icon.removeClass('ion-close-round');
    }
  });

  $('a[href*="#"]')
  // Remove links that don't actually link to anything
  .not('[href="#"]')
  .not('[href="#0"]')
  .click(function(event) {
    // On-page links
    if (
      location.pathname.replace(/^\//, '') == this.pathname.replace(/^\//, '') 
      && 
      location.hostname == this.hostname
    ) {
      // Figure out element to scroll to
      var target = $(this.hash);
      target = target.length ? target : $('[name=' + this.hash.slice(1) + ']');
      // Does a scroll target exist?
      if (target.length) {
        // Only prevent default if animation is actually gonna happen
        event.preventDefault();
        $('html, body').animate({
          scrollTop: target.offset().top
        }, 1000, function() {
          // Callback after animation
          // Must change focus!
          var $target = $(target);
          $target.focus();
          if ($target.is(":focus")) { // Checking if the target was focused
            return false;
          } else {
            $target.attr('tabindex','-1'); // Adding tabindex for elements not focusable
            $target.focus(); // Set focus again
          };
        });
      }
    }
  });


});