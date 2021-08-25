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