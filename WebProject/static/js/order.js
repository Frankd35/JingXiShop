// $(function() {
//     $(".order_submit a").click(function() {
//         console.log("提交")
//         var token = $('[name="csrfmiddlewaretoken"]').attr("value");
//         $.ajax({
//         url:"/order",
//         type:"POST",
//         data:JSON.stringify({"csrfmiddlewaretoken": token}),
//         dataType : "text"
//         })
//     });
//
// });