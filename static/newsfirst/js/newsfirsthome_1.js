/**
 * Created with PyCharm.
 * User: ShadowTrader
 * Date: 12/16/13
 * Time: 12:41 PM
 * To change this template use File | Settings | File Templates.
 */

$(document).ready(function(){

    var od = $("a.headline-list-anchor").attr("data-hash2");

    setInterval(handleRefresh, 10000);

    function handleRefresh() {
        $.ajax({
            type: "GET",
            data: "data",
            url: "/news/news_updates/"+ od + "",
            success: function(data){
                $( "#headline-listview" ).prepend(data);
                $( ".list-group-item " ).slice( 50 ).remove();
                 od = $("a.headline-list-anchor:first").attr("data-hash2"); },

            dataType: "json"
        });

}


    $("#headline-listview").on("click","a:nth-child(4n+4)",
         function(){
             var $link = $(this);
             $('#myModal').modal('show');
             $("#cform").submit(function(event){

        $.post('/news/test',   $("#cform").serialize(),
                function(data) {


                    if (data == "incorrect-captcha-sol"){

                    $( "#result" ).html( '<p class="text-danger">Invalid captcha, please try again.</em></p>'  );
                    Recaptcha.reload();}

                    else
                    {
                        window.location.href = $link.attr('href');
                        }

                });
            return false
    });

             return false});
});
