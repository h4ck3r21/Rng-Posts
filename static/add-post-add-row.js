function addRow(post) {

    console.log(post)

    const iframe = document.createElement('iframe');

    iframe.className = 'post';

    iframe.src = "/post/" + post;

    iframe.addEventListener('load', function () {
        this.style.height = (iframe.contentWindow.document.body.scrollHeight + 16) + "px";
        iframe.contentWindow.addEventListener('resize', function () {
            iframe.style.height = (iframe.contentWindow.document.body.scrollHeight + 16) + "px"
            console.log(iframe.contentWindow.document.body.scrollHeight);
        });
        let iframeDoc = iframe.contentDocument || iframe.contentWindow.document;
        if (typeof iframeDoc.addEventListener != "undefined") {
            iframeDoc.addEventListener("click", iframeClickHandler, false);
        } else if (typeof iframeDoc.attachEvent != "undefined") {
            iframeDoc.attachEvent("onclick", iframeClickHandler);
        }
        const embeds = iframeDoc.getElementsByTagName("iframe");
        console.log(embeds);
        for (i = 0; i < embeds.length; i++) {
            let embedDoc = embeds[i].contentDocument || embeds[i].contentWindow.document;
            if (typeof embedDoc.addEventListener != "undefined") {
                embedDoc.addEventListener("click", iframeClickHandler, false);
            } else if (typeof embedDoc.attachEvent != "undefined") {
                embedDoc.attachEvent("onclick", iframeClickHandler);
            }
            console.log(embeds[i].src)
        }

        function iframeClickHandler() {
            console.log("click");
            if (iframe.classList.contains('selected')) {
                iframe.classList.remove('selected');
            }
            else {
                selected_posts = document.getElementsByClassName('selected');
                Array.prototype.forEach.call(selected_posts, function (post) { post.classList.remove('selected') });
                document.getElementById('post').value = post;
                console.log(document.getElementById('post').value);
                iframe.classList.add('selected');
            }
        }
        // iframe.contentWindow.document.addEventListener("click", iframeClick);
    });


    window.addEventListener('resize', function () {
        iframe.style.height = (iframe.contentWindow.document.body.scrollHeight + 16) + "px"
        console.log(iframe.contentWindow.document.body.scrollHeight);
    });



    document.getElementById('posts').appendChild(iframe);
}