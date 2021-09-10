$(document).ready(function($) {
    function generateBookList(){
        $.ajax({
            url: "/api/v1/book_list",
            dataType: "json"
        })
        .done(function(response) {
            if (response.status) {
                let book_lang_map = {
                    1: 'English',
                    2: 'हिन्दी'
                }
                console.log(response.data);
                let table_rows =  '';
                $.each(response.data, function(index, book) {
                    table_rows += `
                        <tr>
                            <td>${book[0]}</td>
                            <td>${book[1]}</td>
                            <td>${book[2]}</td>
                            <td>${book_lang_map[book[3]]}</td>
                            <td>${book[4]}</td>
                            <td>${book[5]}</td>
                            <td>${book[6]}</td>
                            <td>${book[7]}</td>
                            <td>${book[8]}</td>
                            <td>${book[9]}</td>
                            <td>${book[10]}</td>
                            <td data-book_id="${book[0]}">
                                <button class="btn btn-xs btn-primary edit_btn">Edit</button>&nbsp;
                                <button class="btn btn-xs btn-danger delete_btn">Delete</button>
                            </td>
                        </tr>
                    `;
                });
                let table_html = `
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>Book title</th>
                            <th>Book subtitle</th>
                            <th>Book lang</th>
                            <th>Author</th>
                            <th>Isbn</th>
                            <th>Edition</th>
                            <th>Orig price</th>
                            <th>Curr price</th>
                            <th>Book volume</th>
                            <th>Date created</th>
                            <th>Action</th>
                        <tr>
                    </thead>
                    <tbody>
                        ${table_rows}
                    </tbody>
                `
                $('#book_list').html(table_html);
            }
            else {
                alert(response.msg);
            }
        })
        .fail(function() {
            console.log("error");
        });
    }
    generateBookList();

    $(document).on('click', '.edit_btn', function(event) {
        let book_id = $(this).parent('td').data('book_id');
        location.href = `/?book_id=${book_id}`
    });

    $(document).on('click', '.delete_btn', function(event) {
        let book_id = $(this).parent('td').data('book_id');
        if (confirm()) {
            $.ajax({
                url: "/api/v1/manage_book?action=delete_book",
                type: 'POST',
                dataType: "json",
                data: {
                    'book_id': book_id
                }
            })
            .done(function(response) {
                alert(response.msg);
                if (response.status) {
                    generateBookList();
                }
            })
            .fail(function() {
                console.log("error");
            });
        }
    });
});