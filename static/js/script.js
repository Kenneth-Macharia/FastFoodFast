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
// document.querySelector("").addEventListener("click", function (e) { 
//   e.preventDefault();
//   openCloseLoginModal('openLoginModal', 'checkout')}, false);

// Open signup modal via 'Quick Registration' link on login modal
document.querySelector("#rlabel").addEventListener("click", function () { 
  openCloseLoginModal('openSignUpModal', 'admin')}, false);

// Login modal close button (Dismiss login modal)
document.querySelector(".js_close_login").addEventListener("click", function () {openCloseLoginModal('closeLoginModal')}, false);

// Signup modal close button (Dismiss signup modal)
document.querySelector(".js_close_2").addEventListener("click", function () {
  openCloseLoginModal('closeSignUpModal')}, false);

// Reset login & signup modal error labels on wrong input
document.querySelector("#uemail").addEventListener("focus", function () {
  resetLoginModal('resetLoginEmail')}, false);
document.querySelector("#upsw").addEventListener("focus", function () {
  resetLoginModal('resetLoginPassword')}, false);
document.querySelector("#suemail").addEventListener("focus", function () {
  resetLoginModal('resetSignupEmail')}, false);  
document.querySelector("#supsw").addEventListener("focus", function () {
  resetLoginModal('resetSignupPassword')}, false);
document.querySelector("#supsw2").addEventListener("focus", function () {
  resetLoginModal('resetSignupPassword')}, false);

// Admin dash header close button function
document.querySelector(".js_close_table").addEventListener('click', function() {
  if (document.querySelector('.view_header p').innerHTML = 'Menu List') {
    closeTables('#menu_table');
  }
  }, false);

// Menu list link clicked on admin dash navigation (initialize get all menus)
document.querySelector("#menulist").addEventListener("click", function (e) {
  e.preventDefault();
  getMenu()}, false);

  
/*----------FEATURE FUNCTIONS---------*/

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

// Fetch all menus logic
function getMenu() {
  // Create login request data object
  const url = 'http://127.0.0.1:5000/v1/menus'
  var requestData = new Request(url, {
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

      if (result[0] === 'No menu items found') {
        document.querySelector('.view_header p').innerHTML = result[0];
        document.querySelector('.view_header p').style.color = "#e67e22";
        document.querySelector('.js_close_table').style.color = "black";
      } else {
        document.querySelector('.view_header p').innerHTML = "Menu List";
        document.querySelector('.view_header p').style.color = "#e67e22";
        document.querySelector('.js_close_table').style.color = "black";
        showMenuTable(result);
      }
    })
    // .catch (error => {alert('Server error, contact the site administrator.')});
}

// User signup
function signUp() {
  //Get the login form data
  var name = document.querySelector("#suname").value;
  var email = document.querySelector("#suemail").value;
  var password = document.querySelector("#supsw").value;
  var password2 = document.querySelector("#supsw2").value;

  // Ensure passwords match
  if (password === password2) {
    // create the form data object
    var formData = new FormData();
    formData.append('User_Name', name);
    formData.append('User_Email', email);
    formData.append('User_Password', password);

    // Create login request data object
    const url = 'http://127.0.0.1:5000/v1/auth/signup'
    var requestData = new Request(url, {
      method: 'POST',
      body: formData,
      headers: new Headers(),
      mode: 'cors',
      cache: 'default'}
    );

    // Send login request
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
        openCloseLoginModal('closeSignUpModal');
        idValue = document.querySelector('.modal_login').getAttribute('id');
        let msg = data.Response.Success
        alert(msg);
        openCloseLoginModal('openLoginModal', idValue);
      })
      // .catch (error => {alert('Server error, contact the site administrator.')});
  } else {document.querySelector('#splabel').style.color = "red";} 
}

// User login
var header;
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

      if (idValue === 'admin') {
        var fetchData = new Request('http://127.0.0.1:5000/v1/menus', requestData);
          
        fetch(fetchData)
          .then(response => {
            if (response.status === 200) {
              openCloseLoginModal('closeLoginModal');
              document.querySelector('.admin_section').style.display = "block";
            } else if (response.status === 401) {
              document.querySelector('#alabel').style.color = "red";
            }
          })
      } else if (idValue === 'prev_ord') {
        var fetchData = new Request('http://127.0.0.1:5000/v1/users/orders', requestData);

        fetch(fetchData)
        .then(response => {
          if (response.status === 200) {
            openCloseLoginModal('closeLoginModal');
            //open the previous order modal

          } else if (response.status === 401) {
            document.querySelector('#alabel').style.color = "red";
          }
        })
      } else if (idValue === 'checkout') {
        var fetchData = new Request('http://127.0.0.1:5000/v1/users/orders', requestData);

        fetch(fetchData)
        .then(response => {
          if (response.status === 200) {
            openCloseLoginModal('closeLoginModal');
            //open the checkout order modal

          } else if (response.status === 401) {
            document.querySelector('#alabel').style.color = "red";
          }
        })
      }
    })
    // .catch (error => {alert('Server error, contact the site administrator.')});
}

 /*----------HELPER FUNCTIONS---------*/
 // Close tables displayed in the admin dash
function closeTables (tableId) {

  if (tableId === '#menu_table') {
    // document.querySelector('#menu_table').style.display = 'none';
    let table = document.querySelector("#menu_table");
    rows = table.rows.length
    var i;
    for (i = 0; i <= (rows - 1); i++) {
      table.deleteRow(i);
    }
  }  

}
 
 // Inputs/Labels reset function
function resetLoginModal (action) {
  //Clear login fields
  emailLabel = document.querySelector("#elabel");
  passwordLabel = document.querySelector("#plabel");
  emailInput = document.querySelector("#uemail");
  passwordInput = document.querySelector("#upsw");
  authLabel = document.querySelector('#alabel');

  //clear signup fields
  s_nameInput = document.querySelector("#suname");
  s_emailLabel = document.querySelector("#selabel");
  s_emailInput = document.querySelector("#suemail");
  s_passwordLabel = document.querySelector("#splabel");
  s_passwordInput = document.querySelector("#supsw");
  s2_passwordInput = document.querySelector("#supsw2");

  if (action == 'clearLoginForm') {
    authLabel.style.color = '';
    emailLabel.style.color = ''
    passwordLabel.style.color = ''
    emailInput.value = ''
    passwordInput.value = ''

  } else if (action == 'resetLoginEmail') {
    if (emailLabel.style.color == 'red') {
      emailLabel.style.color = '';
    } else if (authLabel.style.color == 'red') {
      authLabel.style.color = '';
    }

  } else if (action == 'resetLoginPassword') {
      if (passwordLabel.style.color == 'red') {
        passwordLabel.style.color = '';
      }

  } else if (action == 'clearSignupForm') {
    s_nameInput.value = '';
    s_emailLabel.style.color = '';
    s_emailInput.value = '';
    s_passwordLabel.style.color = '';
    s_passwordInput.value = '';
    s2_passwordInput.value = '';

  } else if (action == 'resetSignupEmail') {
    if (s_emailLabel.style.color == 'red') {
      s_emailLabel.style.color = '';
    }

  } else if (action == 'resetSignupPassword') {
    if (s_passwordLabel.style.color == 'red') {
      s_passwordLabel.style.color = '';
    }
  }
}

// Show|Close login form function
function openCloseLoginModal (action, source) {
  modalLogin = document.querySelector(".modal_login");
  modalSignup = document.querySelector(".modal_signup");

  if (action === 'openLoginModal') {
    if (modalLogin.hasAttribute("id")) {
      modalLogin.style.display = "none"
    }
    modalLogin.setAttribute("id", source);
    modalLogin.style.display = "block";
    document.querySelector("#uemail").focus();
    //document.querySelector("#login").style.animation = "slide_from_top 0.7s";
  } else if (action === 'closeLoginModal') { //TODO: Fix modal animation
    //document.querySelector("#login").style.animation = "slide_back_to_top 0.7s";
    if (modalLogin.hasAttribute("id")) {
      modalLogin.removeAttribute("id")
    }
    modalLogin.style.display = "none";
    resetLoginModal('clearLoginForm');
  } else if (action === 'openSignUpModal') {
    modalLogin.style.display = "none";
    resetLoginModal('clearLoginForm');
    modalSignup.style.display = "block";
    document.querySelector("#suname").focus();
  } else if (action === 'closeSignUpModal') {
    modalSignup.style.display = "none";
    resetLoginModal('clearSignupForm');
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