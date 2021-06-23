var fileTypes = ['pdf', 'docx', 'rtf', 'jpg', 'jpeg', 'png', 'txt','wav'];  //acceptable file types
function readURL(input) {
    if (input.files && input.files[0]) {
        var extension = input.files[0].name.split('.').pop().toLowerCase(),  //file extension from input file
            isSuccess = fileTypes.indexOf(extension) > -1;  //is extension in acceptable types

        if (isSuccess) { //yes
            var reader = new FileReader();
            reader.onload = function (e) {
                if (extension == 'pdf'){
                	$(input).closest('.fileUpload').find(".icon").attr('src','https://image.flaticon.com/icons/svg/179/179483.svg');
                }
                else if (extension == 'docx'){
                	$(input).closest('.fileUpload').find(".icon").attr('src','https://image.flaticon.com/icons/svg/281/281760.svg');
                }
                else if (extension == 'rtf'){
                	$(input).closest('.fileUpload').find(".icon").attr('src','https://image.flaticon.com/icons/svg/136/136539.svg');
                }
                else if (extension == 'png'){ $(input).closest('.fileUpload').find(".icon").attr('src','https://image.flaticon.com/icons/svg/136/136523.svg'); 
                }
                else if (extension == 'jpg' || extension == 'jpeg'){
                	$(input).closest('.fileUpload').find(".icon").attr('src','https://image.flaticon.com/icons/svg/136/136524.svg');
                }
                else if (extension == 'wav') {
                  $(input).closest('.fileUpload').find(".icon").attr('src','https://img.icons8.com/nolan/64/audio-file.png');
                }
                else if (extension == 'txt'){
                	$(input).closest('.fileUpload').find(".icon").attr('src','https://image.flaticon.com/icons/svg/136/136538.svg');
                }
                else {
                	//console.log('here=>'+$(input).closest('.uploadDoc').length);
                	$(input).closest('.uploadDoc').find(".docErr").slideUp('slow');
                }
            }

            reader.readAsDataURL(input.files[0]);
        }
        else {
        		//console.log('here=>'+$(input).closest('.uploadDoc').find(".docErr").length);
            $(input).closest('.uploadDoc').find(".docErr").fadeIn();
            setTimeout(function() {
				   	$('.docErr').fadeOut('slow');
					}, 9000);
        }
    }
}
$(document).ready(function(){
   
   $(document).on('change','.up', function(){
   	var id = $(this).attr('id'); /* gets the filepath and filename from the input */
	   var profilePicValue = $(this).val();
	   var fileNameStart = profilePicValue.lastIndexOf('\\'); /* finds the end of the filepath */
	   profilePicValue = profilePicValue.substr(fileNameStart + 1).substring(0,20); /* isolates the filename */
	   //var profilePicLabelText = $(".upl"); /* finds the label text */
	   if (profilePicValue != '') {
	   	//console.log($(this).closest('.fileUpload').find('.upl').length);
	      $(this).closest('.fileUpload').find('.upl').html(profilePicValue); /* changes the label text */
	   }
   });

//    $(".btn-new").on('click',function(){
//         $("#uploader").append('<div class="row uploadDoc"><div class="col-sm-3"><div class="docErr">Please upload valid file</div><!--error--><div class="fileUpload btn btn-orange"> <img src="https://image.flaticon.com/icons/svg/136/136549.svg" class="icon"><span class="upl" id="upload">Upload document</span><input type="file" class="upload up" id="up" onchange="readURL(this);" /></div></div><div class="col-sm-8"><input type="text" class="form-control" name="" placeholder="Note"></div><div class="col-sm-1"><a class="btn-check"><i class="fa fa-times"></i></a></div></div>');
//    });
    
   $(document).on("click", "a.btn-check" , function() {
     if($(".uploadDoc").length>1){
        $(this).closest(".uploadDoc").remove();
      }else{
        alert("You have to upload at least one document.");
      } 
   });
});

$(function() {
    $('#encode').click(function() {
    event.preventDefault();
    let form_data = new FormData($('#uploadform')[0]);
    form_data.append("filename", $("#filename").val())
    form_data.append("secret", $("#secret").val())
    form_data.append("method", $(this).val())

    console.log($(this).val());
    $.ajax({
        type : "POST",
        url : "/uploader",
        contentType: false,
        cache: false,
        processData: false,
        data: form_data,
        success: function(data) {
            // alert(val);
            alert($("#secret").val());
            console.log(data);
            $('#texthere').html(data.encode);
        }
    })
    })
});

$(function() {
    $('#decode').click(function() {
    event.preventDefault();
    let form_data = new FormData($('#uploadform')[0]);
    form_data.append("filename", $("#filename").val())
    form_data.append("method", $(this).val())

    console.log($(this).val());
    $.ajax({
        type : "POST",
        url : "/uploader",
        contentType: false,
        cache: false,
        processData: false,
        data: form_data,
        success: function(data) {
            // alert(val);
            console.log(data);
            $('#texthere').html(data.decode);
        }
    })
    })
});