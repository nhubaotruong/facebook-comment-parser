$(() => {
    const csrftoken = Cookies.get('csrftoken');
    $.ajaxSetup({
        headers: {
            'X-CSRFToken': csrftoken
        }
    });

    $('#theForm').submit(event => {
        event.preventDefault();
        $(':reset').prop('disabled', true);
        $(':submit').prop('disabled', true);
        const postData = {
            fbContent: $('#fbContent').val() || ''
        }
        $.post('api/parse', postData, data => {
            $('#input').css("display", "none");
            $('#result').css("display", "initial");
            const displayData = `
                <thead>
                    <tr>
                        <th scope="col">STT</th>
                        <th scope="col">Account name</th>
                        <th scope="col">Profile link</th>
                        <th scope="col">Email</th>
                        <th scope="col">Mobile phone</th>
                        <th scope="col">Means</th>
                        <th scope="col">Property</th>
                        <th scope="col">Property details</th>
                        <th scope="col">Product</th>
                        <th scope="col">Answer (VN)</th>
                        <th scope="col">Answer (EN)</th>
                        <th scope="col">Opinion Content (VN)</th>
                        <th scope="col">Opinion Content (EN)</th>
                        <th scope="col">Received date</th>
                        <th scope="col">Replied date</th>
                    </tr>
                </thead>
                <tbody>
                    ${data.result.map((comment, index) => {
                return `
                            <tr>
                                <th scope="row">${index + 1}</th>
                                <td>${comment.name || ""}</td>
                                <td>${comment.profile_link || ""}</td>
                                <td></td>
                                <td></td>
                                <td></td>
                                <td></td>
                                <td></td>
                                <td></td>
                                <td>${comment.reply_link || ""}</td>
                                <td></td>
                                <td>${(comment.comment_text || "") + (comment.comment_img || "")}</td>
                                <td>${comment.comment_text_eng || ""}</td>
                                <td>${comment.comment_date || ""}</td>
                                <td></td>
                            </tr>
                        `
            })}
                </tbody>
            `
            $('#resultTable').html(displayData);
            $(':reset').prop('disabled', false);
            $(':submit').prop('disabled', false);
        });
    });

    $('#backBtn').click(() => {
        $('#result').css("display", "none");
        $('#input').css("display", "initial");
    });
});