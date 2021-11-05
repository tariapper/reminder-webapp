$(document).ready(function () {
      $('#data').DataTable({
        "searching": true,
        columns: [{"width":"20%", orderable: true, searchable: false},{"width":"70%",orderable: false, searchable: true},{"width":"10%", orderable: false, searchable: false}],
      });
    });








// function ajaxGetRequest(path, callback) {
//     let request = new XMLHttpRequest();
//     request.onreadystatechange = function () {
//       if (this.readyState === 4 && this.status === 200) {
//         callback(this.response);
//       }
//     }
//     request.open("GET", path);
//     request.send();
// }
// function ajaxPostRequest(path, data, callback){
//   let request = new XMLHttpRequest();
//   request.onreadystatechange = function(){
//     if (this.readyState === 4 && this.status === 200){
//       callback(this.response);
//     }
//   };
//   request.open("POST", path);
//   request.send(data);
// }
//
// function userLogin(){
//     let username = document.getElementById('name').value;
//     let password = document.getElementById('password').value;
//     document.getElementById('name').value='';
//     document.getElementById('password').value='';
//     let userPwDictionary = {"username":username, "password":password}
//     ajaxPostRequest("/userLogin", JSON.stringify(userPwDictionary), identify);
//     //ajaxPostRequest("/userLogin", JSON.stringify(userPwDictionary));
//     function identify(data){
//       //let user = JSON.parse(data).username;
//       //let message = "WELCOME, " + user;
//       //document.getElementById('welcome').innerText=message;
//       //console.log(JSON.parse(data).username);
//       //console.log(JSON.parse(data).password);
//     }
// }
//
// function userRegister(){
//     let username = document.getElementById('name').value;
//     let password = document.getElementById('password').value;
//     document.getElementById('name').value='';
//     document.getElementById('password').value='';
//     let userPwDictionary = {"username":username, "password":password}
//     ajaxPostRequest("/userRegister", JSON.stringify(userPwDictionary), identify);
//     //ajaxPostRequest("/userLogin", JSON.stringify(userPwDictionary));
//     function identify(data){
//       //let user = JSON.parse(data).username;
//       //let message = "WELCOME, " + user;
//       //document.getElementById('welcome').innerText=message;
//       //console.log(JSON.parse(data).username);
//       //console.log(JSON.parse(data).password);
//     }
// }