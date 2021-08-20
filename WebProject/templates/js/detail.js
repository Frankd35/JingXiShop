$(function() {
    
    $(".reducer").mouseover(function() {
        if ($(".num_add input[type='text']").val() <= 1) {
            $(".reducer").css("cursor","not-allowed");
        }
        else {
            $(".reducer").css("cursor","pointer");
        }
    });
    $(".reducer").click(function() {
        if ($(".num_add input[type='text']").val() <= 1) {
            $(".reducer").css("cursor","not-allowed");
        }
        else {
            $(".reducer").css("cursor","pointer");
            var num =  $(".num_add input[type='text']").val();
            $(".num_add input[type='text']").val(num-1);
        }
    });
    $(".adder").click(function() {
        var num =  $(".num_add input[type='text']").val();
        $(".num_add  input[type='text']").val(Number(num)+1);
    });
});