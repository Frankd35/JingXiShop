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
        data:JSON.stringify({'id':itGid, flag:"puton", "csrfmiddlewaretoken": token}),
        dataType : "text",
        success: function(data){
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
        data:JSON.stringify({'id':itGid, flag:"putoff","csrfmiddlewaretoken": token}),
        dataType : "text",
        success: function(data){
            window.location.reload()
        }
        })
    });
    
     $('.itxt').blur(function () {
         // 获取用户输入的数目
         count = Number($(this).val())
         // 重新设置商品的数目
         $(this).val(count)
         console.log("重新设置商品数量："+count)
         var itGid=$(this).attr('goodid');
         var token = $('[name="csrfmiddlewaretoken"]').attr("value");
         $.ajax({
         url:"/merchant_object",
         type:"POST",
         data:JSON.stringify({'id':itGid,'flag':'updatenum', "csrfmiddlewaretoken": token, 'num': count}),
         dataType : "text",
         success: function(data){
            console.log('return successful')
            window.location.reload()
         }
         })

       })

       $('.iprice').blur(function () {
        // 获取用户输入的单价
        count = Number($(this).val())
        // 重新设置商品的单价
        $(this).val(count)
        console.log("重新设置商品单价："+count)
        var itGid=$(this).attr('goodid');
        var token = $('[name="csrfmiddlewaretoken"]').attr("value");
        $.ajax({
        url:"/merchant_object",
        type:"POST",
        data:JSON.stringify({'id':itGid,'flag':'updateprice', "csrfmiddlewaretoken": token, 'price': count}),
        dataType : "text",
        success: function(data){
           console.log('return successful')
           window.location.reload()
        }
        })

      })
});