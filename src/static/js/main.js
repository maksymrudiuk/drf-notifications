$(document).ready(function () {
  getFirebaseToken();
})

function getFirebaseToken() {
  var firebaseConfig = {
    apiKey: "AIzaSyDQjj-V1U9H-gepiij_NfJNvvNXRYi04Rk",
    authDomain: "drf-notifications.firebaseapp.com",
    databaseURL: "https://drf-notifications.firebaseio.com",
    projectId: "drf-notifications",
    storageBucket: "drf-notifications.appspot.com",
    messagingSenderId: "365894588527",
    appId: "1:365894588527:web:1d1b91d1121d9993ad159a"
  };
  // Initialize Firebase
  firebase.initializeApp(firebaseConfig);

  navigator.serviceWorker.register('/static/js/firebase-messaging-sw.js').then(function (registration) {
    const messaging = firebase.messaging();
    messaging.usePublicVapidKey("BNq-Q4V6JFzX-hZpbQtPWq3VGHWA2FFRAs44LUFXsdkHnSJvOzGhY262XUcH-G8M1FICQtd5dp9EP_HP6jYx5ug");
    messaging.requestPermission().then(function () {
      messaging.getToken().then((currentToken) => {
        if (currentToken) {
          console.log('Current token.', currentToken)
        } else {
          console.log('No Instance ID token available. Request permission to generate one.');
        }
      }).catch((err) => {
        console.log('An error occurred while retrieving token. ', err);
      });
    });
  });
}
