var weights = [0.0];
var inputs = [-1,0.5]

function Sign(sum){
  if(sum >= 0){
    return 1;
  } else{
    return -1;
  }
}

function Perceptron(){
  for (var i = 0; i < weights.length; i++){
    weights[i] = random(-1,1);
  }
}

function Guess(inputs){
  var sum = 0;
  for (var i = 0; i < weights.length; i++){
    sum += inputs[i]*weights[i];
  }
  var output = Sign(sum);
  console.log(sum + ' => ' + output);
}

function setup(){
    p = new Perceptron();
    Guess(inputs);
}