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

function UpdateSHEscore(){
    const elements = document.querySelectorAll('#BP, #FP,#IT,#Hazard_codes');
    const checkBoxes = document.querySelectorAll('#resistivity,#reach,#peroxability')
   // const button = document.querySelectorAll('#saftey_score, #health_score, #env_score')
    var inputs ={};
    elements.forEach(function(input) {
         inputs[input.id]=input.value
        // Get the value of the input element and push it to the inputValues array
     })
    checkBoxes.forEach(function(input){
        inputs[input.id]=input.checked;
        })
    console.log(inputs)
    fetch("/CHEM21_calculator", {
      headers: {
        "Content-Type": "application/json",
      },
      method: "POST",
      body: JSON.stringify(inputs),
    })
    .then(function(response){
        return response.json()

    })
    .then(function(item){
    var safety_score = document.getElementById("safety_score")
        safety_score.value = item.safety_score
        safety_score.style.backgroundColor = getColors(item.safety_score);
    var health_score = document.getElementById("health_score")
        health_score.value=item.health_score
        health_score.style.backgroundColor = getColors(item.health_score);
    var environment_score = document.getElementById("env_score")
        environment_score.value = item.environment_score
        environment_score.style.backgroundColor = getColors(item.environment_score);
    var CHEM21_score = document.getElementById("CHEM21_score")
    var output = getOverallColor(item.CHEM21_score)
       CHEM21_score.value= output.phrase
       CHEM21_score.style.backgroundColor = output.color


    })


}

function getColors(score){
    if (score > 6){
    var color = 'red';}
    else if (3 <score && score<7 ){
    var color = 'yellow';}
    else if (score<=3){
    var color = 'green'}
    console.log(score, color)
    return color


}

function getOverallColor(score){
    if (score == 1){
    var color  = 'green';
    var phrase = 'Recommended';}
    else if (score == 2){
    var color  = 'yellow';
    var phrase = 'Problematic';}
    else if (score == 3){
    var color  = 'red';
    var phrase = 'Hazardous';}
    return {'color':color, 'phrase':phrase}


}