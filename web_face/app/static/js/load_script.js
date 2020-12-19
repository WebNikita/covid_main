let dropArea = document.getElementById('drop-area')

;['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
  dropArea.addEventListener(eventName, preventDefaults, false)
})
function preventDefaults (e) {
  e.preventDefault()
  e.stopPropagation()
}

;['dragenter', 'dragover'].forEach(eventName => {
  dropArea.addEventListener(eventName, highlight, false)
})
;['dragleave', 'drop'].forEach(eventName => {
  dropArea.addEventListener(eventName, unhighlight, false)
})
function highlight(e) {
  dropArea.classList.add('highlight')
}
function unhighlight(e) {
  dropArea.classList.remove('highlight')
}

dropArea.addEventListener('drop', handleDrop, false)
function handleDrop(e) {
  let dt = e.dataTransfer
  let files = dt.files
  handleFiles(files)
}

function handleFiles(files) {
  ([...files]).forEach(uploadFile)
}


function uploadFile(file) {
  var url = 'https://dt-miet.ru/warehouse/import'
  var xhr = new XMLHttpRequest()
  var formData = new FormData()
  xhr.open('POST', url, true)
  xhr.addEventListener('readystatechange', function(e) {
  	console.log(xhr.responseText)
  	if (xhr.status != 200) {
        console.log(xhr.status);
    } else {
    	if (xhr.responseText == "error") {
      		document.getElementById("import_allert").innerHTML = `
					<div class="alert alert-danger alert-dismissible fade show" role="alert">
                    <strong>Ошибка!</strong>Не верный формат!
                    <button type="button" class="close" data-dismiss="alert" aria-label="Close">
                        <span aria-hidden="true">&times;</span>
                    </button>
                    </div>
      `
    }
    else if (xhr.readyState == 4 && xhr.status == 200) {
     	 document.getElementById("import_allert").innerHTML = `
					<div class="alert alert-success alert-dismissible fade show" role="alert">
                    <strong>Файл успешно загружен!</strong>Позиции добавлены в БД!
                    <button type="button" class="close" data-dismiss="alert" aria-label="Close">
                        <span aria-hidden="true">&times;</span>
                    </button>
                    </div>
      `
    }
    else if (xhr.readyState == 4 && xhr.status != 200) {
      document.getElementById("import_allert").innerHTML = `
					<div class="alert alert-danger alert-dismissible fade show" role="alert">
                    <strong>Ошибка!</strong> Непредвиденная ошибка, свяжитесь с @nshvora в Telegram.
                    <button type="button" class="close" data-dismiss="alert" aria-label="Close">
                        <span aria-hidden="true">&times;</span>
                    </button>
                    </div>
      `
    }


    }
   
    
  })
  formData.append('file', file)
  xhr.send(formData)
}
