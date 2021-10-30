

// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
const firebaseConfig = {
  apiKey: "AIzaSyBSikv78JVQHaQtcxXeq9YV5I9-8GrlxWQ",
  authDomain: "numberdetection-9d030.firebaseapp.com",
  databaseURL: "https://numberdetection-9d030-default-rtdb.asia-southeast1.firebasedatabase.app",
  projectId: "numberdetection-9d030",
  storageBucket: "numberdetection-9d030.appspot.com",
  messagingSenderId: "675075257427",
  appId: "1:675075257427:web:7cf6a00c0f54eeac1d42a6"
};

// Initialize Firebase
firebase.initializeApp(firebaseConfig);

function getdetails() {
firebase.database().ref('Vechical').on('value',(data)=>{
    let Vechical= data.val();
   //  document.getElementById('request').innerHTML = '';
    for(const vech in Vechical)
    {
        if(Vechical[vech].Veichle_id =  document.getElementById('vecid').value )
        {
       document.getElementById('details').innerHTML +=`
       <tr> <th colspan="2"> <h1>Vehicle Details</h1></th></tr>               
       <tr>
       <td>Vehicle_ID     </td> 
       <td> ${Vechical[vech].Veichle_id}</td> 
   </tr>
   <tr>
       <td>Vehicle_Owner     </td>
       <td> ${Vechical[vech].owner}</td>
   </tr>  
   <tr>
        <td>Owner_ADHAR_NO     </td>
        <td> ${Vechical[vech].AdharNo}</td>
   </tr>  
    <tr>
     <td>Vehicle_Class   </td> 
    <td> ${Vechical[vech].Veichle_Class} </td>
    </tr>
   <tr>
       <td>Manufacture       </td>
       <td> ${Vechical[vech].Manufacturer}</td>
   </tr>
   <tr>
      <td>Model            </td> 
      <td> ${Vechical[vech].Model}</td>
   </tr>
   
   <tr>
       <td>Type            </td> 
       <td> ${Vechical[vech].Type}</td>
   </tr> 
   <tr>
       <td>Year            </td> 
       <td> ${Vechical[vech].Year}</td>
    </tr>
   <tr>
       <td> Colour          </td>
       <td> ${Vechical[vech].Colour}</td>
   </tr> 
       ` ;
       break;
        }
    }
})
}