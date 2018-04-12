$(document).ready(function(){
	$($(".install")[0]).css('display','block');
	$("#directional button").bind("click",function(){
		$("#directional button").removeClass("active");
		$(this).addClass("active");
		var index_num = $(this).index();
		var install = $(".install");
		$(".install").css('display','none');
		$(install[index_num]).css('display','block');
	})
	
})

function readdata(){
	var name = $(this);
	console.log(name);
	
}