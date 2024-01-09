let js_swal_title = window.data.js_swal_title
let js_swal_text = window.data.js_swal_text
let js_swal_confirmButtonText = window.data.js_swal_confirmButtonText
let js_swal_cancelButtonText = window.data.js_swal_cancelButtonText
document.querySelectorAll("a.delete_href").forEach((ref) => {
    ref.addEventListener("click", function (e) {
        e.preventDefault()
        let record = "\n" + e.target.parentElement.attributes['is'].nodeValue
        console.log(record)
        swal.fire({
            title: js_swal_title + record,
            text: js_swal_text,
            icon: 'question',
            showCancelButton: true,
            confirmButtonColor: '#3085d6',
            cancelButtonColor: '#d33',
            confirmButtonText: js_swal_confirmButtonText,
            cancelButtonText: js_swal_cancelButtonText,
            backdrop: true,
            showLoaderOnConfirm: true,
            preConfirm:()=>{
                location.href = e.target.parentElement.href
            },
            allowOutsideClick:()=>false,
            allowEscapeKey:()=>false
        })
    })
})
