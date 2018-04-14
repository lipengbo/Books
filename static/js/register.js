$(function() {
    $("#registerForm").validate({
        rules: {
            username: {
                required: true,
                email: true,
                 remote: {
                    url: "/emailcodes/1/",     //后台处理程序
                    type: "get", //数据发送方式
                    data:{
                        "csrfmiddlewaretoken": function(){
                            return $("[name='csrfmiddlewaretoken']").val();
                        },
                        "send_type": "register",
                    },
                    }
            },
            password: {
                required: true,
                rangelength: [8, 20],
            },
            confirmPassword: {
                required: true,
                minlength: 8,
                equalTo: "[name='password']"
            },
            verify: {
                required: true,
                minlength: 4,
                maxlength: 4,
                remote: {
                    url: "/emailcodes/",     //后台处理程序
                    type: "get", //数据发送方式
                    data:{
                            "username": function(){if($("#registerForm div:first").hasClass('has-success')){
                                return $("#email").val();
                            }},
                            "csrfmiddlewaretoken": function(){
                            return $("[name='csrfmiddlewaretoken']").val();
                        },
                            "send_type": "register",
                        },
                    }
                },
            },
        message: {
            username: {
                required: "请输入合法的邮箱",
                email: "请输入合法的邮箱",
                remote: "用户没有注册",
            },
            password: {
                required: "请输入密码",
                rangelength: "密码至少包一个大写字母、一个小写字母及一个符号，长度至少8位",
            },
            confirmPassword: {
                required: "请确认密码",
                equalTo: "两次密码输入不一致"
            },
            verify: {
                required: true,
                minlength: '验证码不正确',
                maxlength: "验证码不正确",
                remote: "验证码不正确",
            },
        },
        errorClass: 'has-error',
        errorElement: "small",
        focusCleanup: true,
        keyup: true,
        success: function (element) {
            element.parent().parent().removeClass('has-error');
            element.parent().parent().addClass('has-success');
            element.parent().children("i").removeClass('glyphicon-remove');
            element.parent().children("i").addClass('glyphicon-ok');
            element.parent().children('small').remove()
        },
        errorPlacement: function (error, element) {
            element.parent().parent().parent().removeClass('has-success');
            element.parent().parent().children("i").removeClass('glyphicon-ok');
            element.parent().parent().children("i").addClass('glyphicon-remove');
            element.parent().parent().parent().addClass('has-error');
            element.parent().parent().append(error);
            element.parent().parent().children('small').addClass("alert alert-danger")
        },
        submitHandler:function (form) {
            $.ajax({url:"/users/",
                type:"POST",
                data:$(form).serialize(),
                success: function (data, status) {
                    $.cookie('token', data.token, {
                        path: '/',
                        expired: 1,
                    });
                    window.location.href = '/years/';
                },
                error: function (data, status) {
                    alert("服务器错误，请稍后重试！")
                }
        });
        },
    });
});



$(function () {

    $("#sendcode").click(function(){
        if ($("#registerForm div:first").hasClass('has-success')){
            $.ajax({
            url: "/emailcodes/",
            type: 'POST',
            data: {
                'username': $("[name=username]").val(),
                'send_type':"register",
                "csrfmiddlewaretoken": function () {
                   return $.cookie('csrftoken')
                }

            },
            success: function(data, status){
                alert(data.msg)
            },
            error: function (data, status) {
                alert(data.msg);
            }

        })
        }
    })
});


