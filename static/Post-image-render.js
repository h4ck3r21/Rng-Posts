var files = document.getElementById("var").innerHTML;
files = files.slice(1, -1)
files = files.split(", ")
console.log("files:" + files)
var image_num = 0

function filePreview() {
    if (image_num >= files.length || image_num < 0) {
        image_num = 0
      }
    file = files[image_num]
    if (file) {
        document.getElementById('imgContainer').classList.remove("inv");
        var fileImage = document.getElementById("img");
        var src = `` + file.slice(2, -1);
        fileImage.src=src;
        console.log(src)
    };
};

function move_image(n){
    image_num += n;
    console.log(image_num);
    filePreview(image_num);
  };