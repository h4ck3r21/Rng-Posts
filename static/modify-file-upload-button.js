document.querySelectorAll('.file-button').forEach(function (button) {
  const input =  document.querySelector('#File');
  button.addEventListener('click', function(){
    input.click();
  });
  console.log("added button")
});

function addFile (){
  const files = document.querySelector('#file-input').files;
  const file = document.querySelector('#File').files[0];
  let list = new DataTransfer();
  for (let i = 0; i < files.length; i++) {
    list.items.add(files[i])
  }
  list.items.add(file)
  let filelist = list.files
  document.querySelector('#file-input').files = filelist
  console.log(document.querySelector('#file-input').files)
}