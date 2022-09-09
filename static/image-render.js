

window.addEventListener('load', function(){
    document.getElementById('File')/addEventListener('change', function(e){
      const files = document.querySelector('#file-input').files
      addFile()  
      image_num = files.length
      filePreview();
    });
});


function filePreview(){
  const files = document.querySelector('#file-input').files
  const imgPreview = document.getElementById('imgPreview');
  const vidPreview = document.getElementById('vidPreview')
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
    if (reader.result.startsWith("data:video")) {
        vidPreview.src = reader.result
        vidPreview.classList.remove("inv")
        imgPreview.classList.add("inv")
        vidPreview.maxWidth = 200px
    } else if (reader.result.startsWith("data:image")) {
        imgPreview.src = reader.result
        imgPreview.classList.remove("inv")
        vidPreview.classList.add("inv")
        imgPreview.maxWidth = 200px
    } else {
        console.log("unrecognisable file type")
    }

  }, false);

  if (file) {
    document.getElementById('imgPreviewContainer').classList.remove("inv");
    reader.readAsDataURL(file);
  }
}

var image_num = 0

function move_image(n){
  image_num += n
  console.log(image_num)
  filePreview()
}




