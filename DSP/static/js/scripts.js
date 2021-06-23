// $(function() {
//     $('#submit').click(function(e) {
//         e.preventDefault();    
//         alert(1);
//         $.ajax({
//             type: "POST",
//             url: '/uploader',
//             data: $("#form").serialize() +  "&var1=blah"
//             cache: 'false',
//             processData: false,
//             dataType: 'json',
//             success: function(data)
//             {
//                 console.log(data); 
//             },
//             error: function(data)
//             {
//                 console.log(data); 
//                 console.log("error");
//             }
//         })
//         event.preventDefault();
//     });
// });

$(function() {
    $('#upload').click(function() {
    event.preventDefault();
    let form_data = new FormData($('#uploadform')[0]);
    form_data.append("filename", $("#filename").val())
    form_data.append("secret", $("#secret").val())
    form_data.append("method", $(this).val())

    alert(form_data);
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
            console.log($("#secret").val());
            $('#texthere').html($("#secret").val());
        }
        });
    })
});


$(document).ready(function() {
    $('#button').click(function() {
        $.ajax({
            url: 'your.file',
            type: 'GET',
            success: function(data) {
                $('#texthere').html(data);
            }
        });
    });
});