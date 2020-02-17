var weights = [0.0];
var inputs = [-1,0.5]

var x;
var y;
var label;

var points = [];

var lr = 0.1;

class Point{
  constructor(){
    this.x = random(width);
    this.y = random(height);

    if(this.x>this.y){
      this.label = 1;
    }else{
     this.label = -1; 
    }
  }
}

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

function show(point){
  stroke(0);
  if(point.label == 1){
    fill(255);
  }else{
    fill(0);
  }
  ellipse(point.x,point.y,8,8);
}

function setup(){
  createCanvas(500, 500);
  for (var i = 0; i < 100; i++){
    let p = new Point();
    points.push(p);
  }
  Guess(inputs);
}

function draw(){
  background(255);
  points.forEach(point => {
    show(point);

    var inputs = [point.x,point.y]
    var target = points.label;
    train(inputs, target);
    
    var guess = Guess(inputs);
    if(guess == target){
      fill(0,255,0);
    } else{
      fill(255,0,0);
    }
    noStroke();
    ellipse(point.x,point.y,4,4);
  });
}

function train(inputs, target){
  var guess = Guess(inputs);
  var error = target - guess;
  
  for (var i =0; i < weights.length; i ++){
    weights[i] += error * inputs[i] * lr;
  }
}