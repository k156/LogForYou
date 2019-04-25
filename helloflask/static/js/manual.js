
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
    
    $('#main-block').remove();


    var url = '/main/s'
    send_ajax(url, 'POST', {"s":input}, 'json', 
        function(res){
            console.log(res);
            // hbs('search-template', res, 'search-result')
            hbs('search-template', res, 'patients', true)
        }
    );
}



function hbs(sourceId, data, resultId, isFirst=true){
    
    var source = document.getElementById(sourceId).innerHTML;
    var template = Handlebars.compile(source);
    
    if (isFirst){
        var html = template(data);
        document.getElementById(resultId).innerHTML = html;
    }
    else{
        var html = template(data);
        document.getElementById(resultId).innerHTML += html;
    }
}

function send_ajax(url, method, data, dataType, fn) {
    var options = {
        url: url,
        data: data,
        type: method,
        dataType: dataType
    };

    if (dataType == 'ajson')
        options.contentType= 'application/json';

    $.ajax(options).done(function (res) {
        if (fn)
            fn(res)

    }).fail(function (xhr, status, errorThrown) {
        console.error("Sorry, there was a problem!", xhr, status, errorThrown);

    }).always(function (xhr, status) {
        console.log("The request is complete!");
    });
}

var main_url = window.location.href
let pat_id = null;

function open_modal(value){
    pat_id = value
    document.getElementById('badge').innerHTML = ""

    send_ajax('/main', 'POST', "", "json", function(res2){
        hbs("col-template", res2, 'badge', true)
    });
    $('#rgModal').show();
}

$( document ).ready(function() {
    if ( main_url === "http://localhost:5000/main") {
        send_ajax('/main/r', 'POST', "", "json", function(res){

            // QQQ 의사 로그인 후 나의 환자 목록
            // hbs("mypat-template", res, "patients")
        });
        send_ajax('/main', 'POST', "", "json", function(res2){
 
            hbs("discode-template", res2, 'discode_list', false);
            hbs("colmaster-template", res2, 'col_list', false);
            hbs("col-template", res2, 'badge', true);
        });
        
    } else if ( main_url === "http://localhost:5000/logs" ) {
        // drawing table with handlebars
        draw_table(data.pat_id);
        
        
        window.onload = function () {
            
            
            
        };
};});


function draw_table(v){
    send_ajax('/logs/r', 'POST', {id : v}, "json", function(res6) {
        console.log("res6>>>>> ", res6);
        console.log("res6>>>>> ", res6['head']);
        console.log("res6>>>>> ", res6['body']);

        var sc = document.createElement('script');
        sc.id = "tbody-template"
        sc.type = "text/x-handlebars-template"

        var td = ""
        for(var i = 0; i < res6['head'].length; i++) { td += "<td>{{col_"+i+"}}</td>" }
        // document.getElementById("myDIV").appendChild(para);
        // td += "<td></td>"
        var tr = "{{#each body}}<tr><td>{{date}}</td>"+td+"</tr>{{/each}}";
        sc.innerHTML = tr;
        document.body.appendChild(sc);


        // hbs("test-template", res6, "test")
        hbs('thead-template', res6, 'log_thead');
        hbs('tbody-template', res6, 'log_tbody');
        hbs('thead-template', res6, 'log_tfoot');

        $('#dtMaterialDesignExample').DataTable({
            "pagingType": "first_last_numbers" // "simple" option for 'Previous' and 'Next' buttons only
          })
        $('.dataTables_length').addClass('bs-select');

    })        
};   


function add_col(id){
    
    var $badges = $.makeArray($("span.badge").map(function(){
        return $(this).attr("id");
    }));

    var $value = document.getElementById(id).value;

    send_ajax('/main/add_col/'+id, 'POST', {'id' : $value}, "json", function(res4){
        var di = null;
        
        for(var i in res4['result']) {
            $badges.find(function(item) {
                var j = res4['result'][i];
                if (item == j['id']){
                    di = res4['result'].indexOf(j);
                    if(di>-1) res4['result'].splice(di, 1);
                }
            });
        }
        hbs('col-template', res4, 'badge', false);
    });

};


function get_complete_columns(){
    // console.log("get_complete_columns============ ")
    var $badge = $('#badge span');
    var data = [];
    var data1 = [];
    var discode = $('#discode_list').val()
    // console.log("discode >>> ", discode)
    data.push({'pat_id':pat_id})
    data.push({'discode':discode})
    for (var i = 0, len = $badge.length; i < len; i++) {
        col_id = $badge[i].id;
        data1[i] = col_id;
    };
    data.push({"col_id":data1});
    // console.log("data>>>>>>>>>", data)
    
    send_ajax('/main/w', 'POST', {req : data}, 'json', function(res5){
        console.log("res5>>>>>", res5);
    })
}

function remove_element(value) {
    var id = '#' + value;
    $(id).remove();
}