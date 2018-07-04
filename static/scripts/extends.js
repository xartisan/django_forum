/**
 * Created by qimi on 2016/4/17.
 */
(function(arg) {
    //提示指定错误信息
    function errorMessage(container, msg) {
        //确保同时只出现一个错误提示消息
        if (!container.parent().attr("hasError") || container.parent().attr("hasError") == "false") {
            var temp = '<div class="my-alert alert-danger" role="alert">'+msg+'</div>';
            container.parent().after(temp);
            container.parent().attr("hasError", "true");
        }
        //闪烁出现错误的输入框
        shake(container, "red", 2);
        //该输入框获得焦点之后去掉错误提示
        container.focus(function() {
            container.parent().next(".my-alert").remove();
            container.parent().attr("hasError", "false");
        })
    }
    //闪烁提示
    function shake(ele,cls,times) {
        var i = 0,t=null,o=ele.prop("class")+ " ",c="",times=times||2;
        if (t) return;
        t = setInterval(function() {
            i++;
            c = i%2 ? o+cls : o;
            ele.prop("class", c);
            if (i==2*times) {
                clearInterval(t);
                ele.removeClass(cls);
            }
        }, 500);
    }
    //检测输入有效性的扩展
    //debugger;
    arg.extend({
        MyCheckValidity: function(arg) {
            var name_map = {
                email: "邮箱",
                username: "用户名",
                password: "密码",
                repeat_password: "确认密码",
                hostname: "主机名",
                ip: "IP地址",
                port: "端口"
            };
            var flag = true;
            //找到form下的所有class为input-group的input标签
            $(arg).find("input").each(function() {
                //获取到内容
                var name = $(this).prop("name");
                var name_str = name_map[name];
                var value = $(this).val();
                //如果input为空
                if (!value || value.trim() == "") {
                    errorMessage($(this),name_str+"不能为空");
                    flag = false;
                    return false;
                }
                //如果是邮箱，就按照邮箱的规则匹配值
                if (name == "email") {
                    var re_mail = /^([a-z.0-9]{1,26})@([a-z.0-9]{1,20})(.[a-z0-9]{1,8})$/;
                    if (!re_mail.test(value)) {
                        flag = false;
                        errorMessage($(this), name_str+"无效");
                        return false;
                    }
                }
                if (name == "username") {
                    if (value.length < 4) {
                        flag = false;
                        errorMessage($(this), name_str+"长度必须大于4");
                        return false;
                    }
                    if (value.length > 26) {
                        flag = false;
                        errorMessage($(this, name_str+"长度不能超过26"))
                    }
                }
                if (name == "password") {
                    if (value.length < 6) {
                        flag = false;
                        errorMessage($(this), name_str+"长度必须大于6");
                        return false;
                    }
                }
                //判断主机名
                if (name == "hostname") {
                    if (value.length > 255) {
                        flag = false;
                        errorMessage($(this), name_str+"过长");
                        return false;
                    }
                }
                //判断IP
                if (name == "ip") {
                    var re_ip = /^(25[0-5]|2[0-4]\d|[0-1]?\d?\d)(\.(25[0-5]|2[0-4]\d|[0-1]?\d?\d)){3}$/;
                    if (!re_ip.test(value)) {
                        flag = false;
                        errorMessage($(this), name_str+"无效");
                        return false;
                    }
                }
                //判断端口
                if (name == "port") {
                    var re_port = /^(\d)+$/;
                    if (re_port.test(value)) {
                        value = parseInt(value);
                        if (value > 65535) {
                            flag = false;
                            errorMessage($(this), name_str+"无效");
                            return false;
                        }
                    } else {
                        flag = false;
                        errorMessage($(this), name_str+"必须为数字");
                        return false;
                    }
                }
            });
            //一个验证通过的标志位，可用于判断是否继续下一步
            return flag;
        }
    })
})($);