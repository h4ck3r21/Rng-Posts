window.addEventListener('load', function(){
    document.getElementById('File')/addEventListener('change', function(e){
        filePreview();
    });
});

function filePreview(){
  const preview = document.getElementById('imgPreview');
  const file = document.querySelector('#File').files[0];
  const reader = new FileReader();

  reader.addEventListener("load", function () {
    // result is a base64 string
    preview.src = reader.result;
  }, false);

  if (file) {
    reader.readAsDataURL(file);
  }
}

function getContent(){
        document.getElementById("body").value = document.getElementById("body-input").innerHTML;
        console.log(document.getElementById("body").value)
    }

var slideIndex = 1;
showDivs(slideIndex);

function plusDivs(n) {
  showDivs(slideIndex += n);
}

function showDivs(n) {
  var i;
  var x = document.getElementsByClassName("mySlides");
  if (n > x.length) {slideIndex = 1}
  if (n < 1) {slideIndex = x.length} ;
  for (i = 0; i < x.length; i++) {
    x[i].style.display = "none";
  }
  x[slideIndex-1].style.display = "block";
}

