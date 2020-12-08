var firebaseConfig = {
    apiKey: "AIzaSyDeqCBSZU99DQ2y1EDOHik7cK4nJSV5zaU",
    authDomain: "fire-bichu136.firebaseapp.com",
    databaseURL: "https://fire-bichu136.firebaseio.com",
    projectId: "fire-bichu136",
    storageBucket: "fire-bichu136.appspot.com",
    messagingSenderId: "721970488521",
    appId: "1:721970488521:web:baac917ccf9f6410921918",
    measurementId: "G-V3ZZRP6960"
  };
  // Initialize Firebase
  firebase.initializeApp(firebaseConfig);
  firebase.analytics();
class CalendarDataAccess{
    // static storage = new firebase.storage()
    constructor(username,password){
        this.storage = firebase.storage()
    };
    getAllData()
    {
        return null
    }
    AddSomeJobs(){
        this.storage.collection("user").add
    }

};