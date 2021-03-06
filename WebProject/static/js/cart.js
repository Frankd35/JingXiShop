$(function() {
    // 手动输入商品的数量
    $('.itxt').blur(function () {
        // 获取用户输入的数目
        count = Number($(this).val())
        maxnum = Number($(this).attr('maxnum'))
        // 校验count是否合法
        if (isNaN(count) || count < 1) {
            count = 1
        }
        if (count > maxnum){
            count = maxnum
        }
        // 重新设置商品的数目
        $(this).val(count)
        console.log("重新设置商品数量："+count)
        var itGid=$(this).attr('goodid');
        var token = $('[name="csrfmiddlewaretoken"]').attr("value");
        $.ajax({
        url:"/cart",
        type:"POST",
        data:JSON.stringify({'gid':itGid,'flag':'updatenum', "csrfmiddlewaretoken": token, 'num': count}),
        dataType : "text"
        })
        // 单个商品数量
        goodprice = Number($(this).attr('goodprice'))
        // 更新单个商品总价
        $("#sumPrice").html((goodprice*count).toFixed(2))
        // 更新商品的总价
        me_sum();
    })

    $(".cart-list ul").mouseover(function() {
        $(this).addClass("active").siblings().removeClass("active");
    });
    $(".cart-th input[type='checkbox']").click(function() {
        if (this.checked) {
            $(".yui3-u-3-8 input[type='checkbox']").prop("checked",true);
        }
        else {
            $(".yui3-u-3-8 input[type='checkbox']").prop("checked",false);
        }
        me_sum();
    });

    $("#allSellect").click(function (){
        var isChecked = this.checked;
        var token = $('[name="csrfmiddlewaretoken"]').attr("value");
        $.ajax({
        url:"/cart",
        type:"POST",
        data:JSON.stringify({'flag':'allSellect', 'checked':isChecked, "csrfmiddlewaretoken": token}),
        dataType : "text", async: true
        })
    })

    // 发送ajax POST 请求
    $(".goods-list .plus").click(function() {
        console.log("加一")
        var itGid=$(this).attr('goodid');
        var token = $('[name="csrfmiddlewaretoken"]').attr("value");
        $.ajax({
        url:"/cart",
        type:"POST",
        data:JSON.stringify({'gid':itGid,'flag':'plus', "csrfmiddlewaretoken": token}),
        dataType : "text"
        })
    });
    $(".goods-list .mins").click(function() {
        console.log("减一")
        var itGid=$(this).attr('goodid');
        var token = $('[name="csrfmiddlewaretoken"]').attr("value");
        $.ajax({
        url:"/cart",
        type:"POST",
        data:JSON.stringify({'gid':itGid,'flag':'sub', "csrfmiddlewaretoken": token}),
        dataType : "text"
        })
    });

    $(".good-checkbox").click(function() {
        var itGid=$(this).attr('goodid');
        var checkCon = this.checked;
        var token = $('[name="csrfmiddlewaretoken"]').attr("value");
        $.ajax({
        url:"/cart",
        type:"POST",
        data:JSON.stringify({'gid':itGid,'flag':'check', 'checked':checkCon, "csrfmiddlewaretoken": token}),
        dataType : "text", async: true
        })
        me_sum();
        var flag = true;
        for (var i = 0; i < $(".good-checkbox").length; i++) {
            if (! $(".good-checkbox")[i].checked) {
                flag = false;
                break;
            }
        }
        $(".cart-th input[type='checkbox']").prop("checked",flag);
    });
    $(document).ready(function(){
        me_sum();
    });
    function me_sum() {
        var sum = 0;
        for (var i = 0; i < $(".goods-list").length; i++) {
            if ($(".goods-list").eq(i).children(".yui3-u-1-8").eq(3).children().html() == undefined) {
                console.log($(".goods-list").eq(i).children(".yui3-u-1-8").eq(3).children().html());
                continue;
            }
            else if (! $(".good-checkbox")[i].checked) {
                continue;
            }
            else {
                sum = sum + Number($(".goods-list").eq(i).children(".yui3-u-1-8").eq(3).children().html());
            }
        }
        console.log("hhh");
        console.log(sum);
        $(".summoney span").html(sum.toFixed(2));
    };
    $(".goods-list .plus").click(function() {
        var num = parseInt($(this).siblings(".itxt").val());
        var maxnum = parseInt($(this).attr('maxnum'));
        console.log("maxNUM:"+maxnum)
        console.log("num:"+num)
        if(num+1 <= maxnum){
            num = num + 1;
        }else{
            alert("已达到该商品最大库存")
        }
        var m = $(this).siblings(".itxt").val(Number(num)).val();
        var sum = ($(this).parent().parent().siblings(".yui3-u-1-8").eq(1).children(".price").html() * m).toFixed(2);
        $(this).parent().parent().siblings(".yui3-u-1-8").eq(2).children(".sum").html(sum);
        me_sum();

    });
    $(".goods-list .mins").mouseover(function() {
        if ($(this).siblings(".itxt").val() <= 1) {
            $(this).css("cursor","not-allowed");
        }
        else {
            $(this).css("cursor","pointer");
        }
    });
    $(".goods-list .mins").click(function() {
        if ($(this).siblings(".itxt").val() <= 1) {
            $(this).css("cursor","not-allowed");
        }
        else {
            $(this).css("cursor","pointer");
            num =  $(this).siblings(".itxt").val();
            $(this).siblings(".itxt").val(num-1);
            var m = $(this).parent().parent().siblings(".yui3-u-1-8").eq(1).children(".price").html();
            var sum = $(this).parent().parent().siblings(".yui3-u-1-8").eq(2).children(".sum").html();
            $(this).parent().parent().siblings(".yui3-u-1-8").eq(2).children(".sum").html((sum - m).toFixed(2));
            me_sum();
        }
    });
    $(".del1 a").click(function() {
        var r = confirm("确认删除该商品？");
        if (r == true) {
            console.log("删除商品")
            var itGid=$(this).attr('goodid');
            var token = $('[name="csrfmiddlewaretoken"]').attr("value");
            $(this).parent().parent().siblings().remove();
            $(this).parent().parent().remove();
            $(this).closest('.goods-list').remove();
            $.ajax({
            url:"/cart",
            type:"POST",
            data:JSON.stringify({'gid':itGid,'flag':'delete', "csrfmiddlewaretoken": token}),
            dataType : "text"
            })
        } else {
            console.log("取消删除")
        }

        me_sum();
    });
    $(".sumbtn a").click(function (){
        console.log("我被点了")
        window.location.replace("/order")
    })
});