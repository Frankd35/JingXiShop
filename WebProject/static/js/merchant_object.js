$(function() {
    // 发送ajax POST 请求
    $("#put_on").click(function() {
        console.log("上架")
        var itGid=$(this).attr('good_operate1');
        console.log(itGid)
        var token = $('[name="csrfmiddlewaretoken"]').attr("value");
        $.ajax({
        url:"/merchant_object",
        type:"POST",
        data:JSON.stringify({'id':itGid,"csrfmiddlewaretoken": token}),
        dataType : "text",
        success: function(){
            window.location.reload()
        }
        })
    });

	$("#put_off").click(function() {
        console.log("下架")
        var itGid=$(this).attr('good_operate2');
        var token = $('[name="csrfmiddlewaretoken"]').attr("value");
        $.ajax({
        url:"/merchant_object",
        type:"POST",
        data:JSON.stringify({'id':itGid,"csrfmiddlewaretoken": token}),
        dataType : "text",
        success: function(){
            window.location.reload()
        }
        })
    });
    
    $(".clearfix .mins").click(function() {
        console.log("减少")
        var itGid=$(this).attr('goodid');
        var token = $('[name="csrfmiddlewaretoken"]').attr("value");
        $.ajax({
        url:"/merchant_object",
        type:"POST",
        data:JSON.stringify({'id':itGid,'flag':'sub',"csrfmiddlewaretoken": token}),
        dataType : "text",
        success: function(){
            window.location.reload()
        }
        })
    });

    $(".clearfix .plus").click(function() {
        console.log("增加")
        var itGid=$(this).attr('goodid');
        var token = $('[name="csrfmiddlewaretoken"]').attr("value");
        $.ajax({
        url:"/merchant_object",
        type:"POST",
        data:JSON.stringify({'id':itGid,'flag':'plus',"csrfmiddlewaretoken": token}),
        dataType : "text",
        success: function(){
            window.location.reload()
        }
        })
    });
    $('.itxt').blur(function () {
        // 获取用户输入的数目
        count = Number($(this).val())
        // maxnum = Number($(this).attr('maxnum'))
        // // 校验count是否合法
        // if (isNaN(count) || count < 1) {
        //     count = 1
        // }
        // if (count > maxnum){
        //     count = maxnum
        // }
        // 重新设置商品的数目
        $(this).val(count)
        console.log("重新设置商品数量："+count)
        var itGid=$(this).attr('goodid');
        var token = $('[name="csrfmiddlewaretoken"]').attr("value");
        $.ajax({
        url:"/merchant_object",
        type:"POST",
        data:JSON.stringify({'gid':itGid,'flag':'updatenum', "csrfmiddlewaretoken": token, 'num': count}),
        dataType : "text"
        })

    })
    // $("increment plus").click(function() {
    //     var num = parseInt($(this).siblings(".itxt").val());
    //     var maxnum = parseInt($(this).attr('maxnum'));
    //     console.log("maxNUM:"+maxnum)
    //     console.log("num:"+num)
    //     if(num+1 <= maxnum){
    //         num = num + 1;
    //     }else{
    //         alert("已达到该商品最大库存")
    //     }
    //     var m = $(this).siblings(".itxt").val(Number(num)).val();
    //     var sum = ($(this).parent().parent().siblings(".yui3-u-1-8").eq(1).children(".price").html() * m).toFixed(2);
    //     $(this).parent().parent().siblings(".yui3-u-1-8").eq(2).children(".sum").html(sum);
    //     me_sum();

    // });
    // $("#increment mins").mouseover(function() {
    //     if ($(this).siblings(".itxt").val() <= 1) {
    //         $(this).css("cursor","not-allowed");
    //     }
    //     else {
    //         $(this).css("cursor","pointer");
    //     }
    // });
    // $("#increment mins").click(function() {
    //     if ($(this).siblings(".itxt").val() <= 1) {
    //         $(this).css("cursor","not-allowed");
    //     }
    //     else {
    //         $(this).css("cursor","pointer");
    //         num =  $(this).siblings(".itxt").val();
    //         $(this).siblings(".itxt").val(num-1);
    //         var m = $(this).parent().parent().siblings(".yui3-u-1-8").eq(1).children(".price").html();
    //         var sum = $(this).parent().parent().siblings(".yui3-u-1-8").eq(2).children(".sum").html();
    //         $(this).parent().parent().siblings(".yui3-u-1-8").eq(2).children(".sum").html((sum - m).toFixed(2));
    //         me_sum();
    //     }
    // });
});