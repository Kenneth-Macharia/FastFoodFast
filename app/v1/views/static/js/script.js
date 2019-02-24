/* JAVASCRIPT CODE */
//Show login modal - Customer previous orders link
document.querySelector("#prev_ord").addEventListener("click", loginModal ('openCustomer'), false);

//Hide login modal
document.querySelector("#close").addEventListener("click", loginModal ('close'), false);

//Login logic
AccessToken = '';
function login() {
  // Reset login modal on wrong inputs correction
  document.querySelector("#uemail").addEventListener("focus", resetLoginModal ('resetEmail'), false);
  document.querySelector("#upsw").addEventListener("focus", resetLoginModal ('resetPassword'), false);

  //Get the login form data
  var email = document.querySelector("#uemail").value;
  var password = document.querySelector("#upsw").value;
  var formData = new FormData();
  formData.append('User_Email', email);
  formData.append('User_Password', password);

  //Create request object
  const url = 'http://127.0.0.1:5000/v1/auth/login'

  var request = new Request(url, {
    method: 'POST',
    body: formData,
    headers: new Headers(),
    mode: 'cors',
    cache: 'default'}
  );

  //Send login request to backend
  fetch(request).then(function(response) {
    if (response.status === 404) {
      //TODO: server connection error & internal server error message
      document.querySelector('#elabel').style.color = "red";
      document.querySelector('#plabel').style.color = "";
    } else if (response.status === 400) {
      document.querySelector('#plabel').style.color = "red";
      document.querySelector('#elabel').style.color = "";
    } else if  (response.status === 200) {
      //close login modal
      loginModal ('close'); //TODO: Fix close login modal
      
      //open customer previous orders modal

      //open customer checkout modal

      //open admin page

    } 
  });
}

// Show/close login modal function
function loginModal (action) {
  return function (e) {
    if (action === 'openCustomer') {
      e.preventDefault();
      document.querySelector("#login").style.display = "block";
      document.querySelector("#login").style.animation = "slide_from_top 0.7s";
      resetLoginModal('loadForm'); //TODO: Fix clear login modal
  
    } else if (action === 'close') {
      e.preventDefault();
      document.querySelector("#login").style.animation = "slide_back_to_top 0.7s";
      document.querySelector("#login").style.display = "none"; //TODO: Fix login modal slide up effect
    }
  }
}

// Inputs/Labels reset function
function resetLoginModal (action) {
  return function () {
    emailLabel = document.querySelector("#elabel");
    passwordLabel = document.querySelector("#plabel");
    emailInput = document.querySelector("#uemail")
    passwordInput = document.querySelector("#upsw")

    if (action === 'loadForm') {
      emailLabel.style.color = ''
      passwordLabel.style.color = ''
      emailInput.value = ''
      passwordInput.value = ''

    } else if (action === 'resetEmail') {
      if (emailLabel.style.color = 'red') {
        emailLabel.style.color = '';}

    } else if (action === 'resetPassword') {
        if (passwordLabel.style.color = 'red') {
          passwordLabel.style.color = '';}
    }
  }    
}


/* JQUERY CODE */
//Index.html - Sticky navigation
$('.js_sell_section').waypoint(function (direction) {

  if (direction == "down") {
    $('nav').addClass('sticky_nav');
  } else {
    $('nav').removeClass('sticky_nav');
  }
},
  //Enable the sticky_nav 60px before hitting the 'js_sell_section'
{ offset: '60px;' });

//Index.html - Mobile nav bar, active in a viewport width < 730px
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

//Index.html - Smooth scrolling effect
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