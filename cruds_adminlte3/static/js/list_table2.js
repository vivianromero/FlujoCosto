const hrefsDelete2 = document.querySelectorAll("a.delete_href")
let js_swal_title2 = window.data.js_swal_title
let js_swal_text2 = window.data.js_swal_text
let js_swal_confirmButtonText2 = window.data.js_swal_confirmButtonText
let js_swal_cancelButtonText2 = window.data.js_swal_cancelButtonText
hrefsDelete2.forEach((ref) => {
    ref.addEventListener("click", function (e) {
        e.preventDefault()
        swal.fire({
            title: js_swal_title2,
            text: js_swal_text2,
            icon: 'question',
            showCancelButton: true,
            confirmButtonColor: '#3085d6',
            cancelButtonColor: '#d33',
            confirmButtonText: js_swal_confirmButtonText2,
            cancelButtonText: js_swal_cancelButtonText2,
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
