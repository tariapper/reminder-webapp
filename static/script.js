function ajaxGetRequest(path, callback) {
    let request = new XMLHttpRequest();
    request.onreadystatechange = function () {
      if (this.readyState === 4 && this.status === 200) {
        callback(this.response);
      }
    }
    request.open("GET", path);
    request.send();
}
function ajaxPostRequest(path, data, callback){
  let request = new XMLHttpRequest();
  request.onreadystatechange = function(){
    if (this.readyState === 4 && this.status === 200){
      callback(this.response);
    }
  };
  request.open("POST", path);
  request.send(data);
}

function userLogin(){
    let username = document.getElementById('username').value;
    let password = document.getElementById('password').value;
    document.getElementById('username').value='';
    document.getElementById('password').value='';
    let userPwDictionary = {"username":username, "password":password}
    ajaxPostRequest("/userLogin", JSON.stringify(userPwDictionary), none);
    function none(data){
      //let jsonned=JSON.parse(data);
      //console.log(jsonned)
      //Plotly.newPlot("fullPieDiv",jsonned,{"title":"Percentage of People Homeless in NYC by Borough: 2009"});
    }
}