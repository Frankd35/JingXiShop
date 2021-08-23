$(function() {
	    // 发送ajax POST 请求
    	$(".order_submit a").click(function() {
        console.log("hhh")
        var itGid=$(this).attr('goodid');
        var token = $('[name="csrfmiddlewaretoken"]').attr("value");
        $.ajax({
        url:"/cart",
        type:"POST",
        data:JSON.stringify({'gid':itGid,'flag':'plus', "csrfmiddlewaretoken": token}),
        dataType : "text"
        })
        });
});