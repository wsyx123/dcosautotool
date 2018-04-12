function deploy_component(){
	$("#deploy-host").html($("select[name='host']").val());
	$("#deploy-name").html($("input[name='name']").val());
	$.ajax({
		type:'POST',
		url:'',
		data:$("#component-form").serialize(),
		success: function(data){
			var dataObj=eval("("+data+")");
			if( dataObj.status == 'success' ){
				$("#modal-body div").remove();
				$("#modal-body #deploying").remove();
				$("#modal-body #deploy-success").html('部署完成');
				$(".modal-footer button").removeClass('disabled');
				$(".modal-footer button").attr('data-dismiss',"modal");
				clearInterval(time1);
			}
			if( dataObj.status == 'failure' ){
				$("#modal-body div").remove();
				$("#modal-body #deploying").remove();
				$("#modal-body #deploy-failure").html(dataObj.msg);
				$(".modal-footer button").removeClass('disabled');
				$(".modal-footer button").attr('data-dismiss',"modal");
				clearInterval(time1);
			}
		},
	})
}

function delete_component_ask(obj){
	thisobj = $(obj);
	name = $(obj).siblings().eq(1).html();
	host = $(obj).siblings().eq(2).html();
	$("#delete-host").html(host);
	$("#delete-name").html(name);
}

function delete_component_ensure(obj){
	$.ajax({
		type:'POST',
		url:'delete/',
		data:{'name':name,'host':host},
		success: function(data){
			var dataObj=eval("("+data+")");
			if( dataObj.status == 'success' ){
				$("#mySuccessAlert").css('display','block');
				$(thisobj).parent().remove();
			}
			if( dataObj.status == 'failure' ){
				$("#myFailureAlert").css('display','block');
				$("#delete-failure").html(dataObj.msg)
			}
		}
		
	})
}

function deploy_finish(){
	window.location.href='/platform/manage/';
}