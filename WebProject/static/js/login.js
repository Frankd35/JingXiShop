$(function() {
    var login= $('.login_zls1 li input');
    console.log(login.val());
    if(login.val()==1){
        $(".login_zls").hide();
        $(".login_zls2").show();
        $(".goods_count").hide();
        $(".goods_count1").show();
        $(".login_btn2").show();
        $(".login_btn1").hide();
    }
    else{
        $(".login_zls").show();
        $(".login_zls2").hide();
         $(".goods_count1").hide();
         $(".goods_count").show();
         $(".login_btn1").show();
        $(".login_btn2").hide();
    }

});
