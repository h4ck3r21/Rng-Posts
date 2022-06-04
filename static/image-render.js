
window.addEventListener('load', function(){
    document.getElementById('File')/addEventListener('change', function(e){
      addFile()  
      filePreview(0);
    });
});


function filePreview(image_num){
  const preview = document.getElementById('imgPreview');
  const files = document.querySelector('#File').files
  const file = files[image_num];
  const reader = new FileReader();
  console.log(files)

  reader.addEventListener("load", function () {
    // result is a base64 string
    preview.src = reader.result;
  }, false);

  if (file) {
    preview.classList.remove("inv");
    reader.readAsDataURL(file);
  }
}


