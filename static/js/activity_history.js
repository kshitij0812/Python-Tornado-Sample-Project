$(document).ready(function($) {
    $.ajax({
        url: "/api/v1/manage_book?action=get_activity_history",
        dataType: "json"
    })
    .done(function(response) {
        if (response.status) {
            let book_activity_map = {
                1: 'Created',
                2: 'Edited'
            }
            console.log(response.data);
            let table_rows =  '';
            $.each(response.data, function(index, book) {
                table_rows += `
                    <tr>
                        <td>${book[0]}</td>
                        <td>${book[1]}</td>
                        <td>${book[2]}</td>
                        <td>${book_activity_map[book[3]]}</td>
                        <td>${book[4]}</td>
                    </tr>
                `;
            });
            let table_html = `
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Book title</th>
                        <th>Book subtitle</th>
                        <th>Activity Type</th>
                        <th>Date created</th>
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
});