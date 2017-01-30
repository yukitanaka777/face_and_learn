var clm = new clm.tracker({useWebGL:true});
var fb = new faceDeformer();
var masking_switch = false;
var dataCtn = 0;
var maskAnimDate
var canvas;
var FaceImgArr = {};

$(function(){
	canvas = document.getElementById('canvas');
	clm.init(pModel);
    $.getJSON('./static/position.json',function(data){
	    maskAnimDate = data;
	});

    loadImage(ImgURL, function (img) {
      drawImage(img);
    });

	fb.init(canvas);
});

function rendering(){
	if(masking_switch && dataCtn < Object.keys(maskAnimDate).length){
		masking(maskAnimDate[dataCtn]);
		dataCtn++;
		if((dataCtn % 15) == 0){
			var cImg = canvas.toDataURL('image/jpeg');
			FaceImgArr[dataCtn] = cImg;
		}
		requestAnimationFrame(rendering);
	}else if(dataCtn == Object.keys(maskAnimDate).length){
		$.ajax({
    		type: 'POST',
    		contentType: 'application/json',
    		url: "http://localhost:8000/save_json",
    		dataType : 'json',
    		data : JSON.stringify(FaceImgArr_data),
    		success : function(result) {
    		},error : function(result){
       			console.log(result);
    		}
		});
		console.log('hinish');
		cancelAnimationFrame(rendering);
	}
	console.log("hi");
}

function masking_init(maskingPos){
    var MaskImg = document.createElement("img");
	MaskImg.onload = function(){
		console.log(pModel);
		fb.load(MaskImg,maskingPos,pModel);
		masking_switch = true;
		rendering();
	}
	MaskImg.src = ImgURL;
}

function masking(masPos){
	if(masPos){
		fb.draw(masPos);
	}else{
	    console.log(masPos);
	}
}

function drawImage(img) {
	var model = document.getElementById('model');
    var mtx = model.getContext('2d');
    var imgW = img.width;
    var imgH = img.height;

    mtx.drawImage(img, 0, 0, imgW,imgH);
    clm.init(pModel);
    clm.start(model);
	certain_clm_pos();
}

function certain_clm_pos(){
	if(clm.getCurrentPosition()){
		maskingPos = clm.getCurrentPosition();
		masking_init(maskingPos);
	}else{
	    console.log("not get pos");
		setTimeout(function(){
			certain_clm_pos();
		},1000);
	}
}

