// 添加评论

function add_comment_bar() {
    console.log("go into add_comment_bar function...");
    // var thumb_num = $("#article-title").attr("thumb-num");
    // var comment_bar = "<small class='comment-bar pull-right'>" +
    //     "<a style='cursor: pointer' class='margin-left-twenty' comment-type='2'><i class='fa fa-thumbs-o-up fa-fw'></i>" +
    //     thumb_num + "</a>" +
    //     "<a style='cursor: pointer' class='margin-left-twenty' comment-type='1'>回复</a>" +
    //     "</small>";
    // $(".media-heading").each(function () {
    //     $(this).append(comment_bar);
    // });  //end add comment_bar
    $(".comment-bar a").each(function () {
        $(this).click(function () {
            if ($(this).attr('comment-type') == '2') {  //点赞

                // user likes
                $.post('/comment/like/',
                    {
                        'id': $(this).data('id'),
                        'action': $(this).data('action'),
                        'csrfmiddlewaretoken': getCsrf(),
                    },
                    (data) => {
                        if (data['status'] == 'ok') {
                            var previous_action = $(this).data('action');

                            // toggle data-action
                            console.log(previous_action);
                            $(this).data('action', previous_action == 'like' ? 'unlike' : 'like');
                            // toggle link text
                            // $('a.like').text(previous_action == 'like' ? 'Unlike' : 'Like');

                            // update total likes
                            var previous_likes = parseInt($(this).text());
                            console.log(previous_likes);
                            style_attr = previous_action == 'like' ? 'style="color: red"' : '';
                            $(this).html(`<i ${style_attr} class='fa fa-thumbs-o-up fa-fw'></i>    ` + (previous_action == 'like' ? previous_likes + 1 : previous_likes - 1));
                        }
                    }
                );

            } else {  //评论
                let parent_comment_id = $(this).data('id');
                console.log($(this));
                console.log($(this).data('id'));
                var input_html = `<form style="margin-bottom: 10px" method="post" action="/comment/add/">
                     
                    <input type="hidden" name="parent_comment" value=${parent_comment_id}> 
                    <input type="hidden" name="post" value=${}> 
                    <input type="hidden" name="csrfmiddlewaretoken" value=${getCsrf()}> 
                    <textarea class="form-control" name="body" rows="3"></textarea> 
                    <a class="btn btn-default"><i class="fa fa-angle-double-up fa-fw" aria-hidden="true"></i>收起</a> 
                    <button type="submit" class="btn btn-default pull-right">评论</button> 
                    </form>`;
                $(this).parent().parent().siblings('p').after(input_html);
                $(".fa-angle-double-up").parent().click(function () {  //给收起按钮绑定事件
                    $(this).parent().remove();
                })
            }

        });  //end click function
    });  //end bind click to ".comment-bar a"
}