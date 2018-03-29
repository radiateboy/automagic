/**
 * Created by ray on 16-9-9.
 */




function getUrlParam(name) {
    var reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)");
    var r = window.location.search.substr(1).match(reg);
    if (r != null)return r[2];return 0;
}

$(document).ready(function () {


    //产品和项目二级菜单关联 通过product关联project下拉菜单
    $("#selproductid").bind("change", function () {
        var s1SelectedVal = $('#selproductid').val();
        $('#check_productid').val(s1SelectedVal);
        $.ajax({
            type: "GET",
            data: {'productid': s1SelectedVal},
            url: "/setting/get/project/", //后台处理函数的url 这里用的是static url 需要与urls.py中的name一致
            cache: false,
            dataType: 'json',
            async: false,

            success: function (result, TextStatus) {
                //元素管理元素添加项目选择
                $('select[name="ele_add_projectid"]').empty();
                $('select[name="ele_add_projectid"]').append('<option value="">所属项目</option>');
                if (result.length > 0) {
                    for (i = 0; i < result.length; i++) {
                        $('select[name="ele_add_projectid"]').append('<option value="' + result[i].key + '">' + result[i].value + '</option>');
                    }
                }
                $('#selprojectid').empty();
                // $('#selprojectid').append('<option value="">所属项目</option>');
                if (result.length > 0) {
                    for (i = 0; i < result.length; i++) {
                        $('#selprojectid').append('<option value="' + result[i].key + '">' + result[i].value + '</option>');
                    }
                }
                if ($("#selprojectid").val() != localStorage.getItem('project')) {
                    // alert('test');
                    $("#selprojectid").find("option[value=" + localStorage.getItem('project') + "]").attr("selected", true);
                }
                if ($("#selprojectid").val() != "") {
                    $("#selprojectid").change();
                }
            }
        });

        if (s1SelectedVal == localStorage.getItem('product')) {
            return;
        }
        localStorage.setItem('product', s1SelectedVal);
        localStorage.setItem('moduleid', '');
        $('#search_btn').trigger('click');
    });

    /*    通过project关联module下拉菜单   */
    $("#selprojectid").bind("change", function () {
        var s1SelectedVal = $('#selprojectid').val();
        localStorage.setItem('project', s1SelectedVal);
        $.ajax({
            type: "GET",
            data: {'projectid': s1SelectedVal},
            url: "/setting/get/module/", //后台处理函数的url 这里用的是static url 需要与urls.py中的name一致
            cache: false,
            dataType: 'json',

            success: function (result, TextStatus) {
                $('#selmoduleid').empty();
                $('#selmoduleid').append('<option value="">所属模块</option>');
                if (result.length > 0) {
                    for (i = 0; i < result.length; i++) {
                        $('#selmoduleid').append('<option value="' + result[i].key + '">' + result[i].value + '</option>');
                    }
                }
                if ($("#selmoduleid").val() != localStorage.getItem('moduleid')) {
                    $("#selmoduleid").find("option[value=" + localStorage.getItem('moduleid') + "]").attr("selected", true);
                }

            }
        });
        var projectid_url = getUrlParam('projectid');
        if (projectid_url == 0 && $('#selprojectid').val() !== null){
            $('#search_btn').trigger('click');
        }
    });

    /*   通过module关联element 菜单 */
    $("#selmoduleid").bind("change", function () {
        var moduleVal = $('#selmoduleid').val();
        var moduleid = localStorage.getItem('moduleid');
        if (moduleVal!== moduleid){
            $('#search_btn').trigger('click');
            localStorage.setItem('moduleid', moduleVal);
        }
    });

    /*  通过 localStorage 在本地存储选择的产品  */
    if (window.localStorage) {
        var selproduct = localStorage.getItem('product');
        $("#selproductid").find("option[value=" + selproduct + "]").attr("selected", true);
        //$("#selproductid").change();

    }
    if ($("#selproductid") != '') {
        $("#selproductid").change();
    }


    /*    添加元素页面 project关联module下拉多选菜单   */
    $("#sel_projectid").bind("change", function () {
        var s1SelectedVal = $('#sel_projectid').val();
        // $('#mdlist').val('');
        // $('#selvalue').val('');
        $.ajax({
            type: "GET",
            data: {'projectid': s1SelectedVal},
            url: "/setting/get/module/", //后台处理函数的url 这里用的是static url 需要与urls.py中的name一致
            cache: false,
            dataType: 'json',

            success: function (result, TextStatus) {
                // $('.multi_select').empty();
                // $('#selmoduleid').append('<option value="">所属模块</option>');
                // if (result.length > 0) {
                //    $(function (){
                //      $('.multi_select').MSDL({
                //        'width': '160',
                //        'data': result,
                //      });
                //    });
                // }
                $('#selvalue').empty();
                $('#selvalue').append('<option value="">所属模块</option>');
                if (result.length > 0) {
                    for (i = 0; i < result.length; i++) {
                        $('#selvalue').append('<option value="' + result[i].key + '">' + result[i].value + '</option>');
                    }
                }
            }
        });
    });

    /*    编辑元素project关联module下拉菜单   */
    $("#eleprojectid").bind("change", function () {
        var s1SelectedVal = $('#eleprojectid').val();
        $.ajax({
            type: "GET",
            data: {'projectid': s1SelectedVal},
            url: "/setting/get/module/", //后台处理函数的url 这里用的是static url 需要与urls.py中的name一致
            cache: false,
            dataType: 'json',
            async: false,

            success: function (result, TextStatus) {
                $('#elemoduleid').empty();
                $('#elemoduleid').append('<option value="">所属模块</option>');
                if (result.length > 0) {
                    for (i = 0; i < result.length; i++) {
                        $('#elemoduleid').append('<option value="' + result[i].key + '">' + result[i].value + '</option>');
                    }
                }
            }
        });
    });

    /*    添加测试用例    */
    $('#case_add').submit(function () {
        $('[name="autocomplete"]').each(function () {
            if ($(this).val() == '') {
                $(this).next().val('None')
            }
        });
        $.ajax({
            type: "POST",
            data: $(this).serialize(),
            //             data:{casedesc:casedesc, isenabled:isenabled, issmoke:issmoke, projectid:projectid, moduleid:moduleid,dependent:dependent,descr:descr,keyword:keyword,elementid:elementid,inputtext:inputtext},
            url: "/func/case/add/",
            cache: false,
            dataType: "html",
            success: function (result, statues, xml) {
                $('#log_info').addClass('bg-primary');
                $('#log_info').css('display', 'block');
                $('#log_info').html(result);
                setTimeout("location.reload()", 1500);
                window.location.href = "/func/case/list/"
            },
            error: function () {
                $('#log_info').addClass('bg-primary');
                $('#log_info').css('display', 'block');
                $('#log_info').html('保存失败');
                setTimeout("$('#log_info').css('display','none');", 1500);
            }
        });
        return false;
    });

    /*    添加元素     */
    $('#ele_add').submit(function () {
        var descr = $("#id_descr").val();      //获得form中用户输入的descr 注意这里的descr 与你html中的id一致
        var projectid = $("#sel_projectid").val(); //同上
        var moduleid = $("#selvalue").val(); //同上
        var locmode = $("#id_locmode").val();
        var location = $("#id_location").val();
        var m = []
        m = moduleid.split(';')
        // alert(m.length);
        for (i = 0; i < m.length; i++) {
            $.ajax({
                type: "POST",
                data: {descr: descr, projectid: projectid, moduleid: m[i], locmode: locmode, location: location},
                url: "/func/element/add/", //后台处理函数的url 这里用的是static url 需要与urls.py中的name一致
                cache: false,
                dataType: "html",

                success: function (result, statues, xml) {
                    debugger;
                    $('#log_info').addClass('bg-primary');
                    $('#log_info').css('display', 'block');
                    $('#log_info').html(result);
                    setTimeout("$('#log_info').css('display', 'None');$('#id_location').val('');", 1500);  //成功时弹出view传回来的结
                },
                error: function () {
                    debugger;
                    $('#log_info').addClass('bg-primary');
                    $('#log_info').css('display', 'block');
                    $('#log_info').html('添加失败。');
                    setTimeout("location.reload()", 1500);
                }
            });
        }

        return false;
    });

    /*     添加关键字     */
    $('#add_keyword').submit(function () {
        var keyword = $('#keyword').val();
        var kwdescr = $('#kwdescr').val();
        var productid = $('#selproductid').val();
        $.ajax({
            type: "POST",
            data: {keyword: keyword, kwdescr: kwdescr, productid: productid},
            url: "/func/keyword/add/",
            cache: false,
            dataType: "html",
            success: function (result, statues, xml) {
                // debugger;
                $('#log_info').addClass('bg-primary');
                $('#log_info').css('display', 'block');
                $('#log_info').html(result);
                setTimeout("location.reload()", 1500);
                // alert(result);
            },
            error: function () {
                // debugger;
                $('#log_info').addClass('bg-primary');
                $('#log_info').css('display', 'block');
                $('#log_info').html('添加失败，关键字可能已经存在。');
                setTimeout("location.reload()", 1500);
            }
        });
        return false;
    });

    /*    添加产品     */
    $('#product_add').submit(function () {
        $.ajax({
            type: "POST",
            data: $(this).serialize(),
            url: "/setting/product/add/",
            cache: false,
            dataType: "html",
            success: function (result, statues, xml) {
                $('#addProductModal').hide()
                $('#log_info').addClass('bg-primary');
                $('#log_info').css('display', 'block');
                $('#log_info').html(result);
                setTimeout("location.reload()", 1200);
            },
            error: function () {
                $('#log_info').addClass('bg-primary');
                $('#log_info').css('display', 'block');
                $('#log_info').html('创建失败');
                alert('创建失败')
            }
        });
        return false;
    });

    /*     编辑产品     */
    $('#product_edit').submit(function () {
        $.ajax({
            type: "POST",
            data: $(this).serialize(),
            url: "/setting/product/update/",
            cache: false,
            dataType: "html",
            success: function (result, statues, xml) {
                $('#editProductModal').hide()
                $('#log_info').addClass('bg-primary');
                $('#log_info').css('display', 'block');
                $('#log_info').html(result);
                setTimeout("location.reload()", 1200);
            },
            error: function () {
                $('#log_info').addClass('bg-primary');
                $('#log_info').css('display', 'block');
                $('#log_info').html('创建失败');
                alert('创建失败')
            }
        });
        return false;
    });

    /*     添加项目     */
    $('#project_add').submit(function () {
        $.ajax({
            type: "POST",
            data: $(this).serialize(),
            url: "/setting/project/add/",
            cache: false,
            dataType: "html",
            success: function (result, statues, xml) {
                $('#addProjectModal').hide()
                $('#log_info').addClass('bg-primary');
                $('#log_info').css('display', 'block');
                $('#log_info').html(result);
                setTimeout("location.reload()", 1200);
            },
            error: function () {
                $('#log_info').addClass('bg-primary');
                $('#log_info').css('display', 'block');
                $('#log_info').html('创建失败');
                alert('创建失败')
            }
        });
        return false;
    });

    /*     编辑项目     */
    $('#project_edit').submit(function () {
        $.ajax({
            type: "POST",
            data: $(this).serialize(),

            url: "/setting/project/update/",
            cache: false,
            dataType: "html",
            success: function (result, statues, xml) {
                $('#editProjectModal').hide()
                $('#log_info').addClass('bg-primary');
                $('#log_info').css('display', 'block');
                $('#log_info').html(result);
                setTimeout("location.reload()", 1200);
            },
            error: function () {
                $('#log_info').addClass('bg-primary');
                $('#log_info').css('display', 'block');
                $('#log_info').html('创建失败');
                alert('创建失败')
            }
        });
        return false;
    });

    /*   添加模块   */
    $('#module_add').submit(function () {
        $.ajax({
            type: "POST",
            data: $(this).serialize(),
            url: "/setting/module/add/",
            cache: false,
            dataType: "html",
            success: function (result, statues, xml) {
                $('#addModuleModal').hide()
                $('#log_info').addClass('bg-primary');
                $('#log_info').css('display', 'block');
                $('#log_info').html(result);
                setTimeout("location.reload()", 1200);
            },
            error: function () {
                $('#log_info').addClass('bg-primary');
                $('#log_info').css('display', 'block');
                $('#log_info').html('创建失败');
                alert('创建失败')
            }
        });
        return false;
    });

    /*  编辑模块   */
    $('#module_edit').submit(function () {
        $.ajax({
            type: "POST",
            data: $(this).serialize(),
            url: "/setting/module/update/",
            cache: false,
            dataType: "html",
            success: function (result, statues, xml) {
                $('#editModuleModal').hide()
                $('#log_info').addClass('bg-primary');
                $('#log_info').css('display', 'block');
                $('#log_info').html(result);
                setTimeout("location.reload()", 1200);
            },
            error: function () {
                $('#log_info').addClass('bg-primary');
                $('#log_info').css('display', 'block');
                $('#log_info').html('创建失败');
                alert('创建失败')
            }
        });
        return false;
    });

    /*     提交编辑元素    */
    $('#element_edit').submit(function () {
        $.ajax({
            type: "POST",
            data: $(this).serialize(),
            url: "/func/element/update/",
            cache: false,
            dataType: "html",
            success: function (result, statues, xml) {
                $('#editElementModal').hide()
                $('#log_info').addClass('bg-primary');
                $('#log_info').css('display', 'block');
                $('#log_info').html(result);
                setTimeout("location.reload()", 1500);
            },
            error: function () {
                $('#log_info').addClass('bg-primary');
                $('#log_info').css('display', 'block');
                $('#log_info').html('创建失败');
                alert('创建失败')
            }
        });
        return false;
    });

    $(".radioitem").bind("change", function () {
        var selectvalue = $("input[name='tasktype']:checked").val();
        if (selectvalue == 1) {
            $("#testrailrunid").show();
            $("#testrailsuites").hide();
            $("#testsectionid").hide();
            $("#treeDemo").show();
            $("#customParameters").show();
            $("#jenkins_server_url").hide();
            $("#user_id").hide();
            $("#api_token").hide();
            $("#build_name").hide();
            $("#selectedCases").show();
        }
        else if (selectvalue == 2) {
            $("#testrailrunid").hide();
            $("#testrailsuites").show();
            $("#testsectionid").show();
            $("#treeDemo").show();
            $("#customParameters").show();
            $("#jenkins_server_url").hide();
            $("#user_id").hide();
            $("#api_token").hide();
            $("#build_name").hide();
            $("#selectedCases").show();
        }
        else {
            $("#testrailrunid").hide();
            $("#testrailsuites").hide();
            $("#testsectionid").hide();
            $("#treeDemo").hide();
            $("#customParameters").hide();
            $("#jenkins_server_url").show();
            $("#user_id").show();
            $("#api_token").show();
            $("#build_name").show();
            $("#selectedCases").hide();
        }
    });

    /*     提交新增任务    */
    $('#task_add').submit(function () {
        var treeObj = $.fn.zTree.getZTreeObj("treeDemo");
        var nodes = treeObj.getCheckedNodes(true);
        var index = 1;
        var text = '';
        var jsonlist = {}
        nodes.forEach(function (node) {
            if (node.level === 1) {
                var childIds = []
                node.children.forEach(function (child) {
                    childIds.push(child.id)
                })
                jsonlist[index++] = childIds.join(',')
            }
        })
        text = JSON.stringify(jsonlist);
        // for (x in nodes){
        //     if (nodes[x].id < 9999999){
        //         text = text + nodes[x].id + ",";
        //     }
        // }
        $('#caseids').val(text);
        $.ajax({
            type: "POST",
            data: $(this).serialize(),
            url: "/func/task/add/",
            cache: false,
            dataType: "html",
            success: function (result, statues, xml) {
                $('#log_info').addClass('bg-primary');
                $('#log_info').css('display', 'block');
                $('#log_info').html(result);
                setTimeout("window.location.href='/func/task/list/'", 500);
            },
            error: function () {
                $('#log_info').addClass('bg-primary');
                $('#log_info').css('display', 'block');
                $('#log_info').html('创建失败');
                alert('创建失败')
            }
        });
        return false;
    });

    /*     提交编辑任务    */
    $('#task_edit').submit(function () {
        var treeObj = $.fn.zTree.getZTreeObj("treeDemo");
        var nodes = treeObj.getCheckedNodes(true);
        var index = 1;
        var text = "";
        var jsonlist = {}
        nodes.forEach(function (node) {
            if (node.level === 1) {
                var childIds = []
                node.children.forEach(function (child) {
                    if (child.checked === true) {
                        childIds.push(child.id)
                    }
                })
                jsonlist[index++] = childIds.join(',')
            }
        })
        text = JSON.stringify(jsonlist);
        // for (x in nodes){
        //     if (nodes[x].id < 9999999){
        //         text = text + nodes[x].id + ",";
        //     }
        // }
        $('#caseids').val(text);
        var taskid = $("#taskid").val();
        $.ajax({
            type: "POST",
            data: $(this).serialize(),
            url: "/func/task/update/" + taskid + "/",
            cache: false,
            dataType: "html",
            success: function (result, statues, xml) {
                $('#log_info').addClass('bg-primary');
                $('#log_info').css('display', 'block');
                $('#log_info').html(result);
                setTimeout("window.location.href='/func/task/list/'", 500);
            },
            error: function () {
                $('#log_info').addClass('bg-primary');
                $('#log_info').css('display', 'block');
                $('#log_info').html('修改失败');
                alert('修改失败')
            }
        });
        return false;
    });


});

/*    点击产品编辑按钮    */
function setproductValue(id) {
    $.ajax({
        type: "GET",
        data: {'productid': id},
        url: "/setting/setedit/product/",
        cache: false,
        dataType: 'json',

        success: function (result, TextStatus) {
            if (result.length > 0) {
                for (i = 0; i < result.length; i++) {
                    $('#editProductModal [name="productid"]').val(result[i].id);
                    $('#editProductModal [name="productname"]').val(result[i].name);
                    $('#editProductModal [name="descr"]').val(result[i].descr);
                    $('#editProductModal [name="sortby"]').val(result[i].sortby);

                    if (result[i].isenabled) {
                        $('#editProductModal input:checkbox').attr("checked", "checked");
                    }
                    else {
                        $('#editProductModal input:checkbox').attr("checked", false);
                    }
                }
            }
        }
    });
}

/*   点击项目编辑按钮    */
function setprojectValue(id) {
    $.ajax({
        type: "GET",
        data: {'projectid': id},
        url: "/setting/setedit/project/",
        cache: false,
        dataType: 'json',

        success: function (result, TextStatus) {
            if (result.length > 0) {
                for (i = 0; i < result.length; i++) {
                    $('#editProjectModal [name="projectid"]').val(result[i].id);
                    $('#editProjectModal [name="projectname"]').val(result[i].name);
                    $('#editProjectModal [name="descr"]').val(result[i].descr);
                    $('#editProjectModal [name="version"]').val(result[i].version);
                    $('#editProjectModal [name="sortby"]').val(result[i].sortby);

                    if (result[i].isenabled) {
                        $('#editProjectModal input:checkbox').attr("checked", "checked");
                    }
                    else {
                        $('#editProjectModal input:checkbox').attr("checked", false);
                    }
                }
            }
        }
    });
}

/*点击模块编辑按钮*/
function setmoduleValue(id) {
    $.ajax({
        type: "GET",
        data: {'moduleid': id},
        url: "/setting/setedit/module/",
        cache: false,
        dataType: 'json',

        success: function (result, TextStatus) {
            if (result.length > 0) {
                for (i = 0; i < result.length; i++) {
                    $('#editModuleModal [name="moduleid"]').val(result[i].id);
                    $('#editModuleModal [name="modulename"]').val(result[i].name);
                    $('#editModuleModal [name="sortby"]').val(result[i].sortby);

                    if (result[i].isenabled) {
                        $('#editModuleModal input:checkbox').attr("checked", "checked");
                    }
                    else {
                        $('#editModuleModal input:checkbox').attr("checked", false);
                    }
                    // debugger;
                }
            }
        }
    });
}

/*    点击用户编辑按钮    */
function setuserValue(id) {
    $.ajax({
        type: "GET",
        data: {'userid': id},
        url: "/setting/setedit/user/",
        cache: false,
        dataType: 'json',

        success: function (result, TextStatus) {
            if (result.length > 0) {
                for (i = 0; i < result.length; i++) {
                    $('#editUserModal [name="userid"]').val(result[i].id);
                    $('#editUserModal [name="username"]').val(result[i].username);
                    // $('#editUserModal [name="password"]').val(result[i].password);
                    // $('#editUserModal [name="confirmPassword"]').val(result[i].password);
                    $('#editUserModal [name="email"]').val(result[i].email);
                    $('#editUserModal [name="realname"]').val(result[i].realname);
                    $('#editUserModal [name="mobile"]').val(result[i].mobile);
                    $('#editUserModal [name="testrailuser"]').val(result[i].testrailuser);
                    $('#editUserModal [name="testrailpass"]').val(result[i].testrailpass);
                    if (result[i].is_active) {
                        $('#editUserModal input[name="is_active"]').attr("checked", "checked");
                    }
                    else {
                        $('#editUserModal input[name="is_active"]').attr("checked", false);
                    }
                    if (result[i].is_admin) {
                        $('#editUserModal input[name="is_admin"]').attr("checked", "checked");
                    }
                    else {
                        $('#editUserModal input[name="is_admin"]').attr("checked", false);
                    }

                }
            }
        }
    });
}


/*    点击元素编辑按钮    */
function setelementValue(id) {

    $.ajax({
        type: "GET",
        data: {'elementid': id},
        url: "/func/setedit/element/",
        cache: false,
        dataType: 'json',
        async: true,

        success: function (result, TextStatus) {
            if (result.length > 0) {
                for (var i = 0; i < result.length; i++) {
                    $('#editElementModal [name="elementid"]').val(result[i].id);
                    $('#editElementModal [name="eledescr"]').val(result[i].descr);
                    $('#editElementModal [name="ele_add_projectid"]').val(result[i].projectid);
                    $('#eleprojectid').change();
                    $('#editElementModal [name="moduleid"]').val(result[i].moduleid);
                    $('#editElementModal [name="locmode"]').val(result[i].locmode);
                    $('#editElementModal [name="elelocation"]').val(result[i].location);
                }

            }
            // alert(result[i].projectid);

        }
    });

}

/*     添加用户     */
$(function () {
    $('#user_add')
        .bootstrapValidator({
//        live: 'disabled',
            message: 'This value is not valid',
            feedbackIcons: {
                valid: 'icon icon-ok',
                invalid: 'icon icon-remove',
                validating: 'icon icon-refresh'
            },
            fields: {
                username: {
                    message: '无效的用户名',
                    validators: {
                        notEmpty: {
                            message: '登录用户名不能为空'
                        },
                        stringLength: {
                            min: 4,
                            max: 30,
                            message: '用户名的长度为4-30字符'
                        },
                        regexp: {
                            regexp: /^[a-zA-Z0-9_\.\@]+$/,
                            message: '用户名只能由字母、数字和下划线组成'
                        },
                        different: {
                            field: 'password',
                            message: '用户名和密码不能一样'
                        }
                    }
                },
                email: {
                    validators: {
                        emailAddress: {
                            message: '无效的邮箱地址'
                        },
                        notEmpty: {
                            message: '邮箱地址不能为空'
                        }
                    }
                },
                password: {
                    validators: {
                        notEmpty: {
                            message: '登录密码不能为空'
                        },
                        different: {
                            field: 'username',
                            message: '密码不能和用户名一样'
                        }
                    }
                },
                confirmPassword: {
                    validators: {
                        notEmpty: {
                            message: '确认密码不能为空'
                        },
                        identical: {
                            field: 'password',
                            message: '密码和确认密码输入不一致'
                        }
                    }
                }
            }
        })

        .on('success.form.bv', function (e) {

            e.preventDefault();

            var $form = $(e.target);

            var bv = $form.data('bootstrapValidator');

            $.post($form.attr('action'), $form.serialize(), function (result) {
                $('#addUserModal').hide()
                $('#log_info').addClass('bg-primary');
                $('#log_info').css('display', 'block');
                $('#log_info').html(result);
                setTimeout("location.reload()", 1500);
            })
        });

});

/*     编辑用户     */
$(function () {
    $('#user_edit')
        .bootstrapValidator({
//        live: 'disabled',
            message: 'This value is not valid',
            feedbackIcons: {
                valid: 'icon icon-ok',
                invalid: 'icon icon-remove',
                validating: 'icon icon-refresh'
            },
            fields: {
                email: {
                    validators: {
                        emailAddress: {
                            message: '无效的邮箱地址'
                        },
                        notEmpty: {
                            message: '邮箱地址不能为空'
                        }
                    }
                },
                password: {
                    validators: {
                        identical: {
                            field: 'confirmPassword',
                            message: '密码和确认密码输入不一致'
                        }
                    }
                },
                confirmPassword: {
                    validators: {
                        identical: {
                            field: 'password',
                            message: '密码和确认密码输入不一致'
                        }
                    }
                }
            }
        })
        //         .bootstrapValidator({
        // //        live: 'disabled',
        //         message: 'This value is not valid',
        //         feedbackIcons: {
        //             valid: 'icon icon-ok',
        //             invalid: 'icon icon-remove',
        //             validating: 'icon icon-refresh'
        //         },
        //         fields: {
        //             email: {
        //                 validators: {
        //                     emailAddress: {
        //                         message: '无效的邮箱地址'
        //                     },
        //                     notEmpty: {
        //                         message: '邮箱地址不能为空'
        //                     }
        //                 }
        //             },
        //             password: {
        //                 validators: {
        //                     different: {
        //                         field: 'username',
        //                         message: '密码不能和用户名一样'
        //                     }
        //                 }
        //             },
        //             confirmPassword: {
        //                 validators: {
        //                     identical: {
        //                         field: 'password',
        //                         message: '密码和确认密码输入不一致'
        //                     }
        //                 }
        //             },
        //         }
        //     })

        .on('success.form.bv', function (e) {

            e.preventDefault();

            var $form = $(e.target);

            var bv = $form.data('bootstrapValidator');

            $.post($form.attr('action'), $form.serialize(), function (result) {
                $('#addEditModal').hide();
                $('#log_info').addClass('bg-primary');
                $('#log_info').css('display', 'block');
                $('#log_info').html(result);
                setTimeout("location.reload()", 1500);
            })
        });

});

/*   执行用例    */
function runcase(id) {
    $('#run' + id).attr('disabled', true);
    $('#run' + id + '>i.glyphicon.glyphicon-play-circle').remove();
    $('#run' + id).append('<i class="glyphicon glyphicon-record"></i>');

    $.ajax({
        type: "GET",
        data: {'caseid': id},
        url: "/func/case/run/",
        cache: false,
        dataType: "html",

        success: function (result, TextStatus, xml) {
            debugger;
            // alert(result);
            // $('#run'+id).attr('disabled',false);
            // $('#run'+id).addClass('green');
            // $('#run'+id).text('Run');
            setTimeout("location.reload()", 500);
        }
    });
}

/*   执行任务    */
function runtask(id) {
    // $('#run'+id).attr('disabled',true);
    $('#run' + id + '>i.glyphicon.glyphicon-play-circle').remove();
    $('#run' + id).append('<i class="glyphicon glyphicon-record"></i>');

    $.ajax({
        type: "GET",
        data: {'taskid': id},
        url: "/func/task/run/",
        cache: false,
        dataType: "html",

        success: function (result, TextStatus, xml) {
            // debugger;
            // alert(result);
            // $('#run'+id).attr('disabled',false);
            // $('#run'+id).addClass('green');
            // $('#run'+id).text('Run');
            setTimeout("location.reload()", 500);
        }
    });
}

function viewdebuginfo(x) {
    var debuginfo = $('td#' + x + ' pre').text();
    $('#divdebuginfo').text(debuginfo);
}


$("#selprojectid").on("change", function () {
    $('#mdlist').val('');
    $('#selvalue').val('');
});

/*    编辑元素上下移动行    */
function up(obj) {
    var objParentTR = $(obj).parent().parent();
    var prevTR = objParentTR.prev();
    if (prevTR.length > 0) {
        prevTR.insertAfter(objParentTR);
    }
}
function down(obj) {
    var objParentTR = $(obj).parent().parent();
    var nextTR = objParentTR.next();
    if (nextTR.length > 0) {
        nextTR.insertBefore(objParentTR);
    }
}

function goback() {
    window.history.back();
}