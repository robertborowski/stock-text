$(document).ready(function() {
  // Get the values of the variables in HTML page
  var emailVerifyStatus = $('#email_verify_check').text();
  var phoneVerifyStatus = $('#phone_verify_check').text();

  // If those values do not have length of 0 (blank) then that means account is not 100% verified, so display modal button
  if(emailVerifyStatus.length !== 0 || phoneVerifyStatus.length !== 0) {
    document.getElementById('modalBtn').style.display = 'block';
  } else {
    document.getElementById('modalBtn').style.display = 'none';
  }
});