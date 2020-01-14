/*
 *
 *   RENAISSANCE - Responsive Admin Theme
 *   version 1.3.0
 *
*/

var datetime = null,
        date = null;

var update = function () {
    date = moment(new Date())
    datetime.html(date.format('h:mm A'));
};

$(window).on('load', function(){
    //Preloader
    setTimeout(function(){
        $('.preloader').fadeOut(100);
    }, 500);
});


// check if browser support HTML5 local storage
function localStorageSupport() {
    return (('localStorage' in window) && window['localStorage'] !== null)
}


  //Personal working platform Sidebar

$("li.perwork-btn").click(function(){

     $(this).toggleClass("active").siblings().removeClass("active");

    var currentEle=$(this);
    
    var siblingsElel=currentEle.siblings("li.members-btn");

    $.each(siblingsElel,function(index,ele){
       $("#"+$(ele).data("href")).removeClass('members-sidebar-open');
       if($("#"+$(ele).data("href")).hasClass('dropdown-menu')){
          $("#"+$(ele).data("href")).attr("aria-expanded","false");
          $(ele).removeClass("open").removeClass("active");
       }
    });

    cta($(this)[0], $("#"+currentEle.data("href"))[0], {relativeToWindow: true}, function () {
      if($("#"+currentEle.data("href")).hasClass('dropdown-menu')){
        $("#"+currentEle.data("href")).attr("aria-expanded","true");
        currentEle.toggleClass("open");
      }else{
          $("#"+currentEle.data("href")).toggleClass('members-sidebar-open');
      }
    });

    $(currentEle.data("close")).click(function(){
      $("#"+currentEle.data("href")).removeClass('members-sidebar-open');
      currentEle.removeClass('active');
    });
  return false;

});

