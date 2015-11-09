TOPLEVEL = ["Will they like it?", "Will they be good at it?", "Can we afford them?"] 

WILLTHEYBEGOODAIT = ["Soft Skills", "Technical Skills", "Experience", "Education"];

TECHNICALSKILLS = ["Programming", "Databases", "Analytics/Statistics"]

EXPERIENCE = ["Industry specificity", "Years of experience", "Job title relevance"]

EDUCATION = ["School/College Name", "Strong Grades", "Course Relevance", "Qualification Level (BSc/MSc/Phd)"]

WILLTHEYLIKEIT = ["Cultural fit", "Career alignment/development", "Personal development goals"]

CANWEAFFORDTHEM = ["Monetary Price", "Enough Responsibility"]

ENOUGHRESPONSIBILITY = [ "Seniority" ,"Reportees"]

QUESTIONS = [TOPLEVEL, WILLTHEYLIKEIT, WILLTHEYBEGOODAIT, CANWEAFFORDTHEM,
             TECHNICALSKILLS, EXPERIENCE, EDUCATION, ENOUGHRESPONSIBILITY]




FORMID = "1I3gZU11uJir5m-d0XVsM8rcRKUx5E2Il6MtxH5C_fbw"

PRELABEL = "Strongly prefer "


/** This function returns all possible pairs from a given array of strings **/
/** Inverts some pairs. Returns a list of objects                          **/
function getAllPairs(skill_array) {
  var pair_array = [];
  for (var i=0;i<skill_array.length;i++){
    for (var j=0;j<skill_array.length;j++){
      if(i > j){
        if(j%2){
          pair_array.push({"label":skill_array[i] + " or " +skill_array[j], "param1":skill_array[i], "param2":skill_array[j]});
        }
        else {
          pair_array.push({"label":skill_array[j] + " or " +skill_array[i], "param1":skill_array[j], "param2":skill_array[i]});
        }
      }
    }
  }
  return pair_array;
}

/** Tests getAllPairs above. Logging the output labels **/
function testGetAllPairs(){
  var values = getAllPairs(TOPLEVEL);
  for each(value in values){
    Logger.log(value.label);
  }
}

/** Adds a given question set to the form **/
function addQuestionSet(level_string_array, form_object){
  var questions = getAllPairs(level_string_array);
  for each(var question in questions){
    var item = form_object.addScaleItem();
    item.setTitle(question["label"]).setBounds(1, 7).setLabels(PRELABEL+question["param1"], PRELABEL+question["param2"]);
  }
}

/** Generates our form **/
function main(){
  var form = FormApp.openById(FORMID);
  for each(question in QUESTIONS){
    Logger.log(question)
    addQuestionSet(question, form)
  }
}

/** Clears the attached form **/
function clearForm(){
  var form = FormApp.openById(FORMID);
  var items = form.getItems().length;
  Logger.log(form.getItems())
  for(i=0;i<form.getItems().length;i++){
    Logger.log(form.deleteItem(0))
    }
  }
