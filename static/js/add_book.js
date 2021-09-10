$(document).ready(function($) {
    const urlParams = new URLSearchParams(window.location.search);
    const book_id = urlParams.get('book_id');

    function getBookDetails(book_id){
        $.ajax({
            url: "/api/v1/manage_book?action=get_book_details",
            dataType: 'json',
            data: {
                'book_id': book_id
            }
        })
        .done(function(response) {
            if (response.status) {
                let data = response.data;
                $('input[name="book_title"]').val(data[1]);
                $('input[name="book_subtitle"]').val(data[2]);
                $('select[name="book_lang"]').val(data[3]);
                $('input[name="author"]').val(data[4]);
                $('input[name="isbn"]').val(data[5]);
                $('input[name="edition"]').val(data[6]);
                $('input[name="orig_price"]').val(data[7]);
                $('input[name="curr_price"]').val(data[8]);
                $('select[name="book_volume"]').val(data[9]);
            }
        })
        .fail(function() {
            console.log("error");
        });
    }

    if (book_id) {
        getBookDetails(book_id);
    }

    $('form').on('submit', function(event) {
        event.preventDefault();
        let el = $(this);
        let formData = new FormData(el[0]);
        let url = "/api/v1/add_book";
        if (book_id) {
            url += `?book_id=${book_id}`;
        }
        $.ajax({
            url: url,
            type: 'POST',
            data: formData,
            dataType: "json",
            async: false,
            cache: false,
            contentType: false,
            processData: false,
        })
        .done(function(response) {
            alert(response.msg);
            if (response.status) {
                window.location = '/book_list';
            }
        })
        .fail(function() {
            console.log("error");
        });
    });
});