
// Confirm Delete

$(document).on('click', '.delete-confirm', function(){
    return confirm('Are you sure you want to delete this?');
})

// Contact Details

$(document).on('click', '.contact-advertiser', function(){
    return document.getElementById('advertiser-phone').classList.remove("d-none");
})

// Datepicker