$(function() {
    $('.deleteorder a').click(function (){
        var flag = confirm("确认收货？")
        if(flag){
            console.log("确认收货")
            var oid = $(this).attr('oid')
            console.log(oid)
            $.ajax({
                url:"/user_center_order",
                type:"POST",
                data:JSON.stringify({'oid':oid,'flag':'delete'}),
                dataType : "text", async: true,
                success: function (data){
                    location.reload(true)
                }
            })
        }else{
            console.log("取消确认收货")
        }
    })
});