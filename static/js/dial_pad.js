var count = 0;
var active_digit = '';
var timer_active = 0;
var index = 0;

var one = ["1"];
var two = ["2","a","b","c",];
var three = ["3","d","e","f"];
var four = ["4","g","h","i"];
var five = ["5","j","k","h"];
var six = ["6","m","n","o"];
var seven = ["7","p","q","r","s"];
var eight = ["8","t","u","v"];
var nine = ["9","w","x","y","z"];
var star = ["*"];
var zero = ["0"];
var hash = ["#"];


$(".digit").on('click', function() {
  var num = ($(this).clone().children().remove().end().text());

  if (num !== active_digit){
    //Update active digit
    active_digit = num;
    timer_active = 0;
    index = 0;
    //Start timer
    timer();
    //
    if (count < 11) {
      var digit = dictionary(num.trim());
      $("#output").append('<span>' + digit + '</span>');
      count++;
    }
  }
  else if (num === active_digit ){
      //Update last value
      if (count < 11) {
        var digit = dictionary(num.trim());
        $('#output span:last-child').replaceWith('<span>' + digit + '</span>');
        }
    }
});

$('.btn-danger').on('click', function() {
  timer_active = 0;
  active_digit = '';
  index = 0;
  $('#output span:last-child').remove();
  count--;
});

$('.btn-success').on('click', function() {
  timer_active = 0;
  active_digit = '';
  index = 0;

  //Set output values to hidden form id
  prepareDiv();

  //Send Request
  var form = document.getElementById('formId');
  form.submit();

  //Clear Text
  let len = $('#output span').length;
  for (let i = 0; i < len; i++){
    $('#output span:last-child').remove();
  }

  count--;
});

function timer(){
  timer_active = 1;
  // Set the date we're counting down to
  var countDownDate = new Date();
  countDownDate.setSeconds(countDownDate.getSeconds() + 5);

  // Update the count down every 1 second
  var x = setInterval(function() {

    // Get today's date and time
    var now = new Date();

    // Find the distance between now and the count down date
    var distance = countDownDate - now;

    // Time calculations for days, hours, minutes and seconds
    var seconds = Math.floor((distance % (1000 * 60)) / 1000);

    // Output the result in an element with id="demo"
    document.getElementById("response").innerHTML =  seconds + "s ";

    if (timer_active === 0){
      clearInterval(x);
    }

    // If the count down is over, write some text
    if (distance < 0) {
      clearInterval(x);
      timer_active = 0;
      active_digit = '';
      index = 0;
      document.getElementById("response").innerHTML = "EXPIRED";
    }
  }, 1000);
}

function dictionary(num){
  var response = '';
  switch(num){
    case '1':
      //Set text based on index and then increment
      if (one.length === index +1){
        response = one[index];
        index = 0;
      } else {
        response = one[index];
        index ++;
      }
      break;
    case '2':
      if (two.length === index +1){
        response = two[index];
        index = 0;
      } else {
        response = two[index];
        index ++;
      }
      break;
    case '3':
      if (three.length === index +1){
        response = three[index];
        index = 0;
      } else {
        response = three[index];
        index ++;
      }
      break;
    case '4':
      if (four.length === index +1){
        response = four[index];
        index = 0;
      } else {
        response = four[index];
        index ++;
      }
      break;
    case '5':
      if (five.length === index +1){
        response = five[index];
        index = 0;
      } else {
        response = five[index];
        index ++;
      }
      break;
    case '6':
      if (six.length === index +1){
        response = six[index];
        index = 0;
      } else {
        response = six[index];
        index ++;
      }
      break;
    case '7':
      if (seven.length === index +1){
        response = seven[index];
        index = 0;
      } else {
        response = seven[index];
        index ++;
      }
      break;
    case '8':
      if (eight.length === index +1){
        response = eight[index];
        index = 0;
      } else {
        response = eight[index];
        index ++;
      }
      break;
    case '9':
      if (nine.length === index +1){
        response = nine[index];
        index = 0;
      } else {
        response = nine[index];
        index ++;
      }
      break;
    case '0':
      if (zero.length === index +1){
        response = zero[index];
        index = 0;
      } else {
        response = zero[index];
        index ++;
      }
      break;
    case '#':
      if (hash.length === index +1){
        response = hash[index];
        index = 0;
      } else {
        response = hash[index];
        index ++;
      }
      break;
    case '*':
      if (star.length === index +1){
        response = star[index];
        index = 0;
      } else {
        response = star[index];
        index ++;
      }
      break;
    default:
      response = 'default';
      break;
  }
  return response;
}

function prepareDiv() {
    document.getElementById("hidden_text_area").value = document.getElementById("output").innerHTML;
}