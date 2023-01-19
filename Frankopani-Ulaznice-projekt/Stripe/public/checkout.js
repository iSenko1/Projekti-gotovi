// This is a public sample test API key.
// Don’t submit any personally identifiable information in requests made with this key.
// Sign in to see your own test API key embedded in code samples.
const stripe = Stripe("pk_test_51K6tdwAXKEmEy22JkAD3kC4pGJ7K3jtBjwQARLgiQJljwH1VTcjB7WZj8Goo9aBmoJdOz7nNfE53pCdkKB1cpMv100vGlYZ1Dx");

// The items the customer wants to buy
const items = [{ id: "xl-tshirt" }];

let elements;

initialize();
checkStatus();

document
  .querySelector("#payment-form")
  .addEventListener("submit", handleSubmit);

var emailAddress = '';
// Fetches a payment intent and captures the client secret
async function initialize() {
  const response = await fetch("/create-payment-intent", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ items }),
  });
  const { clientSecret } = await response.json();

  const appearance = {
    theme: 'stripe',
    variables: {
      colorPrimary: '#d60000',
      colorBackground: '#c7c7c7',
    },
  };
  elements = stripe.elements({ appearance, clientSecret });

  const linkAuthenticationElement = elements.create("linkAuthentication");
  linkAuthenticationElement.mount("#link-authentication-element");

  linkAuthenticationElement.on('change', (event) => {
    emailAddress = event.value.email;
  });

  const paymentElementOptions = {
    layout: "tabs",
  };

  const paymentElement = elements.create("payment", paymentElementOptions);
  paymentElement.mount("#payment-element");
}


async function handleSubmit(e) {
  e.preventDefault();
  setLoading(true);

  //----------------------------------------------------------------
  // Fetch the data from the other HTML file
  ///../index.html
  // const response = await fetch('http://127.0.0.1:5500/index.html');
  // const data = await response.text();
  
  // // Extract the values you want to save
  // const ticketPrice = $(data).find('.ticketBox').attr('data-ticket-price');
  // const imeKarte = $(data).find('.ticketBox').find('.naslov-karte').html();
  
  // // Send a POST request to the server to save the data to a JSON file
  // const saveResponse = await fetch('/save-to-json', {
  //   method: 'POST',
  //   body: JSON.stringify({ticketPrice, imeKarte}),
  //   headers: { 'Content-Type': 'application/json' },
  // });

  // // Check if the server was able to save the data
  // if (!saveResponse.ok) {
  //   console.error('Failed to save data to JSON file');
  // }

  // let data1 = window.localStorage.getItem('blagajna');
  // console.log(data1);
  //----------------------------------------------------------------

  const { error } = await stripe.confirmPayment({
    elements,
    confirmParams: {
      // Make sure to change this to your payment completion page
      // if total > 50
      return_url: "https://frankopani.eu/frankopani/",
      receipt_email: emailAddress,
    },
  });

  // This point will only be reached if there is an immediate error when
  // confirming the payment. Otherwise, your customer will be redirected to
  // your `return_url`. For some payment methods like iDEAL, your customer will
  // be redirected to an intermediate site first to authorize the payment, then
  // redirected to the `return_url`.
  if (error.type === "card_error" || error.type === "validation_error") {
    showMessage(error.message);
  } else {
    showMessage("An unexpected error occurred.");
  }

  setLoading(false);
}

// Fetches the payment intent status after payment submission
async function checkStatus() {
  const clientSecret = new URLSearchParams(window.location.search).get(
    "payment_intent_client_secret"
  );

  if (!clientSecret) {
    return;
  }

  const { paymentIntent } = await stripe.retrievePaymentIntent(clientSecret);

  switch (paymentIntent.status) {
    case "succeeded":
      showMessage("Payment succeeded!");
      break;
    case "processing":
      showMessage("Your payment is processing.");
      break;
    case "requires_payment_method":
      showMessage("Your payment was not successful, please try again.");
      break;
    default:
      showMessage("Something went wrong.");
      break;
  }
}

// ------- UI helpers -------

function showMessage(messageText) {
  const messageContainer = document.querySelector("#payment-message");

  messageContainer.classList.remove("hidden");
  messageContainer.textContent = messageText;

  setTimeout(function () {
    messageContainer.classList.add("hidden");
    messageText.textContent = "";
  }, 4000);
}

// Show a spinner on payment submission
function setLoading(isLoading) {
  if (isLoading) {
    // Disable the button and show a spinner
    document.querySelector("#submit").disabled = true;
    document.querySelector("#spinner").classList.remove("hidden");
    document.querySelector("#button-text").classList.add("hidden");
  } else {
    document.querySelector("#submit").disabled = false;
    document.querySelector("#spinner").classList.add("hidden");
    document.querySelector("#button-text").classList.remove("hidden");
  }
}