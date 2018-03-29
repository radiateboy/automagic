/**
 * Created by Ray on 16-11-11.
 */

/*    点击元素编辑按钮    */
function setkeywordValue(id){

    $.ajax({
        type:"GET",
        data:{'keywordid':id},
        url: "/func/setedit/keyword/",
        cache: false,
        dataType:'json',

        success: function(result,TextStatus) {
            if (result.length >0){
                for(var i=0; i<result.length; i++) {
                    // $('#editKeywordModal [name="productid"]').val(result[i].productid);
                    $('#editKeywordModal [name="productname"]').find("option[value="+result[i].productid+"]").attr("selected",true);
                    $('#editKeywordModal [name="keywordid"]').val(result[i].id);
                    $('#editKeywordModal [name="kwdescr"]').val(result[i].descr);
                    $('#editKeywordModal [name="keyword"]').val(result[i].name);
                }

         }
         // alert(result[i].projectid);
        },
        error:function (result) {
            alert(result)
        }
     });

}

/*     编辑元素     */
   $('#keyword_edit').submit(function () {
       $.ajax({
           type:"POST",
           data: $(this).serialize(),
           url:"/func/keyword/update/",
           cache: false,
           dataType:"html",
           success:function (result, statues,xml) {
               $('#editProductModal').hide()
               $('#log_info').addClass('bg-primary');
               $('#log_info').css('display','block');
               $('#log_info').html(result);
               setTimeout("location.reload()",1200);
           },
           error:function () {
               $('#log_info').addClass('bg-primary');
               $('#log_info').css('display','block');
               $('#log_info').html('创建失败');
               alert('创建失败')
           }
       });
       return false;
   });