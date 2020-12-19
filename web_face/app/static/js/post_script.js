function send_post(text){
    var xhr = new XMLHttpRequest();
    var obj
    var click_data
    xhr.open('POST', 'https://dt-miet.ru/warehouse/index', false);
            
    xhr.send([text]);
    if (xhr.status != 200) {
        console.log(xhr.status);
    } else {
        document.getElementById("table_info").innerHTML = '';
        obj = JSON.parse(xhr.responseText);
        if (Object.keys(obj)[0] == 'warehouse_admin_info'){
            for (var i = 0; i < Object.keys(obj['warehouse_admin_info']).length + 1; i++){
                click_data = `${obj['warehouse_admin_info'][i][0]}|${obj['warehouse_admin_info'][i][1]}|${obj['warehouse_admin_info'][i][2]}`
                document.getElementById("table_info").innerHTML += `<tr><td id='name'>${obj['warehouse_admin_info'][i][0]}</td><td id='cell'>${obj['warehouse_admin_info'][i][1]}</td><td id='count'>${obj['warehouse_admin_info'][i][2]}</td><td><button type="button" onclick="plaseholder_edit('${click_data}')" class="btn btn-primary" data-toggle="modal" data-target="#editModal">Изменить</button></td><tr>`;
            }
        } else {
            for (var i = 0; i < Object.keys(obj['warehouse_client_info']).length + 1; i++){
                click_data = `'order|${obj["warehouse_client_info"][i][0]}|${obj["warehouse_client_info"][i][2]}|${obj["warehouse_client_info"][i][3]}'`;
                document.getElementById("table_info").innerHTML += `<tr><td id="name">${obj['warehouse_client_info'][i][0]}</td><td id="count">${obj['warehouse_client_info'][i][1]}</td><td><button type="button" onclick="modal_window(${click_data})" class="btn btn-primary" data-toggle="modal" data-target="#exampleModal">Заказать</button></td><tr>`;
            }
        }
    }

};

function modal_window(text){
    var info = text.split("|")
     
    document.getElementById("recipient_name").value = info[3];

    document.getElementById("modal_window").innerHTML = '';
    document.getElementById("modal_window").innerHTML += `
<button  type="button" class="btn btn-secondary" data-dismiss="modal">Закрыть</button>
<button  type="button" class="btn btn-secondary" data-dismiss="modal" id="post_button" onclick="order('${text}')">Отправить</button>
`;
};


function add_email_window(name){
    document.getElementById("modal_window_email").innerHTML = '';
    document.getElementById("modal_window_email").innerHTML += `
    <button  type="button" class="btn btn-secondary" data-dismiss="modal">Закрыть</button>
    <button  type="button" class="btn btn-secondary" data-dismiss="modal" id="post_button" onclick="add_email_post('${name}')">Привязать</button>
    `   ;
};


function add_email_post(name){
    var xhr = new XMLHttpRequest();

    var data = {
                    "name": name,
                    "email": document.getElementById("email_name").value
                 };

    xhr.open('POST', 'https://dt-miet.ru/warehouse/add_email', false);
    xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    xhr.send(JSON.stringify(data));
}

// function modal_window_edit(text){
//     document.getElementById("modal_window").innerHTML = '';
//     document.getElementById("modal_window").innerHTML += `
// <button  type="button" class="btn btn-secondary" data-dismiss="modal">Закрыть</button>
// <button  type="button" class="btn btn-secondary" onclick="order('${text}')">Отправить</button>
// `;
// };

function order(text){

    var xhr = new XMLHttpRequest();
    var click_data    

    click_data = `${text}|${document.forms["post_form"].elements["recipient_count"].value}|${document.forms["post_form"].elements["message_text"].value}`
    
    xhr.open('POST', 'https://dt-miet.ru/warehouse/bot', false);
    
    xhr.send([click_data]);
    
    if (xhr.status != 200) {
        console.log(xhr.status);
    } else {
        if (xhr.responseText == "Error") {
            document.getElementById("allert").innerHTML = `
                <div class="alert alert-danger alert-dismissible fade show" role="alert">
                    <strong>Ошибка!</strong> Вы пытаетесь взять больше чем есть на складе!
                    <button type="button" class="close" data-dismiss="alert" aria-label="Close">
                        <span aria-hidden="true">&times;</span>
                    </button>
                </div>`;
        }
        if (xhr.responseText == "Zero") {
            document.getElementById("allert").innerHTML = `
                <div class="alert alert-danger alert-dismissible fade show" role="alert">
                    <strong>Ошибка!</strong> Вы пытаетесь взять 0 штук!
                    <button type="button" class="close" data-dismiss="alert" aria-label="Close">
                        <span aria-hidden="true">&times;</span>
                    </button>
                </div>`;
        }
        if (xhr.responseText == "ok") {
            document.getElementById("allert").innerHTML = `
                    <div class="alert alert-success alert-dismissible fade show" role="alert">
                    <strong>Запрос отправлен!</strong> Ожидайте уведомления о выдачи товара.
                    <button type="button" class="close" data-dismiss="alert" aria-label="Close">
                        <span aria-hidden="true">&times;</span>
                    </button>
                    </div>
                    `;
        }
        if (xhr.responseText == "No_data") {
            document.getElementById("allert").innerHTML = `
                    <div class="alert alert-danger alert-dismissible fade show" role="alert">
                    <strong>Запрос не отправлен!</strong> Привяжите телеграм или почту!
                    <button type="button" class="close" data-dismiss="alert" aria-label="Close">
                        <span aria-hidden="true">&times;</span>
                    </button>
                    </div>
                    `;
        }
    }

}

function plaseholder_edit(text){
    var info = text.split("|")
    document.getElementById("modal_window_edit").innerHTML = '';
    document.getElementById("modal_window_edit").innerHTML += `
<button  type="button" class="btn btn-secondary" data-dismiss="modal">Закрыть</button>
<button  type="button" class="btn btn-secondary" data-dismiss="modal" onclick="edit()">Изменить</button>
    `;
    document.getElementById("edit_name").value = info[0];
    document.getElementById("edit_count").value = info[1];
    document.getElementById("edit_text").value = info[2];

}

function edit(){

    var xhr = new XMLHttpRequest();
    
    var data = `${document.forms["post_form_edit"].elements["edit_name"].value}|${document.forms["post_form_edit"].elements["edit_count"].value}|${document.forms["post_form_edit"].elements["edit_text"].value}`;

    xhr.open('POST', 'https://dt-miet.ru/warehouse/edit', false);
    
    xhr.send([data]);
    
    if (xhr.status != 200) {
        console.log(xhr.status);
    } else {
        var obj = JSON.parse(xhr.responseText);
        send_post(obj['info'])
    }

}


function addposition_post(){
    var xhr = new XMLHttpRequest();

    var data = {
                    "name": document.getElementById("addposition_name").value,
                    "category": document.getElementById("addposition_category").value,
                    "cell": document.getElementById("addposition_cell").value,
                    "count": document.getElementById("addposition_count").value
                }

    xhr.open('POST', 'https://dt-miet.ru/warehouse/add_position', false);
    xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    xhr.send(JSON.stringify(data));
    window.location.reload();
};
