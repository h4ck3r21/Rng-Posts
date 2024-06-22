var files = document.getElementById("var").innerHTML;
files = files.split(",");
console.log("files:" + files);
var image_num = 0;

function filePreview() {
    if (image_num >= files.length) {
        image_num = 0
    } else if (image_num < 0) {
        image_num = files.length - 1
    }
    console.log(image_num)
    src = files[image_num]
    if (files[image_num] != "") {
        console.log(files)
        document.getElementById('imgContainer').classList.remove("inv");
        var fileFrame = document.getElementById("file");
        fileFrame.src = src;
        console.log(src);
        resizeImageLoop(fileFrame, src);
        console.log(files.length);
        if (files.length >= 2) {
            var buttons = document.querySelectorAll('.img-selector');
            console.log(buttons);
            buttons.forEach(showItem);
        }
    };
};

function showItem(item, index) {
    console.log("showing buttons")
    item.classList.remove("inv");
}

function resizeImageLoop(iframe, src) {
    if (iframe.contentWindow.document.body == null) {
        setTimeout(() => { resizeImageLoop(iframe, src); }, 10);
        return
    }
    elements = iframe.contentWindow.document.body.getElementsByTagName("*")
    console.log(iframe)
    console.log(elements)
    console.log(src)
    if (src == "") {
        return
    }
    else if (elements.length == 0 || !(elements[0].src.includes(src) || elements[0].baseURI.includes(src))) {
        setTimeout(() => { resizeImageLoop(iframe, src); }, 10);
    } else {
        console.log(elements[0].src)
        if (elements[0].tagName == "IMG") {
            console.log("resizing image")
            resizeImage(iframe, elements[0])
        }
        else if (elements[0].tagName == "VIDEO") {
            elements[0].removeAttribute("autoplay")
            ratio = 594 / 420;
            iframe.style = "height:" + (ratio * iframe.offsetWidth) + "px";
            document.getElementById("imgContainer").style = "height:" + (ratio * iframe.offsetWidth) + "px";
        }
        else {
            ratio = 594 / 420;
            iframe.style = "height:" + (ratio * iframe.offsetWidth) + "px";
            document.getElementById("imgContainer").style = "height:" + (ratio * iframe.offsetWidth) + "px";
        }
        console.log(iframe.offsetWidth);
        console.log(iframe.offsetHeight);
    }
}

function resizeImage(iframe, image) {
    console.log(iframe + "\n" + image)
    width = iframe.offsetWidth;
    image.style.maxWidth = width + "px";
    image.style.borderRadius = "5px";
    iframe.style = "height:" + (image.height + 1) + "px";
    height = image.height + 1;
    console.log("height, width = " + height + " " + width);
    document.getElementById("imgContainer").style = "height:" + (image.height + 1) + "px";
    console.log(document.body.scrollHeight);
};

function move_image(n) {
    image_num += n;
    console.log(image_num);
    filePreview();
};

imageContainer = document.getElementById('imgContainer');
imageContainer.addEventListener("load", filePreview());
window.addEventListener("resize", function () {
    iframe = document.getElementById("file");
    src = iframe.src;
    resizeImageLoop(iframe, src);
})