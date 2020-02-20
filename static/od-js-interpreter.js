window.openDecision = (function(){
"use strict";
// The node of the tree the user is currently seeing
let currentNode,
// The decision tree that is being rendered
tree,
// Contains the html to display the tree name
preString,
// Used to log the nodes shown and answers given by the user, used for history
log,
// The div-container in which the tree is rendered in (where the question, buttons etc. is shown)
selectedDiv,

 expose = {};

expose.init = function (path, divId) {
  tree = path;
  selectedDiv = divId;
  displayTree();
};

// Listener for hashchange in the URL if the user clicks the browser's back-button
// The hash tells us the node name, that is currently displayed
window.onhashchange = function() {
  if ((currentNode != location.hash.replace('#','')) && (location.hash.length > 0)) {
        if (log.nodes.length > 0) {
          //Go back one step
          currentNode = location.hash.replace('#','');
          log.nodes.pop();
          log.answers.pop();
        } else {
          // Else restart
          currentNode = tree.header.start_node;
          log = {'nodes': [], 'answers': []};
        }
        displayNode();
    }
};

function displayTree  () {
  currentNode = tree.header.start_node;
  preString = '<h3>' + tree.header.tree_name + '</h3><br>';
  log = {'nodes': [], 'answers': []}
  displayNode()
};

function displayNode () {
  // Check for vars that need to be replaced
  console.log(log);
  location.hash = currentNode;
  let string = preString + tree[currentNode].question + '<br>';

  if (tree[currentNode].input_type == 'button') {
    for (let i = 0; i < tree[currentNode].answers.length; i++) {
        string += '<button type="button" class="btn btn-primary ml-2" id="answer-button" value=' + i + '>' + tree[currentNode].answers[i] + '</button>'
      }
    }
  else if (tree[currentNode].input_type == 'list') {
    string += '<select id="list-select">'
    for (let i = 0; i < tree[currentNode].answers.length; i++) {
      string += '<option value=' + i + '>' + tree[currentNode].answers[i] + '</option>'
      }
      string += '</select><br><button type="button" class="btn btn-primary ml-2 mt-3" id="submit-list-button">Submit</button>'
    }
  else if (tree[currentNode].input_type == 'number') {
  string += '<input type="number" id="number-input">'
  string += '</select><br><button type="button" class="btn btn-primary ml-2 mt-3" id="submit-number-button">Submit</button>'
}
else if (tree[currentNode].input_type == 'date') {
  string += '<input type="number" id="date-input">'
  string += '</select><br><button type="button" class="btn btn-primary ml-2 mt-3" id="submit-number-button">Submit</button>'
};

  string += '<br><button type="button" class="btn btn-primary ml-2 mt-3" id="restart-button">Restart</button><button type="button" class="btn btn-primary ml-2 mt-3" id="back-button">Back</button>'
  document.getElementById(selectedDiv).innerHTML = string;
  document.addEventListener( "click", listener );
};


function listener (event) {
  // Support IE6-8
 let target = event.target || event.srcElement;

  if (target.id == 'answer-button') {
    let answerId = parseInt(target.value);
    let answer = tree[currentNode].answers[answerId];
    checkAnswer(answer, 'button');

  } else if (target.id == 'submit-list-button') {
    let answerId = parseInt(document.getElementById("list-select").value);
    let answer = tree[currentNode].answers[answerId];
    checkAnswer(answer, 'list');

  } else if (target.id == 'submit-number-button') {
    let answer = document.getElementById("number-input").value;
    checkAnswer(answer, 'number');

  } else if (target.id == 'submit-date-button') {
    let answer = document.getElementById("date-input").value;
    // Load datepicker
    checkAnswer(answer, 'date');

  } else if (target.id == 'restart-button') {
    currentNode = tree.header.start_node;
    displayNode();
    log = {'nodes': [], 'answers': []};

  } else if (target.id == 'back-button') {
      if (log.nodes.length > 0) {
        currentNode = log.nodes.pop();
        log.answers.pop();
      } else {
        currentNode = tree.header.start_node;
        log = {'nodes': [], 'answers': []};
      }
    displayNode();
  }
};

function checkAnswer (answer, input_type) {
  let rule = jsonLogic.apply(tree[currentNode].rules, {"answer":answer});
  log['nodes'].push(currentNode);
  log['answers'].push(answer);
  currentNode = tree[currentNode].results[rule].destination;
  displayNode();
};

// Initiate with path(s) for trees and div to display everything in, CSS classes later

// Show question (display as safe html, look for variables) and display answers
// list: take answers from a list in display selectfield with listener attached
// date/number: show numberfield or datefield with datepicker attached, attach listener
// end_node: show restart or save-button

// Save/download progress function
// Check header data
// Validate user input and give errors
//Todo: JS translation


 return expose;
}());
