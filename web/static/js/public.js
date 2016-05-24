var nav_width = $(".nav").width()
var action_offset_left = $('.action').offset().left
var action_index = $(".nav li").index($('.action').parent())
if (action_index>2 ) {
	var left = action_offset_left-nav_width/2+15
	$('.nav').scrollLeft(left)
};
//验证手机号码
var checkphone = function(phone){
	var reg = /^0?1[3|4|5|8][0-9]\d{8}$/;
	if (reg.test(phone)) {
	    return true;
	}else{
	    return false;
	}
}
$('.content img').each(function(){
	if ($(this).width()>$('.content').width()) {
		$(this).removeAttr('style');
		$(this).css({'width':$('.content').width()});
	};
})
$('.temple-content img').each(function(){
	if ($(this).width()>$('.temple-content').width()) {
		$(this).removeAttr('style');
		$(this).css({'width':$('.temple-content').width()});
	};
})
$('.born img').each(function(){
	if ($(this).width()>$('.born').width()) {
		$(this).removeAttr('style');
		$(this).css({'width':$('.born').width()});
	};
})
$('.mage-content img').each(function(){
	if ($(this).width()>$('.mage-content').width()) {
		$(this).removeAttr('style');
		$(this).css({'width':$('.mage-content').width()});
	};
})
$('.goodraise-content img').each(function(){
	if ($(this).width()>$('.goodraise-content').width()) {
		$(this).removeAttr('style');
		$(this).css({'width':$('.goodraise-content').width()});
	};
})
$('.activity-content img').each(function(){
	if ($(this).width()>$('.activity-content').width()) {
		$(this).removeAttr('style');
		$(this).css({'width':$('.activity-content').width()});
	};
})
$('.new-content img').each(function(){
	if ($(this).width()>$('.new-content').width()) {
		$(this).removeAttr('style');
		$(this).css({'width':$('.new-content').width()});
	};
})
$('.news-text img').each(function(){
	if ($(this).width()>$('.news-text').width()) {
		$(this).removeAttr('style');
		$(this).css({'width':$('.news-text').width()});
	};
})
$('.volunteer-content img').each(function(){
	if ($(this).width()>$('.volunteer-content').width()) {
		$(this).removeAttr('style');
		$(this).css({'width':$('.volunteer-content').width()});
	};
})
