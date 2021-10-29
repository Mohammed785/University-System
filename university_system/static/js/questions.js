const answerForms = document.querySelectorAll('.answer-form');
const editBtns = document.querySelectorAll('.edit-btn');

var editFlag = false;
var endpoint = '';
editBtns.forEach(btn => {
    btn.addEventListener('click', function (e) {
        editFlag = true;
        const answerSlug = $(btn).data('answerslug');
        endpoint = `http://127.0.0.1:8000/api/v1/answer/${answerSlug}/update/`
        const answerBody = e.target.parentElement.previousElementSibling.children[1].firstChild.data
        let formInput = e.target.parentElement.parentElement.parentElement.parentElement.nextElementSibling[1]
        let formBtn = e.target.parentElement.parentElement.parentElement.parentElement.nextElementSibling[2]
        formInput.value = answerBody
        formBtn.innerText = 'Update'
    })
})

answerForms.forEach(form => {
    form.addEventListener('submit', e => {
        let body = e.target[1]
        let btn = e.target[2]
        const token = e.target[0].value;
        if (body.value) {
            if (editFlag === false) {
                let questionSlug = $(form).data('questionslug');
                let answerPostEndpoint = `http://127.0.0.1:8000/api/v1/question/${questionSlug}/answer/create/`
                apiCall('POST', answerPostEndpoint, body.value, token)
                body.value = ''
            }
            else {
                apiCall("PUT", endpoint, body.value, token)
                editFlag = false
                body.value = ''
                btn.innerText = 'Submit'
            }
        }
        else {
            alert("Please Enter A Answer Before Submit")
        }
    })
})

function apiCall(method, endpoint, body, token) {
    $.ajax({
        method: method,
        url: endpoint,
        data: { body },
        headers: { "X-CSRFToken": token },
        success: (data) => {
            console.log(data);
        },
        error: (e) => {
            console.error(e)
        }
    })
}
