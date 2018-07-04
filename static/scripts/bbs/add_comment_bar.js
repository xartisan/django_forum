// 添加评论

function add_comment_bar() {
    console.log("go into add_comment_bar function...");
    var thumb_num = $("#article-title").attr("thumb-num");
    var comment_bar = "<small class='comment-bar pull-right'>" +
        "<a style='cursor: pointer' class='margin-left-twenty' comment-type='2'><i class='fa fa-thumbs-o-up fa-fw'></i>" +
        thumb_num + "</a>" +
        "<a style='cursor: pointer' class='margin-left-twenty' comment-type='1'>回复</a>" +
        "</small>";
    $(".media-heading").each(function () {
        $(this).append(comment_bar);
    });  //end add comment_bar
    $(".comment-bar a").each(function () {
        $(this).click(function () {
            if ($(this).attr('comment-type') == '2') {  //点赞



            } else {  //评论
                let parent_comment_id = $(this).parent().parent().attr('comment-id');
                var input_html = `<form style="margin-bottom: 10px"> 
                    <input type="hidden" name="parent_comment_id" value=${parent_comment_id}> 
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