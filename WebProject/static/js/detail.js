// $(function() {
//     // 计算商品的总价格
//     function update_goods_amount() {
//         // 获取商品的单价和数量
//         price = $('.show_pirze').children('em').text()
//         count = $('.num_show').val()
//         // 计算商品的总价
//         price = parseFloat(price)
//         count = parseInt(count)
//         amount = price * count
//         // 设置商品的总价
//         $('.total').children('em').text(amount.toFixed(2) + '元')
//     }
//
//     $(".reducer").mouseover(function() {
//         if ($(".num_add input[type='text']").val() <= 1) {
//             $(".reducer").css("cursor","not-allowed");
//         }
//         else {
//             $(".reducer").css("cursor","pointer");
//         }
//     });
//     $(".reducer").click(function() {
//         if ($(".num_add input[type='text']").val() <= 1) {
//             $(".reducer").css("cursor","not-allowed");
//         }
//         else {
//             $(".reducer").css("cursor","pointer");
//             var num =  $(".num_add input[type='text']").val()-1;
//             $(".num_add input[type='text']").val(num);
//             update_goods_amount()
//         }
//     });
//     $(".adder").click(function() {
//         console.log("我被点了")
//         var num =  $(".num_add input[type='text']").val() + 1;
//         $(".num_add  input[type='text']").val(Number(num));
//         update_goods_amount()
//     });
// });
$(function() {
    $(".jieshao").click(function () {
        $('.pinglun').removeClass('active')
        $(this).addClass('active')
        $('#tab_detail').show()
        $('#tab_comment').hide()
    })

    $('.pinglun').click(function () {
        $('.jieshao').removeClass('active')
        $(this).addClass('active')
        $('#tab_detail').hide()
        $('#tab_comment').show()
    })

    //update_goods_amount()

    // 计算商品的总价格
    function update_goods_amount() {
        // 获取商品的单价和数量
        price = $('.show_pirze').children('em').text()
        count = $('.num_show').val()
        // 计算商品的总价
        price = parseFloat(price)
        count = parseInt(count)
        amount = price * count
        // 设置商品的总价
        $('.total').children('em').text(amount.toFixed(2) + '元')
    }

    // 增加商品的数量
    $('.adder').click(function () {
        console.log("增加")
        // 获取商品原有的数目
        count = parseInt($('.num_show').val())
        maxnum = parseInt($('.max_num').val())
        // 加1
        if (count < maxnum){
            count = count+1
        // 重新设置商品的数目
        $('.num_show').val(count)
        $('.postvalue').val(count)
        }
        var itGid=$(this).attr('goodid');
        var token = $('[name="csrfmiddlewaretoken"]').attr("value");
        $.ajax({
        url:"/cart",
        type:"POST",
        data:JSON.stringify({'gid':itGid,'num':count, "flag":"updatenum","csrfmiddlewaretoken": token}),
        dataType : "text"
        })
        // 更新商品的总价
        update_goods_amount()
    })

    // 减少商品的数量
    $('.reducer').click(function () {
        console.log("减少")
        // 获取商品原有的数目
        count = $('.num_show').val()
        // 减1
        count = parseInt(count)-1
        if (count <= 0) {
            count = 1
        }
        // 重新设置商品的数目
        $('.num_show').val(count)
        $('.postvalue').val(count)
        // 更新商品的总价
        var itGid=$(this).attr('goodid');
        var token = $('[name="csrfmiddlewaretoken"]').attr("value");
        $.ajax({
        url:"/cart",
        type:"POST",
        data:JSON.stringify({'gid':itGid,'num':count, "flag":"updatenum","csrfmiddlewaretoken": token}),
        dataType : "text"
        })
        update_goods_amount()
    })


    // 手动输入商品的数量
    $('.num_show').blur(function () {
        // 获取用户输入的数目
        count = $(this).val()
        // 校验count是否合法
        if (isNaN(count) || count.trim().length == 0 || parseInt(count) <= 0) {
            count = 1
        }
        // 重新设置商品的数目
        $(this).val(parseInt(count))
        $('.postvalue').val(count)
        // 更新商品的总价
        var itGid=$(this).attr('goodid');
        var token = $('[name="csrfmiddlewaretoken"]').attr("value");
        $.ajax({
        url:"/cart",
        type:"POST",
        data:JSON.stringify({'gid':itGid,'num':count, "flag":"updatenum","csrfmiddlewaretoken": token}),
        dataType : "text"
        })
        update_goods_amount()
    })
    //搜索框输入商品类型，进去该商品类型列表，向后端传用户输入商品类型名称
    $(".input_btn").click(function () {
        var type = $(".input_text").val();
        // 判断用户输入是否为空
        if (type == '' || type == null) {
            var aobj = document.getElementById("search1");
            aobj.href = "";
            alert('未输入商品名称！')

        } else {
            $.ajax({
                url: "/goods",
                type: "POST",
                data: JOSN.stringify({'gname': type}),
                dataType: "text"
            })
        }

    })
    // 点击商品类型，进入该商品类型商品列表，向后端传商品类型id
    $(".subnav a").click(function () {
        var itgid = $(this).attr('GoodsCategory.id ');
        $.ajax({
            url: "/goods",
            type: "POST",
            data: JOSN.stringify({'gid': itgid}),
            dataType: "text"
        })
    })
    // 点击商品类型，进入该商品类型商品列表，向后端传商品类型id
    $(".navlist a").click(function () {
        var itgid = $(this).attr('GoodsCategory.id ');
        $.ajax({
            url: "/goods",
            type: "POST",
            data: JOSN.stringify({'gid': itgid}),
            dataType: "text"
        })
    })
    // 点击商品类型，进入该商品类型商品列表，向后端传商品类型id
    $(".breadcrumb a").click(function () {
        var itgid = $(this).attr('goods.style.id ');
        $.ajax({
            url: "/goods",
            type: "POST",
            data: JOSN.stringify({'gid': itgid}),
            dataType: "text"
        })
    })
    //点击立即购买，进入结算界面，向后端传购买用户id,商品数量，商品id
    $('.buy_btn').click(function () {
        var uid = $(this).attr('user.id');
        var count = $('.num_show').val();
        var gid = $(this).attr('goods.goods_id');
        $.ajax({
            url: "/cart",
            type: "POST",
            data: JOSN.stringify({'uid': uid, 'gid': gid, 'count': count}),
            dataType: "text"
        })
    })
    //点击加入购物车，向后端传加入购物车的用户id,商品数量，商品id
    $('.add_cart').click(function () {
        var uid = $(this).attr('user.id');
        var count = $('.num_show').val();
        var gid = $(this).attr('goods.goods_id');
        $.ajax({
            url: "/cart",
            type: "POST",
            data: JOSN.stringify({'uid': uid, 'gid': gid, 'count': count}),
            dataType: "text"
        })
    })
    //点击加入收藏夹，向后端传加入收藏夹的用户id,，商品id
    $('.add_shou').click(function () {
        var uid = $(this).attr('user.id');
        var gid = $(this).attr('goods.goods_id');
        $.ajax({
            url: "/cart",
            type: "POST",
            data: JOSN.stringify({'uid': uid, 'gid': gid}),
            dataType: "text"
        })
    })
    // 点击商品图片，进入该商品详情页，向后端传该商品id
    $(".new_goods a").click(function () {
        var itgid = $(this).attr('goods.goods_id');
        $.ajax({
            url: "/goods",
            type: "POST",
            data: JOSN.stringify({'gid': itgid}),
            dataType: "text"
        })
    })
});