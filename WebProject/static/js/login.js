$(function() {
    var login= $('.login_zls1 li input');
    console.log(login.val());
    if(login.val()==1){
        $(".login_zls").hide();
        $(".login_zls2").show();
    }
    else{
        $(".login_zls").show();
        $(".login_zls2").hide();
    }

});