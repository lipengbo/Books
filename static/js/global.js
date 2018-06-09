function setCookie(cname,cvalue,exdays)
{
  let d = new Date();
  d.setTime(d.getTime()+(exdays*24*60*60*1000));
  let expires = "expires="+d.toGMTString();
  document.cookie = cname + "=" + cvalue + "; " + expires;
}

function getCookie(cname)
{
  let name = cname + "=";
  let ca = document.cookie.split(';');
  for(let i=0; i<ca.length; i++)
  {
    let c = ca[i].trim();
    if (c.indexOf(name)===0) return c.substring(name.length,c.length);
  }
  return "";
}


$(function () {
    let user = $("#user");
    if((getCookie("name")) && !document.getElementById("userMenu")){
        $.ajax({
            url: "/users/1/",
            success: function (data, status) {
                let name = data.first_name || data.username;
                let user = $("#user");
                user.addClass("profile");
                user.find("li:first a").empty().append('<img class="img-circle" src='+ data.image +'>'+ name +'<b class="caret"></b><span class="fa fa-envelope pull-right message" style="font-size:1.5em"><span class="navbar-unread count">10</span></span>');
                user.find("li:first").append('<ul id="userMenu" class="dropdown-menu" style="display:none"><li class="divider"></li><li><a href="/user/account">账号设置 <span class="glyphicon glyphicon-cog pull-right"></span></a></li><li class="divider"></li><li><a href="/user/logout" id="logout">安全退出 <span class="glyphicon glyphicon-log-out pull-right"></span></a></li></ul>');
                user.remove("li:even")
            },
        })
    }
    else{
        if (user.hasClass("profile")){user.removeClass("profile")}
        user.append('<li id="userInfo" class="dropdown"><a href="/user/login"><i class="fa fa-sign-in"></i>  登录</a></li>');
        user.append('<li><a href="/user/register"><i class="fa fa-pencil"></i>  注册</a></li>');
    }
});

$(function(){
    //刷新验证码
    $(".captcha").click(function(){
        $.get("/captcha/refresh/?"+Math.random(), function(result){
                $("#id_captcha_1").val('').focus();
                $('.captcha').attr("src",result.image_url);
                $('#id_captcha_0').attr("value",result.key);
            });
    });
    $("#logout").click(function () {
        document.cookie = "";
        window.location.href = '/'
    });
});

