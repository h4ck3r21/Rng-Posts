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
    if (files[0] != "") {
        console.log(files)
        document.getElementById('imgContainer').classList.remove("inv");
        var fileFrame = document.getElementById("file");
        fileFrame.src = src;
        console.log(src);
        resizeImageLoop(fileFrame, src);
    };
};

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
    height = iframe.offsetHeight;
    width = iframe.offsetWidth;
    console.log("height, width = " + height + " " + width);
    image.style.maxHeight = height + "px";
    image.style.maxWidth = width + "px";

};

function move_image(n){
    image_num += n;
    console.log(image_num);
    filePreview();
};

document.getElementById('imgContainer').addEventListener("load", filePreview(0));
