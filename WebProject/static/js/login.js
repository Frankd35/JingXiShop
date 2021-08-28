$(function() {
 $(document).ready(function() {
        countdown();
        setInterval(countdown, 1000);
    });
    function countdown() {
        var nowtime = +new Date();
        var inputtime = +new Date('2021-9-18 24:00:00');
        var times = (inputtime - nowtime) / 1000;
        var h = parseInt(times / 60 / 60 % 24);
        h = h < 10 ? '0' + h : h;
        $(".hour").html(h);
        var m = parseInt(times / 60 % 60);
        m = m < 10 ? '0' + m : m;
        $(".minute").html(m);
        var s = parseInt(times % 60);
        s = s < 10 ? '0' + s : s;
        $(".second").html(s);
    };
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
