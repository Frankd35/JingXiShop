$(function() {
    $(".del1 a").click(function() {
        $(this).parent().parent().siblings().remove();
        $(this).parent().parent().remove();
        $(this).closest('.goods-list').remove();
    });

});