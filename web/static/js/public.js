//验证手机号码
var checkphone = function(phone){
	var reg = /^0?1[3|4|5|8][0-9]\d{8}$/;
	if (reg.test(phone)) {
	    return true;
	}else{
	    return false;
	}
}