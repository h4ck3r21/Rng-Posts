

window.addEventListener('load', function(){
    console.log("load")
    document.getElementById('File').addEventListener('change', function(e){
        console.log("change")
        const files = document.querySelector('#file-input').files
        addFile()
        image_num = files.length
        filePreview();
    });
});


function filePreview(){
  const files = document.querySelector('#file-input').files
  if (image_num >= files.length) {
    image_num = 0
  } else if (image_num < 0) {
    image_num = files.length
  }
  const file = files[image_num];
  const reader = new FileReader();
  console.log(files)

  reader.addEventListener("load", function () {
    // result is a base64 string
    const preview = document.getElementById('PreviewContainer');
    datatype = reader.result.split(";")[0].split(":")[1];
    src = reader.result;
    preview.innerHTML = '';

    if (datatype.startsWith("image")) {
        element = document.createElement("img");
    } else if (datatype.startsWith("video")) {
        element = document.createElement("video");
    } else {
        element = document.createElement("embed");
        element.type = datatype;


    };
    element.style.maxWidth = "450px";
    element.src = src;
    preview.appendChild(element);

    if (files.length > 1) {
        left = document.createElement("button");
        left.classList.add("btn");
        left.classList.add("left");
        left.onclick = function () {move_image(-1);};
        left.type = "button"
        left.innerHTML = "&#10094;";
        preview.appendChild(left);

        right = document.createElement("button");
        right.classList.add("btn");
        right.classList.add("right");
        right.onclick = function () {move_image(+1);};
        right.type = "button"
        right.innerHTML = "&#10095;";
        preview.appendChild(right);
    }



  }, false);

  if (file) {
    document.getElementById('PreviewContainer').classList.remove("inv");
    reader.readAsDataURL(file);
  }
}

var image_num = 0

function move_image(n){
  image_num += n
  console.log(image_num)
  filePreview()
}



