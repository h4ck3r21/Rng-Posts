

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
    datatype = reader.result.split(";")[0]
    const embed = document.getElementById("preview")
    embed.data = reader.result
    embed.width = "100%"


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




