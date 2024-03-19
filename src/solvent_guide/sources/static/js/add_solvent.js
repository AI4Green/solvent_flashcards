function getSolventInfo (casNumber) {
    fetch("/add_solvent", {
      headers: {
        "Content-Type": "application/json",
      },
      method: "POST",
      body: JSON.stringify({
        cas_number:casNumber

      }),
    })
    .then(function(response){
        return response.json()

    })
    .then(function(item){
    $("#example_flashcard").html(item.example_flashcard).show();
        })
}
function getFlashcardData() {
const elements = document.querySelectorAll("#CAS, #Family, #Solvent,#Safety, #Health, #Env, #FP, #BP, #Worst-H3xx, #Worst-H4xx, #Replacement-Issues, #Replacement-1");
var inputs ={};
elements.forEach(function(input) {
         inputs[input.id]=input.value
        // Get the value of the input element and push it to the inputValues array
     })
     return inputs
}

function saveFlashcard(){
var allData = getFlashcardData();
fetch("/save_flashcard", {
  headers: {
    "Content-Type": "application/json",
  },
  method: "POST",
  body: JSON.stringify(allData)
  })
  .then(function(response){
      var result = response.json()
      if (result == 'success'){
       $("#example_flashcard").html('Solvent flashcard added!').show();
      }
  })
}

function changeBorderColor(buttonElement){
    var justColor = getComputedStyle(buttonElement).getPropertyValue('background-color');
    document.getElementById('card').style.borderColor = justColor;

}

