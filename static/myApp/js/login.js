layui.use('layer', function(){
  var layer = layui.layer;
});


function doLogin() {
    var account_element = document.getElementById("account"),
        password_element = document.getElementById("password");
    var account = account_element.value.replace(/\s+/g,""),
        password =  password_element.value.replace(/\s+/g,"");
    if(account == "" || password == ""){
        account_element.className = "empty";
        password_element.className = "empty"
        return false;
    }else{
        account_element.className = "";
        password_element.className = "";
    }
    var xhr=new XMLHttpRequest();
    xhr.open("post","/doLogin/",true);
    xhr.setRequestHeader('content-type', 'application/x-www-form-urlencoded');
    xhr.send("account="+account+"&password="+password+"&auth=1");
    xhr.onreadystatechange = function () {
      if (xhr.readyState==4 && xhr.status == 200){
          if(xhr.responseText == "ok"){
              console.log('123')
              window.location.href="/myApp/Admin/ctl";
          }else{
              layer.open({
                  title: '提示',
                  content: '账号或密码错误，请重新输入！'
              });
          };
       };
    };
    return false;
};

