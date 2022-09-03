var files = document.getElementById("var").innerHTML;
files = files.split(",");
console.log("files:" + files);
var image_num = 0;

function filePreview(n) {
    if (image_num >= files.length || image_num < 0) {
        image_num = 0
      }
    src = files[image_num]
    if (file) {
        document.getElementById('imgContainer').classList.remove("inv");
        var fileFrame = document.getElementById("file");
        fileFrame.addEventListener("readystatechange", resizeImage(fileFrame));
        fileFrame.src= src;
        console.log(src);
    };
};

function resizeImage(iframe) {
    height = iframe.offsetWidth;
    width = iframe.offsetHeight;
    console.log("height, width = " + height + " " + width);
    iDocument = iframe.contentWindow.document;
    console.log(iDocument);
    image = iDocument.getElementsByTagName("img")[0];
    height + "px";
    width + "px";

};

function move_image(n){
    image_num += n;
    console.log(image_num);
    filePreview(image_num);
};

document.getElementById('imgContainer').addEventListener("load", filePreview(0));
