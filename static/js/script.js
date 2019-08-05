/*--------------------------------------------------------------------------
           JAVASCRIPT CODE - Handles core webapage functionality
  ------------------------------------------------------------------------*/

/*----------GLOBAL VARIABLES---------*/

// Backend server location - Base url for Heroku hosted API
var api_base_url = 'https://api-fastfoodfast.herokuapp.com'

// Fetch header object with authorization credentials
var header;


/*----------ELEMENTS EVENTS--------*/

// Access customer previous orders link (Open login modal)
document.querySelector("#prev_ord").addEventListener("click", function (e) { 
  e.preventDefault();
  openCloseModals('openLoginModal', 'prev_ord')
}, false);

// Access admin dashboard link (Open login modal)
document.querySelector("#admin").addEventListener("click", function (e) { 
  e.preventDefault();
  openCloseModals('openLoginModal', 'admin')
}, false);

// Logout user (Both admins and guest) - close the modal and blacklist theh token
// On page reload save the user token and when the link to open a protected modal is clicked check if its has expired and reqire login, else just open the protected modal.
//https:developer.mozilla.org/en-US/docs/Web/API/Window/sessionStorage

//Access customer checkout order button (Open login modal)
// document.querySelector("").addEventListener("click", function (e) { 
//   e.preventDefault();
//   openCloseModals('openLoginModal', 'checkout')
// }, false);


// Open signup modal via 'Quick Registration' link on login modal
document.querySelector("#rlabel").addEventListener("click", function () { 
  openCloseModals('openSignUpModal', 'admin')
}, false);

// Login modal close button (Dismiss login modal)
document.querySelector(".js_close_login").addEventListener("click", function () {
  openCloseModals('closeLoginModal')
}, false);

// Signup modal close button (Dismiss signup modal)
document.querySelector(".js_close_signup").addEventListener("click", function () {
  openCloseModals('closeSignUpModal')
}, false);

// Add menu close button (Dismiss add menu modal)
document.querySelector(".js_close_add_menu").addEventListener("click", function () {
  openCloseModals('closeAddMenuModal')
}, false);

// Reset login & signup modal error labels on wrong input
document.querySelector("#uemail").addEventListener("focus", function () {
  resetModals('resetLoginEmail')
}, false);
document.querySelector("#upsw").addEventListener("focus", function () {
  resetModals('resetLoginPassword')
}, false);
document.querySelector("#suemail").addEventListener("focus", function () {
  resetModals('resetSignupEmail')
}, false);  
document.querySelector("#supsw").addEventListener("focus", function () {
  resetModals('resetSignupPassword')
}, false);
document.querySelector("#supsw2").addEventListener("focus", function () {
  resetModals('resetSignupPassword')
}, false);

// Close and reset Admin modal
document.querySelector("#logout").addEventListener("click", function (e) { 
  e.preventDefault();
  closeTables('#menu_table');
  document.querySelector('#menulist').classList.remove('js-deactivateLink');
  // Close modal
  document.querySelector('.admin_section').style.display = 'none';
  // Reset view header p
  document.querySelector('.view_header p').style.color = "#e4e1e1fa";
  document.querySelector(".view_header p").innerHTML = 'View section heading';
}, false);

// Admin dash header close button function
document.querySelector(".js_close_table").addEventListener('click', function() {
  
  if (document.querySelector('.view_header p').innerHTML === 'Menu List') {
    closeTables('#menu_table');
    document.querySelector('#menulist').classList.remove('js-deactivateLink');
  }
    // Reset view header p in admin dash board
  document.querySelector('.view_header p').style.color = "#e4e1e1fa";
  document.querySelector(".view_header p").innerHTML = 'View section heading';
}, false);

// Menu list link clicked on admin dash navigation (initialize get all menus)
document.querySelector("#menulist").addEventListener("click", function (e) {
  e.preventDefault();

  if (document.querySelector('.view_header p').innerHTML === 'Menu List') {
      document.querySelector('#menulist').classList.add('js-deactivateLink');
  } else {
    getMenu();
  }
}, false);

// Add menu link clicked on admin dash navigation (initialize add new menu item)
document.querySelector("#addmenu").addEventListener("click", function (e) {
  e.preventDefault();

  // Close any table in admin dash
  document.querySelector(".js_close_table").click();

  // Open add menu modal
  openCloseModals('openAddMenuModal', 'admin');
  
}, false);

  
/*----------FEATURE FUNCTIONS---------*/

// Add new menu item
function addMenuItem() {
  //Get the login form data
  var formData = new FormData();
  formData.append('Menu_Name', document.querySelector("#menuname").value);
  formData.append('Menu_Description', document.querySelector("#menudesc").value);
  formData.append('Menu_Price', parseInt(document.querySelector("#menuprice").value, 10));
  formData.append('Menu_ImageURL', document.querySelector("#menuurl").value);

  // Request data object
  const add_menu_endpoint = api_base_url.concat('/v1/menu');
  var requestData = new Request(add_menu_endpoint, {
    method: 'POST',
    mode: 'cors',
    body: formData,
    cache: 'default',
    credentials: 'include',
    headers: header});

  // Send add menu request
  fetch(requestData)
    .then(response => {
      if (response.status === 201) {
        return Promise.resolve(response);
      } else {
        return Promise.reject(new Error(response.statusText))
      }
    })
    .then(response => {return response.json()})
    .then(function (data) {
      openCloseModals('closeAddMenuModal', 'admin');
      let msg = data.Response.Success;
      alert(msg);
    })
    // .catch (error => {alert('Server error, contact the site administrator.')}); //TODO: Error handling
}

// Fetch all menus logic
function getMenu() {
  // Request data object
  const get_menus_endpoint = api_base_url.concat('/v1/menus');
  var requestData = new Request(get_menus_endpoint, {
    method: 'GET',
    mode: 'cors',
    cache: 'default',
    credentials: 'include',
    headers: header});

  // Send get menus request
  fetch(requestData)
    .then(response => {
      if (response.status === 200) {
        return Promise.resolve(response);
      } else {
        return Promise.reject(new Error(response.statusText))
      }
    })
    .then(response => {return response.json()})
    .then(function (data) {
      result = data.Response.Success

      if (result === 'No menu items found') {
        document.querySelector('.view_header p').innerHTML = result;
        document.querySelector('.view_header p').style.color = "#e67e22";
      } else {
        document.querySelector('.view_header p').innerHTML = "Menu List";
        document.querySelector('.view_header p').style.color = "#e67e22";
        showMenuTable(result);
      }
    })
    // .catch (error => {alert('Server error, contact the site administrator.')}); //TODO: Error handling
}

// USER LOGIN //
function login() {
  //Get the login form data
  var email = document.querySelector("#uemail").value;
  var password = document.querySelector("#upsw").value;
  var formData = new FormData();
  formData.append('User_Email', email);
  formData.append('User_Password', password);

  // Create login request data object
  const signin_endpoint = api_base_url.concat('/v1/auth/login');
  var requestData = new Request(signin_endpoint, {
    method: 'POST',
    body: formData,
    headers: new Headers(),
    mode: 'cors',
    cache: 'default'}
  );

  // Send login request
  fetch(requestData)
    .then(response => {
      if (response.status === 404) {
        document.querySelector('#elabel').style.color = "red";
        return Promise.reject(new Error(response.statusText))
      } else if (response.status === 400) {
        document.querySelector('#plabel').style.color = "red";
        return Promise.reject(new Error(response.statusText))
      } else if (response.status === 200) {
        return Promise.resolve(response);
      }
    })
    .then(response => {return response.json()})
    .then(function(data) {
      idValue = document.querySelector('.modal_login').getAttribute('id');

      header = new Headers({
        "Authorization": "Bearer ".concat(data.Access_token)
      });

      var requestData = {
        method: 'GET',
        mode: 'cors',
        cache: 'default',
        credentials: 'include',
        headers: header};
      
      //Attempt login to an admin feature to verify admin rights
      if (idValue === 'admin') {
        var fetchData = new Request(api_base_url.concat('/v1/menus'), requestData);
          
        fetch(fetchData)
          .then(response => {
            if (response.status === 200) {
              openCloseModals('closeLoginModal');
              document.querySelector('.admin_section').style.display = "block";
            } else if (response.status === 401) {
              document.querySelector('#alabel').style.color = "red";
            }
          })

      /* Attempt login to a Guest feature to verify Guest rights. Note Admins
        cannot access Guest features like placing orders and viewing previous
        orders */
      } else if (idValue === 'prev_ord') {
        var fetchData = new Request(api_base_url.concat('/v1/users/orders'), requestData);

        fetch(fetchData)
        .then(response => {
          if (response.status === 200) {
            openCloseModals('closeLoginModal');
            //open the previous order modal

          } else if (response.status === 401) {
            document.querySelector('#alabel').style.color = "red";
          }
        })
      } else if (idValue === 'checkout') {
        var fetchData = new Request(api_base_url.concat('/v1/users/orders'), requestData);

        fetch(fetchData)
        .then(response => {
          if (response.status === 200) {
              //open the checkout order page confirm payment and create saveorder            

          } else if (response.status === 401) {
            document.querySelector('#alabel').style.color = "red";
          }
        })
      }
    })
    // .catch (error => {alert('Server error, contact the site administrator.')}); //TODO: Error handling
}

// USER SIGNUP //
function signUp() {
  //Get the signup form data
  var name = document.querySelector("#suname").value;
  var email = document.querySelector("#suemail").value;
  var address = document.querySelector("#suadd").value;
  var password = document.querySelector("#supsw").value;
  var password2 = document.querySelector("#supsw2").value;

  // Ensure passwords match
  if (password === password2) {
    // create the form data object
    var formData = new FormData();
    formData.append('User_Name', name);
    formData.append('User_Email', email);
    formData.append('User_Address', address);
    formData.append('User_Password', password);

    // Create signup request data object
    const signup_endpoint = api_base_url.concat('/v1/auth/signup');
    var requestData = new Request(signup_endpoint, {
      method: 'POST',
      body: formData,
      headers: new Headers(),
      mode: 'cors',
      cache: 'default'}
    );

    // Send signup request
    fetch(requestData)
      .then(response => {
        if (response.status === 400) {
          document.querySelector('#selabel').style.color = "red";
          return Promise.reject(new Error(response.statusText))
        } else if (response.status === 201) {
          return Promise.resolve(response);
        }
      })
      .then(response => {return response.json()})
      .then(function (data) {
        openCloseModals('closeSignUpModal');
        idValue = document.querySelector('.modal_login').getAttribute('id');
        let msg = data.Response.Success
        alert(msg);
        openCloseModals('openLoginModal', idValue);
      })
      // .catch (error => {alert('Server error, contact the site administrator.')}); // TODO: Error handdling?

  } else {document.querySelector('#splabel').style.color = "red";}
}


 /*----------HELPER FUNCTIONS---------*/

 // Add menu item logic
 var cart_buttons = document.querySelectorAll('.add_cart');

function collectCartItems() {
  // Figure out which menu items has been clicked
  this.setAttribute('id', 'clicked');

}

for (var i = 0; i < cart_buttons.length; i++) {
  cart_buttons[i].addEventListener('click', collectCartItems)


  // Collect the menu name & price from the DOM as an object

  
  // Add the menu details object to an order array, store to a session object


  // Dsiplay menu added to cart pop ups


  // Change cart icon color to orange, if atleast on item in cart


}

 // Close tables displayed in the admin dash
function closeTables (tableId) {

  if (tableId === '#menu_table') {
    let table = document.querySelector("#menu_table").querySelector("tbody");
    rows = table.rows.length

    for (var i = (rows - 1); i >= 0; i--) {
      table.deleteRow(i);
    }
    document.querySelector('#menu_table').style.display = 'none';

  }

}

// var el = getElementsByClassName('module');
// for (var i=0; i < el.length; i++) {
//     // Here we have the same onclick
//     el.item(i).onclick = clickerFn;
// }

// var x = document.getElementById("myTable").rows[0].cells;
// x[0].innerHTML = "NEW CONTENT";


  // Show Menus table
function showMenuTable(menuArray) {
  // Get the menu table to add rows to
  let table = document.querySelector("#menu_table").querySelector("tbody");
  // For each item in the array returned from the backend do the following:
  var i;
  for (i = 0; i <= (menuArray.length - 1); i++) {
    // Insert row
    let newRow = table.insertRow(table.rows.length);

    var j;
    for (j = 0; j <= 3; j++) {
      
      // Insert new 4 cells per row, append menuArray data and control elements
      let newCell = newRow.insertCell(j);

      if (j === 0) {
        let newText = document.createTextNode(menuArray[i].Menu_Id);
        newCell.appendChild(newText);
      } else if (j === 1) {
        let newText = document.createTextNode(menuArray[i].Menu_Name);
        newCell.appendChild(newText);
      } else if (j === 2) {
        let newText = document.createTextNode('$' + menuArray[i].Menu_Price);
        newCell.appendChild(newText);
      } else if (j === 3) {
        // Create the checkbox and submits input per row in 'Action cell'
          // Create the container divs, 1 for the checkboxes, the other for the submits
        let checkboxDiv = document.createElement("DIV");
        checkboxDiv.setAttribute("class", "view_info_div");
        let submitDiv = document.createElement("div");
        submitDiv.setAttribute("class", "view_info_div");

          // Create the nodes, 1 checkbox with a label and 2 submits and append to their respective divs
        let menuCheck = document.createElement("INPUT");
        menuCheck.setAttribute("type", "checkbox");
        menuCheck.setAttribute("name", "menu_availability");
        menuCheck.setAttribute("id", "menu_check");
        if (menuArray[i].Menu_Availability === "Available") {
          menuCheck.checked = true;
        checkboxDiv.appendChild(menuCheck);
        } else if (menuArray[i].Menu_Availability === "Unavailable") {
          menuCheck.checked = false;
          checkboxDiv.appendChild(menuCheck);
        }

        let menuCheckLabel = document.createElement("LABEL");
        let menuCheckLabelText = document.createTextNode("Available");
        menuCheckLabel.appendChild(menuCheckLabelText);
        checkboxDiv.appendChild(menuCheckLabel);
        
        let submitEdit = document.createElement("INPUT");
        submitEdit.setAttribute("type", "submit");
        submitEdit.setAttribute("value", "Edit");
        submitEdit.setAttribute("id", "submit_e");
        submitDiv.appendChild(submitEdit);

        let submitDelete = document.createElement("INPUT");
        submitDelete.setAttribute("type", "submit");
        submitDelete.setAttribute("value", "Delete");
        submitDelete.setAttribute("id", "submit_d");
        submitDiv.appendChild(submitDelete);

        // Append the two divs to the last row cell 
        newCell.appendChild(checkboxDiv);
        newCell.appendChild(submitDiv);
      }
    }  
  }
   // Show the table
   document.querySelector("#menu_table").style.display = "block";
}
 
 // Inputs/Labels reset function
function resetModals (action) {
  // Login fields to clear
  emailLabel = document.querySelector("#elabel");
  passwordLabel = document.querySelector("#plabel");
  emailInput = document.querySelector("#uemail");
  passwordInput = document.querySelector("#upsw");
  authLabel = document.querySelector('#alabel');

  // Signup fields to clear
  s_nameInput = document.querySelector("#suname");
  s_emailLabel = document.querySelector("#selabel");
  s_emailInput = document.querySelector("#suemail");
  s_addressInput = document.querySelector('#suadd');
  s_passwordLabel = document.querySelector("#splabel");
  s_passwordInput = document.querySelector("#supsw");
  s2_passwordInput = document.querySelector("#supsw2");

  switch (action) {
    case 'clearLoginForm':
      authLabel.style.color = '';
      emailLabel.style.color = ''
      passwordLabel.style.color = ''
      emailInput.value = ''
      passwordInput.value = ''
      break;

    case 'resetLoginEmail':
      if (emailLabel.style.color == 'red') {
        emailLabel.style.color = '';
      } else if (authLabel.style.color == 'red') {
        authLabel.style.color = '';
      }
      break;

    case 'resetLoginPassword':
      if (passwordLabel.style.color == 'red') {
        passwordLabel.style.color = '';
      }
      break;

    case 'clearSignupForm':
      s_nameInput.value = '';
      s_emailLabel.style.color = '';
      s_emailInput.value = '';
      s_addressInput.value = '';
      s_passwordLabel.style.color = '';
      s_passwordInput.value = '';
      s2_passwordInput.value = '';
      break;

    case 'resetSignupEmail':
      if (s_emailLabel.style.color == 'red') {
        s_emailLabel.style.color = '';
      }
      break;

    case 'resetSignupPassword':
      if (s_passwordLabel.style.color == 'red') {
        s_passwordLabel.style.color = '';
      }
      break;

    case 'clearAddMenuModal':
      document.querySelector('#menuname').value = '';
      document.querySelector('#menudesc').value = '';
      document.querySelector('#menuprice').value = '';
      document.querySelector('#menuurl').value = '';
      break;
  }

}

// Show|Close login form function
function openCloseModals (action, source) {
  modalLogin = document.querySelector(".modal_login");
  modalSignup = document.querySelector(".modal_signup");
  modalAddMenu = document.querySelector(".modal_menu-add");

  switch (action) {
    case 'openLoginModal':
      if (modalLogin.hasAttribute("id")) {
        modalLogin.style.display = "none"
      }
      modalLogin.setAttribute("id", source);
      modalLogin.style.display = "block";
      document.querySelector("#uemail").focus();
      break;

    case 'closeLoginModal':
      if (modalLogin.hasAttribute("id")) {
        modalLogin.removeAttribute("id")
      }
      modalLogin.style.display = "none";
      resetModals('clearLoginForm');
      break;

    case 'openSignUpModal':
      modalLogin.style.display = "none";
      resetModals('clearLoginForm');
      modalSignup.style.display = "block";
      document.querySelector("#suname").focus();
      break;

    case 'closeSignUpModal':
      modalSignup.style.display = "none";
      resetModals('clearSignupForm');
      break;

    case 'openAddMenuModal':
      modalAddMenu.style.display = "block";
      document.querySelector('#menuname').focus();
      break;
      
    case 'closeAddMenuModal':
      modalAddMenu.style.display = "none";
      resetModals('clearAddMenuModal');
      break;
  }

}


/*-------------------------------------------------------------------------
                JQUERY CODE - Handles the webpage animations
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