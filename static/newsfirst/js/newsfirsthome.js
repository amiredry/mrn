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
                 od = $("a.headline-list-anchor:first").attr("data-hash2");  console.log ( od );},

            dataType: "json"
        });
    /*
     $.get("http://127.0.0.1:8001/news/news_updates/"+ od + "", function(data){
                                                                         $( "#headline-listview" ).prepend(data);
                                                                         $( "li" ).slice( 50 ).css( "opacity",0.2 );
                                                                         od = $("li:first-child a.headline-list-anchor").attr("data-hash2");

                                                                               },"json");


*/

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



/*
    $("#headline-listview").on("click",".headline-list-anchor", function(){
         var $link = $(this);
         $('#overlay').load($link.attr('href')).dialog({
             modal: true,
             resizable: false,
             draggable: false,
			 width: 900,
             height:500
            }).empty();
         return false
     });
*/
});
