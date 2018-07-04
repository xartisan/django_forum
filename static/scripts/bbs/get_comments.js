/**
 * Created by qimi on 2016/6/9.
 */

function getComments() {
    $.get(
        "{% url 'bbs:get_comments' article_obj.id %}",
        //"/bbs/get_comments/1/",
        function(callback) {
            console.log(callback);
            //$(".comment-list").html(callback);
        }
    ); //end get
}

function getCsrf() {
    return $("input[name='csrfmiddlewaretoken']").val();
}

$(document).ready(function() {
    $(".comment-form-box button").click(function () {  // 给发表评论的按钮绑定事件
        var comment_text = $(".comment-form-box textarea").val();  //获得评论内容
        if (comment_text.trim().length < 5) {
            alert("客官，五字起评，不议价。");
        }else {
            //post
            $.post("{% url 'bbs:post_comment' %}",
                {
                    'comment_type': 1,
                    article_id: "{{ article_obj.id }}",
                    parent_comment_id: null,
                    'comment': comment_text.trim(),
                    'csrfmiddlewaretoken': getCsrf()
                },  // end post args
                function(callback) {
                    console.log(callback);
                    if (callback == 'OK') {
                        alert("post comment success!");
                    }
                }
            );  // end post
        }
    });  //end button click
    $("#get-comments").click(function() {
        console.log("点击获取评论");
        getComments();
    })
}); // end document ready