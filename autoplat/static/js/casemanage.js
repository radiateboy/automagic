/**
 * Created by ray on 16-11-2.
 */

var keywordlist = []
$(document).ready(function(){
    /*  根据项目查询元素进行模糊搜索匹配   */
    if($("#selprojectid").val() != ""){
        var s1SelectedVal = $('#selprojectid').val();
        //通过 project 查询对应 element  进行模糊搜索匹配
        $.ajax({
        type:"GET",
        data:{'projectid':s1SelectedVal},
        url: "/func/get/element/", //后台处理函数的url 这里用的是static url 需要与urls.py中的name一致
        cache: false,
        dataType:'json',
        async:false,

        success: function(result,TextStatus) {
            if (result.length > 0) {
                elementTags = result;

                $('input[name="autocomplete"]').each(function() {
                    $(this).autocomplete({
                        minLength: 0,
                        source: elementTags,
                        focus: function (event, ui) {
                            return false;
                        },
                        select: function (event, ui) {
                            $(this).val(ui.item.value);
                            $(this).next().val(ui.item.key);

                            return false;
                        },

                    }).data("ui-autocomplete")._renderItem = function (ul, item) {
                        return $("<li>")
                                .append('<div class="ui-menu-item-wrapper" title="' + item.location.replace(/"/g, "'") + '">' + item.value + '</div>')
                                .appendTo(ul);
                    };
                })
            }
        }
    });
    }

    /* 根据产品名称查询关键字列表 */
    if($('[name="caseproductname"]').val() != ""){
        var productid = $('[name="caseproductname"]').val();
        $.ajax({
            type: "GET",
            data: {'productid': productid},
            url: "/func/get/keyword/", //后台处理函数的url 这里用的是static url 需要与urls.py中的name一致
            cache: false,
            dataType: 'json',

            success: function (result, TextStatus) {
                keywordlist = result;
                if ($('#case_add').length > 0){
                    $('#keyword_1').empty();
                    $('#keyword_1').append('<option value="">请选择关键字</option>');
                    if (result.length > 0) {
                        for (i = 0; i < result.length; i++) {
                            $('select[name="keyword"]').append('<option value="' + result[i].key + '">'+'['+ result[i].productid +']'+ result[i].kwdescr + '</option>');
                        }
                    }
                }
            },
            error:function (result) {
                alert(result);
            }
        });
    }
});




/*    通过project关联对应 element   */
$("#selprojectid").bind("change",function(){
    var s1SelectedVal = $('#selprojectid').val();
    /*  根据项目查询元素进行模糊搜索匹配   */
    if($("#selprojectid").val() != ""){
        //通过 project 查询对应 element  进行模糊搜索匹配
        $.ajax({
            type:"GET",
            data:{'projectid':s1SelectedVal},
            url: "/func/get/element/", //后台处理函数的url 这里用的是static url 需要与urls.py中的name一致
            cache: false,
            dataType:'json',
            async:false,

            success: function(result,TextStatus) {
                if (result.length > 0) {
                    elementTags = result;
                    $('input[name="autocomplete"]').each(function() {
                        $(this).autocomplete({
                            minLength: 0,
                            source: elementTags,
                            focus: function (event, ui) {
                                return false;
                            },
                            select: function (event, ui) {
                                $(this).val(ui.item.value);
                                $(this).next().val(ui.item.key);

                                return false;
                            },

                        }).data("ui-autocomplete")._renderItem = function (ul, item) {
                            return $("<li>")
           .append('<div class="ui-menu-item-wrapper" title="' + item.location.replace(/"/g, "'") + '">' + item.value + '</div>')
           .appendTo(ul);
                        };
                    })
                }
            }
        });
    }
});

//行添加
function case_step_addtr() {
    rowid = $('#rowid').val();
    var len = parseInt($("#linecounter").val())+1;

    $("#tab tbody").append('<tr id=row'+len+' name="rowstep">'
        +'<td>'+len+'</td>'
        +'<td><input name="descr" class="ac-acaseedit-input" placeholder="请输入步骤描述" type="input"></td>'
        +'<td><select id="keyword_'+len+'" name="keyword" class="ak-left ac-aselect col01"></select></td>'
        +'<td><input id="autocomplete_'+len+'" name="autocomplete" class="ui-autocomplete-input ac-element-input" type="input"><input type="hidden" id="elementid_'+len+'" name="elementid" value="None"></td>'
        +'<td><input name="inputtext" class="ac-keywordtext-input" placeholder="" type="input"></td>'
        +'<td><a  title="上移" class="ke-ablock" onclick="up(this)"><i class="glyphicon glyphicon-chevron-up"></i></a>' +
        '<a  title="下移" class="ke-ablock" onclick="down(this)"><i class="glyphicon glyphicon-chevron-down"></i></a>' +
        '<a  title="删除" class="ke-ablock" onclick="deltr('+len+')"><i class="glyphicon glyphicon-trash"></i></a>' +
        '<a  title="复制" class="ke-ablock" onclick="case_step_copytr(this)"><i class="glyphicon glyphicon-copy"></i></a></td>'
        +'</tr>');
    $("#linecounter").val(len);
    if(rowid != ''){
        $('#row'+len).insertAfter('#row'+rowid);
    }
    $('#rowid').val('');
    $('#keyword_'+len).empty();
    if (keywordlist.length > 0) {
                for (i = 0; i < keywordlist.length; i++) {
                    $('#keyword_'+len).append('<option value="' + keywordlist[i].key + '">'+'['+ keywordlist[i].productid +']'+ keywordlist[i].kwdescr + '</option>');
                }
            }

    $( "#autocomplete_" +len ).autocomplete({
        minLength: 0,
        source: elementTags,
        focus: function( event, ui ) {
            return false;
        },
        select: function( event, ui ) {
            $( "#autocomplete_"+len ).val( ui.item.value );
            $( "#elementid_"+len ).val( ui.item.key );
            return false;
        },
    })
        .data( "ui-autocomplete" )._renderItem = function( ul, item ) {
        return $( "<li>" )
            .append('<div class="ui-menu-item-wrapper" title="'+item.location.replace(/"/g,"'")+'">' + item.value + '</div>')
            .appendTo( ul );
    };
}

//行复制
function case_step_copytr(obj) {
   // row_num = $('#rowid_copy').val();
   // var len = parseInt($("#linecounter").val())+1;
   // copy_rowid= '#row'+row_num
    var objParentTR = $(obj).parent().parent();
    copy_rowid = '#'+objParentTR[0].id
    var len = parseInt($("#linecounter").val())+1;
    var descr=$(copy_rowid).find($("input[name='descr']"))[0].value;
    var keyword_selectedIndex=$(copy_rowid).find($("select[name='keyword']"))[0].selectedIndex;
    var element=$(copy_rowid).find($("input[name='autocomplete']"))[0].value;
    var element_num=$(copy_rowid).find($("input[name='elementid']"))[0].value;
    var inputtext=$(copy_rowid).find($("input[name='inputtext']"))[0].value;

    $("#tab tbody").append('<tr id=row'+len+' name="rowstep">'
        +'<td>'+len+'</td>'
        +'<td><input name="descr" class="ac-acaseedit-input" placeholder="请输入步骤描述" type="input" ></td>'
        +'<td><select id="keyword_'+len+'" name="keyword" class="ak-left ac-aselect col01"></select></td>'
        +'<td><input id="autocomplete_'+len+'" name="autocomplete" class="ui-autocomplete-input ac-element-input" type="input" value='+element+'><input type="hidden" id="elementid_'+len+'" name="elementid" value='+element_num+'></td>'
        +'<td><input name="inputtext" class="ac-keywordtext-input" placeholder="" type="input" value="'+inputtext+'"></td>'
        +'<td><a  title="上移" class="ke-ablock" onclick="up(this)"><i class="glyphicon glyphicon-chevron-up"></i></a>' +
        '<a  title="下移" class="ke-ablock" onclick="down(this)"><i class="glyphicon glyphicon-chevron-down"></i></a>' +
        '<a  title="删除" class="ke-ablock" onclick="deltr('+len+')"><i class="glyphicon glyphicon-trash"></i></a>' +
        '<a  title="复制" class="ke-ablock" onclick="case_step_copytr(this)"><i class="glyphicon glyphicon-copy"></i></a></td>'
        +'</tr>');
    $("#linecounter").val(len);
    $("#row"+len).find($("input[name='descr']"))[0].value=descr
    if(copy_rowid != ''){
        $('#row'+len).insertAfter('#row'+len);
    }
    $('#copy_rowid').val('');
    $('#keyword_'+len).empty();
    if (keywordlist.length > 0) {
                for (i = 0; i < keywordlist.length; i++) {
                    if(i==keyword_selectedIndex)
                        $('#keyword_'+len).append('<option value="' + keywordlist[i].key + '" selected="selected">'+'['+ keywordlist[i].productid +']'+ keywordlist[i].kwdescr + '</option>');
                    else
                        $('#keyword_'+len).append('<option value="' + keywordlist[i].key + '">'+'['+ keywordlist[i].productid +']'+ keywordlist[i].kwdescr + '</option>');
                }
            }

    $( "#autocomplete_" +len ).autocomplete({
        minLength: 0,
        source: elementTags,
        focus: function( event, ui ) {
            return false;
        },
        select: function( event, ui ) {
            $( "#autocomplete_"+len ).val( ui.item.value );
            $( "#elementid_"+len ).val( ui.item.key );
            return false;
        },
    })
        .data( "ui-autocomplete" )._renderItem = function( ul, item ) {
        return $( "<li>" )
            .append('<div class="ui-menu-item-wrapper" title="'+item.location.replace(/"/g,"'")+'">' + item.value + '</div>')
            .appendTo( ul );
    };
}
//行删除
function deltr(index) {
    $("tr[id='row"+index+"']").remove();//删除当前行
}