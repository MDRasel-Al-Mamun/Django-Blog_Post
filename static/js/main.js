// Form validation

$(document).ready(function () {
  $('#validation-form').validate({
    rules: {
      first_name: 'required',
      last_name: 'required',
      username: {
        required: true,
        minlength: 8,
      },
      email: {
        required: true,
        email: true,
      },
      old_password: 'required',
      password: {
        required: true,
        minlength: 8,
      },
      confirm_password: {
        required: true,
        equalTo: '#passwordField',
      },
    },
    messages: {
      firstname: 'Please enter your first name',
      lastname: 'Please enter your last name',
      username: {
        required: 'Please enter a username',
        minlength: 'Your username must consist of at least 8 characters',
      },
      email: 'Please enter a valid email address',
      old_password: 'Please enter your current password',
      password: {
        required: 'Please provide a password',
        minlength: 'Your password must be at least 8 characters long',
      },
      confirm_password: {
        required: 'Confirm your password',
        equalTo: 'Password not match',
      },
    },
    errorElement: 'em',
    errorPlacement: function (error, element) {
      // Add the `invalid-feedback` class to the error element
      error.addClass('invalid-feedback');

      if (element.prop('type') === 'checkbox') {
        error.insertAfter(element.next('label'));
      } else {
        error.insertAfter(element);
      }
    },
    highlight: function (element, errorClass, validClass) {
      $(element).addClass('is-invalid').removeClass('is-valid');
    },
    unhighlight: function (element, errorClass, validClass) {
      $(element).addClass('is-valid').removeClass('is-invalid');
    },
  });

  // Password Strength Check

  if ($.fn.passwordStrength) {
    $('#passwordField').passwordStrength({
      minimumChars: 8,
    });
  }
  // Image File Upload

  $('#fileupload').change(function (event) {
    var x = URL.createObjectURL(event.target.files[0]);
    $('#upload-img').attr('src', x);
    console.log(event);
  });
});

// Search AutoComplete

$(function () {
  $('#query').autocomplete({
    source: '/blog/search_auto/',
    select: function (event, ui) {
      AutoCompleteSelectHandler(event, ui);
    },
    minLength: 2,
  });
});

function AutoCompleteSelectHandler(event, ui) {
  var selectedObj = ui.item;
}

// Sign Up Authentication

const usernameField = document.querySelector('#usernameField');
const feedBackArea = document.querySelector('.usernameFeedBackArea');
const emailField = document.querySelector('#emailField');
const emailFeedBackArea = document.querySelector('.emailFeedBackArea');

usernameField.addEventListener('keyup', (e) => {
  const usernameVal = e.target.value;

  usernameField.classList.remove('is-invalid');
  feedBackArea.style.display = 'none';

  if (usernameVal.length > 0) {
    fetch('/authentication/validate_username', {
      body: JSON.stringify({ username: usernameVal }),
      method: 'POST',
    })
      .then((res) => res.json())
      .then((data) => {
        if (data.username_error) {
          usernameField.classList.add('is-invalid');
          feedBackArea.style.display = 'block';
          feedBackArea.innerHTML = `<p style="color:red";>${data.username_error}</p>`;
        }
      });
  }
});

emailField.addEventListener('keyup', (e) => {
  const emailVal = e.target.value;

  emailField.classList.remove('is-invalid');
  emailFeedBackArea.style.display = 'none';

  if (emailVal.length > 0) {
    fetch('/authentication/validate_email', {
      body: JSON.stringify({ email: emailVal }),
      method: 'POST',
    })
      .then((res) => res.json())
      .then((data) => {
        if (data.email_error) {
          emailField.classList.add('is-invalid');
          emailFeedBackArea.style.display = 'block';
          emailFeedBackArea.innerHTML = `<p style="color:red";>${data.email_error}</p>`;
        }
      });
  }
});
