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
    elements = iframe.contentWindow.document.body.getElementsByTagName("*")
    console.log(elements)
    console.log(src)
    if (elements.length == 0 || !(elements[0].src.includes(src) || elements[0].baseURI.includes(src)))  {
        setTimeout(() => {  resizeImageLoop(iframe, src); }, 1000);
    } else {
        console.log(elements[0].src)
        if (elements[0].tagName == "IMG") {
            console.log("resizing image")
            resizeImage(iframe, elements[0])
        }
    }
}

function resizeImage(iframe, image) {
    console.log(iframe + "\n" + image)
    height = iframe.offsetHeight;
    width = iframe.offsetWidth;
    console.log("height, width = " + height + " " + width);
    image.style.maxWidth = width + "px";
    image.style.borderRadius = "5px";
    iframe.style = "height:" + (image.height + 1) + "px";
    document.getElementById("imgContainer").style = "height:" + (image.height + 1) + "px";
    console.log(document.body.scrollHeight);
};

function move_image(n){
    image_num += n;
    console.log(image_num);
    filePreview();
};

imageContainer = document.getElementById('imgContainer');
imageContainer.addEventListener("load", filePreview(0));
window.addEventListener("resize", function () {
    iframe = document.getElementById("file");
    src = iframe.src;
    resizeImageLoop(iframe, src);
})
