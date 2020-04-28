// Create a Stripe client.

let formdata = document.getElementById("payment-form");
let pub_key = formdata.getAttribute("data-token");

var stripe = Stripe(pub_key);

// Create an instance of Elements.
var elements = stripe.elements();

// Custom styling can be passed to options when creating an Element.
// (Note that this demo uses a wider set of styles than the guide below.)
var style = {
  base: {
    color: "#32325d",
    fontFamily: '"Helvetica Neue", Helvetica, sans-serif',
    fontSmoothing: "antialiased",
    fontSize: "16px",
    "::placeholder": {
      color: "#aab7c4",
    },
  },
  invalid: {
    color: "#fa755a",
    iconColor: "#fa755a",
  },
};

// Create an instance of the card Element.
var card = elements.create("card", { style: style });

// Add an instance of the card Element into the `card-element` <div>.
card.mount("#card-element");

// Handle real-time validation errors from the card Element.
card.addEventListener("change", function (event) {
  var displayError = document.getElementById("card-errors");
  if (event.error) {
    displayError.textContent = event.error.message;
  } else {
    displayError.textContent = "";
  }
});

// Handle form submission.
var form = document.getElementById("payment-form");
form.addEventListener("submit", function (event) {
  event.preventDefault();

  stripe.createToken(card).then(function (result) {
    if (result.error) {
      // Inform the user if there was an error.
      var errorElement = document.getElementById("card-errors");
      errorElement.textContent = result.error.message;
    } else {
      // Send the token to your server.
      stripeTokenHandler(result.token);
      card.clear();
    }
  });
});

// Submit the form with the token ID.
function stripeTokenHandler(token) {
  let endpoint = formdata.getAttribute("action");
  let methods = formdata.getAttribute("method");
  var data = { token: token.id };

  $.ajax({
    url: endpoint,
    method: methods,
    data: data,
    success: function (data) {
      let display = `<div class="row" style="margin-top: 20%;"><div class="col my-auto"><h2>${data.message}</h2></div></>`;

      let container = document.getElementById("payments");
      container.innerHTML = " ";
      container.innerHTML = display;
      setTimeout
      // console.log(data.message);
    },
    error: function () {},
  });

  // Insert the token ID into the form so it gets submitted to the server
}
