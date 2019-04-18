$

var isDocShown = false, isPatShown = false;
    
// 각 유저별 로그인박스 보여주는 함수
function showLoginForm(value){
    if (!isDocShown & value == 'd') {
    isDocShown = true;
    isPatShown = false;
    $('#loginform_doctor').show();
    $('#loginform_patient').hide();
    }else if (!isPatShown & value == 'p') {
    isDocShown = false;
    isPatShown = true;
    $('#loginform_doctor').hide();
    $('#loginform_patient').show();
    }else if ((isDocShown & value == 'd') | (isPatShown & value == 'p')) {
    isDocShown = false;
    isPatShown = false;
    $('#loginform_doctor').hide();
    $('#loginform_patient').hide(); 
    }
};


// QQQ 환자 검색 기능 만들기
// $('form').on('submit', function(event, tag) {
//     console.log("aaaa")
//     // Prevent the page from reloading
//     event.preventDefault();
//     event.stopPropagation();

//     // Set the text-output span to the value of the first input
//     var $input = $(this).find('input');
//     console.log($(this))
//     var input = $input.val();
//     console.log(input)
//     console.log(tag)
// })

function search(event) {
    console.log("aaaaa", ...arguments)
    console.log(event)
    // Prevent the page from reloading
    event.preventDefault();
    event.stopPropagation();

    // Set the text-output span to the value of the first input
    // var $input = $(this).find('input');
    var $input = $('input')
    console.log(">>>>", $input)
    var input = $input.val();
    console.log(input)
    
    var url = '/main/s'
    send_ajax(url, 'POST', {"s":input}, 'json', 
        function(res){
            console.log(res);
            hbs('search-template', res, )
        }
    );
}

function hbs(sourceId, data, resultId){
    var source = document.getElementById(sourceId).innerHTML;
    var template = Handlebars.compile(source);
    var html = template(data);
    document.getElementById(resultId).innerHTML = html;
}

function send_ajax(url, method, data, dataType, fn) {
    $.ajax({
        url: url,
        data: data,
        type: method,
        dataType: dataType

    }).done(function (res) {
        if (fn)
            fn(res)

    }).fail(function (xhr, status, errorThrown) {
        console.error("Sorry, there was a problem!", xhr, status, errorThrown);

    }).always(function (xhr, status) {
        console.log("The request is complete!");
    });
}
