var files = document.getElementById("var").innerHTML;
files = files.slice(1, -1)
files = files.split(",")
console.log("files:" + files)
var image_num = 0

function filePreview(n) {
    if (image_num >= files.length || image_num < 0) {
        image_num = 0
      }
    src = files[image_num]
    if (file) {
        document.getElementById('imgContainer').classList.remove("inv");
        var fileFrame = document.getElementById("file");
        fileFrame.src=src;
        console.log(src)
    };
};

function move_image(n){
    image_num += n;
    console.log(image_num);
    filePreview(image_num);
  };