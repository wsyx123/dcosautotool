$(document).ready(function(){
var myURL = document.location.pathname;
var myURLlen = myURL.split('/');  //判断  url 路径长度 ，如果>=4 就是二级菜单，需要设置collapse,设置 active
var myNav = $("#col-md-2 .nav li > a");
if(myURLlen.length >=4){
	var secondmenu = myURLlen[1];
	$("#"+secondmenu).collapse('show');
	var secondNav = $("#"+secondmenu).children().find("a");
	setliactive(myURL,secondNav);
	$("#col-md-2 .nav-header span").toggleClass("glyphicon-chevron-down");
}else{
	setliactive(myURL,myNav);
}

$("#col-md-2 .nav-header").bind("click",function(){
	$("#col-md-2 .nav-header span").toggleClass("glyphicon-chevron-down");
});


});

function setliactive(myURL,myNav){
	for(i=0;i<myNav.length;i++){
		var links = myNav[i].getAttribute("href");
		if(myURL == links){
		    $(myNav[i]).parent().addClass("active");
		   }
		if(myURL == '/'){
			$(myNav[0]).parent().addClass("active");
		}
	};
}