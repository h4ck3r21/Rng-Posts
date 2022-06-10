

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
  const preview = document.getElementById('imgPreview');
  if (image_num >= files.length) {
    image_num = 0
  }
  const file = files[image_num];
  const reader = new FileReader();
  console.log(files)

  reader.addEventListener("load", function () {
    // result is a base64 string
    preview.src = reader.result;
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
  filePreview(image_num)
}




