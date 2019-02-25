/*--------------------------------------------------------------------------
                              JAVASCRIPT CODE
  ------------------------------------------------------------------------*/
/*----------ELEMENTS EVENTS--------*/
// Access customer previous orders link (Open login modal)
document.querySelector("#prev_ord").addEventListener("click", function (e) { 
  e.preventDefault();
  openCloseLoginModal('openLoginModal', 'prev_ord')}, false);

 // Access admin dashboard link (Open login modal)
document.querySelector("#admin").addEventListener("click", function (e) { 
  e.preventDefault();
  openCloseLoginModal('openLoginModal', 'admin')}, false);

// Access customer checkout order button (Open login modal)


// Login modal close button (Dismiss login modal)
document.querySelector(".js_close").addEventListener("click", function () {
  openCloseLoginModal('closeLoginModal')}, false);

// Reset login modal on wrong input - nth login attempt
document.querySelector("#uemail").addEventListener("focus", function () {
  resetLoginModal ('resetEmail')}, false);
document.querySelector("#upsw").addEventListener("focus", function () {
  resetLoginModal ('resetPassword')}, false);


  
/*----------CUSTOM FUNCTIONS---------*/
 

// User login
function login() {
  //Get the login form data
  var email = document.querySelector("#uemail").value;
  var password = document.querySelector("#upsw").value;
  var formData = new FormData();
  formData.append('User_Email', email);
  formData.append('User_Password', password);

  // Create login request data object
  const url = 'http://127.0.0.1:5000/v1/auth/login'
  var requestData = new Request(url, {
    method: 'POST',
    body: formData,
    headers: new Headers(),
    mode: 'cors',
    cache: 'default'}
  );

  // Send login request
  fetch(requestData)
    .then((response) => {
      if (response.status === 404) {
        document.querySelector('#elabel').style.color = "red";
        document.querySelector('#plabel').style.color = "";
        return Promise.reject(new Error(response.statusText))
      } else if (response.status === 400) {
        document.querySelector('#plabel').style.color = "red";
        document.querySelector('#elabel').style.color = "";
        return Promise.reject(new Error(response.statusText))
      } else if (response.status === 200) {
        //openCloseLoginModal('closeLoginModal');
        return Promise.resolve(response);
      }
    })
    .then((response) => {return response.json()})
    .then(function(data) {

      idValue = document.querySelector('.modal').getAttribute('id');

      if (idValue === 'admin') {
      //verify admin privileges and open the admin dashboard
        var header = new Headers({
          "Content-Type": "application/json",
          "Authorization": "Bearer ".concat(data['Access_token'])
        });

        const url = 'http://127.0.0.1:5000/v1/auth/update'
        var requestData = new Request(url, {
          method: 'POST',
          body: formData,
          mode: 'cors',
          cache: 'default',
          credentials: 'include',
          headers: header});

        fetch(requestData)
          .then((response) => {return response.json()})
          .then(function(authData) {
            console.log(authData);
          })


        }
    })
    .catch ((error) => {console.log('Request failed', error)});

    // // Open requred modal or page
    // if (action === 'userPrevOrders') {
    //   //confirm it's a Guest logging in
    //   //open customer previous orders modal
      
    // } else if (action === 'userCheckoutOrders') {
    //   //confirm it's a Guest logging in
    //   //open customer checkout modal

    // } else if (action === 'adminDashboard') {
    //   //confirm it's an admin logging in
    //   //open admin dashboard
    // }

}

// Inputs/Labels reset function
function resetLoginModal (action) {
  emailLabel = document.querySelector("#elabel");
  passwordLabel = document.querySelector("#plabel");
  emailInput = document.querySelector("#uemail")
  passwordInput = document.querySelector("#upsw")

  if (action === 'clearForm') {
    emailLabel.style.color = ''
    passwordLabel.style.color = ''
    emailInput.value = ''
    passwordInput.value = ''

  } else if (action === 'resetEmail') {
    if (emailLabel.style.color = 'red') {
      emailLabel.style.color = '';
    }

  } else if (action === 'resetPassword') {
      if (passwordLabel.style.color = 'red') {
        passwordLabel.style.color = '';
      }
  }   
}

// Show|Close login form function
function openCloseLoginModal (action, source) {
  modalForm = document.querySelector(".modal")
  if (action === 'openLoginModal') {
    if (modalForm.hasAttribute("id")) {
      modalForm.style.display = "none"
    }
    modalForm.setAttribute("id", source);
    modalForm.style.display = "block";
    document.querySelector("#uemail").focus();
    //document.querySelector("#login").style.animation = "slide_from_top 0.7s";
  } else if (action === 'closeLoginModal') { //TODO: Fix modal animation
    //document.querySelector("#login").style.animation = "slide_back_to_top 0.7s";
    if (modalForm.hasAttribute("id")) {
      modalForm.removeAttribute("id")
    }
    modalForm.style.display = "none";
    resetLoginModal('clearForm');
  }
}

/*-------------------------------------------------------------------------
                              JQUERY CODE
  -----------------------------------------------------------------------*/
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