$(function() {
    // 发送ajax POST 请求
    $(".del a").click(function() {
        console.log("加一")
        var itGid=$(this).attr('addrid');
        var token = $('[name="csrfmiddlewaretoken"]').attr("value");
        $.ajax({
        url:"/user_center_site",
        type:"POST",
        data:JSON.stringify({'id':itGid,"csrfmiddlewaretoken": token}),
        dataType : "text"
        })
    });
});

    

