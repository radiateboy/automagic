/**
 * Created by ray on 16-11-2.
 */
		var MoveTest = {
			errorMsg: "放错了...请选择正确的类别！",
			curTarget: null,
			curTmpTarget: null,
			noSel: function() {
				try {
					window.getSelection ? window.getSelection().removeAllRanges() : document.selection.empty();
				} catch(e){}
			},
			dragTree2Dom: function(treeId, treeNodes) {
				return !treeNodes[0].isParent;
			},
			prevTree: function(treeId, treeNodes, targetNode) {
				return !targetNode.isParent && targetNode.parentTId == treeNodes[0].parentTId;
			},
			nextTree: function(treeId, treeNodes, targetNode) {
				return !targetNode.isParent && targetNode.parentTId == treeNodes[0].parentTId;
			},
			innerTree: function(treeId, treeNodes, targetNode) {
				return targetNode!=null && targetNode.isParent && targetNode.tId == treeNodes[0].parentTId;
			},
			dragMove: function(e, treeId, treeNodes) {
				var p = null, pId = 'dom_' + treeNodes[0].pId;
				if (e.target.id == pId) {
					p = $(e.target);
				} else {
					p = $(e.target).parent('#' + pId);
					if (!p.get(0)) {
						p = null;
					}
				}

				// $('.domBtnDiv .active').removeClass('active');
				// if (p) {
				// 	p.addClass('active');
				// }
			},
			// dropTree2Dom: function(e, treeId, treeNodes, targetNode, moveType) {
			// 	var domId = "dom_" + treeNodes[0].getParentNode().id;
			// 	if (moveType == null && (domId == e.target.id || $(e.target).parents("#" + domId).length > 0)) {
			// 		var zTree = $.fn.zTree.getZTreeObj("treeDemo");
			// 		zTree.removeNode(treeNodes[0]);
            //
			// 		var newDom = $("span[domId=" + treeNodes[0].id + "]");
			// 		if (newDom.length > 0) {
			// 			newDom.removeClass("domBtn_Disabled");
			// 			newDom.addClass("domBtn");
			// 		} else {
			// 			$("#" + domId).append("<span class='domBtn' domId='" + treeNodes[0].id + "'>" + treeNodes[0].name + "</span>");
			// 		}
			// 		MoveTest.updateType();
			// 	} else if ( $(e.target).parents(".domBtnDiv").length > 0) {
			// 		alert(MoveTest.errorMsg);
			// 	}
			// },
			dom2Tree: function(e, treeId, treeNode) {
				var target = MoveTest.curTarget, tmpTarget = MoveTest.curTmpTarget;
				if (!target) return;
				var zTree = $.fn.zTree.getZTreeObj("treeDemo"), parentNode;
				if (treeNode != null && treeNode.isParent && "dom_" + treeNode.id == target.parent().attr("id")) {
					parentNode = treeNode;
				} else if (treeNode != null && !treeNode.isParent && "dom_" + treeNode.getParentNode().id == target.parent().attr("id")) {
					parentNode = treeNode.getParentNode();
				}

				if (tmpTarget) tmpTarget.remove();
				if (!!parentNode) {
					var nodes = zTree.addNodes(parentNode, {id:target.attr("domId"), name: target.text()});
					zTree.selectNode(nodes[0]);
				} else {
					target.removeClass("domBtn_Disabled");
					target.addClass("domBtn");
					alert(MoveTest.errorMsg);
				}
				MoveTest.updateType();
				MoveTest.curTarget = null;
				MoveTest.curTmpTarget = null;
			},
			updateType: function() {
				var zTree = $.fn.zTree.getZTreeObj("treeDemo"),
				nodes = zTree.getNodes();
				for (var i=0, l=nodes.length; i<l; i++) {
					var num = nodes[i].children ? nodes[i].children.length : 0;
					nodes[i].name = nodes[i].name.replace(/ \(.*\)/gi, "") + " (" + num + ")";
					zTree.updateNode(nodes[i]);
				}
			},
			bindDom: function() {
				$(".domBtnDiv").bind("mousedown", MoveTest.bindMouseDown);
			},
			bindMouseDown: function(e) {
				var target = e.target;
				if (target!=null && target.className=="domBtn") {
					var doc = $(document), target = $(target),
					docScrollTop = doc.scrollTop(),
					docScrollLeft = doc.scrollLeft();
					target.addClass("domBtn_Disabled");
					target.removeClass("domBtn");
					curDom = $("<span class='dom_tmp domBtn'>" + target.text() + "</span>");
					curDom.appendTo("body");

					curDom.css({
						"top": (e.clientY + docScrollTop + 3) + "px",
						"left": (e.clientX + docScrollLeft + 3) + "px"
					});
					MoveTest.curTarget = target;
					MoveTest.curTmpTarget = curDom;

					doc.bind("mousemove", MoveTest.bindMouseMove);
					doc.bind("mouseup", MoveTest.bindMouseUp);
					doc.bind("selectstart", MoveTest.docSelect);
				}
				if(e.preventDefault) {
					e.preventDefault();
				}
			},
			bindMouseMove: function(e) {
				MoveTest.noSel();
				var doc = $(document),
				docScrollTop = doc.scrollTop(),
				docScrollLeft = doc.scrollLeft(),
				tmpTarget = MoveTest.curTmpTarget;
				if (tmpTarget) {
					tmpTarget.css({
						"top": (e.clientY + docScrollTop + 3) + "px",
						"left": (e.clientX + docScrollLeft + 3) + "px"
					});
				}
				return false;
			},
			bindMouseUp: function(e) {
				var doc = $(document);
				doc.unbind("mousemove", MoveTest.bindMouseMove);
				doc.unbind("mouseup", MoveTest.bindMouseUp);
				doc.unbind("selectstart", MoveTest.docSelect);

				var target = MoveTest.curTarget, tmpTarget = MoveTest.curTmpTarget;
				if (tmpTarget) tmpTarget.remove();

				if ($(e.target).parents("#treeDemo").length == 0) {
					if (target) {
						target.removeClass("domBtn_Disabled");
						target.addClass("domBtn");
					}
					MoveTest.curTarget = null;
					MoveTest.curTmpTarget = null;
				}
			},
			bindSelect: function() {
				return false;
			}
		};

		var setting = {
		    check: {
                enable: true,
                chkboxType: {
                    "Y": "ps",
                    "N": "ps"
                }
            },
			edit: {
				enable: true,
				showRemoveBtn: false,
				showRenameBtn: false,
				drag: {
					prev: MoveTest.prevTree,
					next: MoveTest.nextTree,
					inner: MoveTest.innerTree
				}
			},
			data: {
				keep: {
					parent: true,
					leaf: true
				},
				simpleData: {
					enable: true
				}
			},
			callback: {
				beforeDrag: MoveTest.dragTree2Dom,
				onDrop: MoveTest.dropTree2Dom,
				onDragMove: MoveTest.dragMove,
				onMouseUp: MoveTest.dom2Tree
			},
			view: {
				selectedMulti: false
			}
		};

		// var zNodes =[
		// 	{ id:1, pId:0, name:"植物", isParent: true, open:true},
		// 	{ id:2, pId:0, name:"动物", isParent: true, open:true},
		// 	{ id:20, pId:2, name:"大象"},
		// 	{ id:29, pId:2, name:"鲨鱼"},
		// 	{ id:10, pId:1, name:"大白菜"},
		// 	{ id:19, pId:1, name:"西红柿"}
		// ];

		// $(document).ready(function(){
		// 	$.fn.zTree.init($("#treeDemo"), setting, zNodes);
		// 	MoveTest.updateType();
		// 	MoveTest.bindDom();
		// });
//
// var setting = {
//     check: {
//         enable: true,
//         chkboxType: {
//             "Y": "ps",
//             "N": "ps"
//         }
//     },
//     data: {
//         simpleData: {
//             enable: true
//         }
//     }
// };

function sortNumber(a,b){
  return a-b;
}

/*    编辑任务页面 设置选中的case状态    */
function setTreeValue(caselist){
    var treeObj = $.fn.zTree.getZTreeObj("treeDemo");
    var nodes = treeObj.transformToArray(treeObj.getNodes());
    var newObj = JSON.parse(caselist.replace(/&quot;/ig, '"'));
    var strArray = _.values(newObj);
    var strNew = [];
    var strOld = [];
    var tempNode = [];
    var x;
    _.each(strArray, function(str){
        strOld = _.union(strOld, str.split(','));
        strNew = _.union(strNew, str.split(',').sort(sortNumber));
    });
    for (x in nodes){
        for( j=0; j<strOld.length; j++){
            if (nodes[x].id == strOld[j]){
                var newNode = {};
                newNode.id = nodes[x].id;
                newNode.name = nodes[x].name;
                tempNode.push(newNode);
                treeObj.checkNode(nodes[x],true,true);
            }
        }
    }
    for (x in nodes){
        for( j=0; j<strNew.length; j++){
            if (nodes[x].id == strNew[j] && strNew[j]!=strOld[j]){
                for(index in tempNode){
                    if(tempNode[index].id == strOld[j]){
                        nodes[x].name = tempNode[index].name;
                        nodes[x].id = tempNode[index].id;
                        break;
                    }
                }
                break;
            }
        }
    }
}
var zNodes = [];

$(document).ready(function () {
    $.fn.zTree.init($("#treeDemo"), setting, zNodes);
    MoveTest.updateType();
    MoveTest.bindDom();
    /*    通过project关联module树   */
    $("#selprojectid_task").bind("change", function () {
        var s1SelectedVal = $('#selprojectid_task').val();
        var issmoke = $('#issmoke').val();
        $.ajax({
            type: "GET",
            data: {'projectid': s1SelectedVal,'issmoke':issmoke},//$(this).serialize()
            url: "/setting/get/moduleList/", //后台处理函数的url 这里用的是static url 需要与urls.py中的name一致
            cache: false,
            dataType: 'text',
            success: function (result, TextStatus) {
                zNodes = eval(result)
                $.fn.zTree.init($("#treeDemo"), setting, zNodes);
            },
            error: function (result) {
                alert(result)
            }

        });
    });

    $("#selprojectid_task_edit").change();

});


//行添加
function addtr() {
    rowid = $('#rowid').val();
    var len = parseInt($("#linecounter").val()) + 1;

    $("#tab tbody").append('<tr id=row' + len + ' name="rowstep">'
        + '<td>' + len + '</td>'
        + '<td><input name="codedescr" class="ac-acaseedit-input" placeholder="参数描述" type="input" required=""></td>'
        + '<td><input name="codename" class="ac-acaseedit-input" placeholder="参数编码(MWIP)" type="input" required=""></td>'
        + '<td><input name="codevalue" class="ac-acaseedit-input ac-acode-desc" placeholder="参数值" type="input" required=""></td>'
        + '<td><a class="btn btn-small btn-link" onclick="deltr(' + len + ')">删除</a></td>'
        + '</tr>');
    $("#linecounter").val(len);
    if (rowid != '') {
        $('#row' + len).insertAfter('#row' + rowid);
    }
    $('#rowid').val('');
}
//行删除
function deltr(index) {
    $("tr[id='row" + index + "']").remove();//删除当前行
}