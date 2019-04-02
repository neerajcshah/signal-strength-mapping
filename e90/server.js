var path = require('path');
var express = require('express');
var app = express();
var string;

// Log the requests
// app.use(logger('dev'));

app.use(express.static(path.join(__dirname, 'public')));
const spawn = require("child_process").spawn;
const pythonProcess = spawn('python',["./image.py"]);
pythonProcess.stdout.on('data', function(data) {
  console.log(data)
});


app.listen(8000);


// Serve static files
/*
app.get('/', function(req, res){
    res.sendFile(__dirname + '/index.html');
});
*/

// app.use(express.static(path.join(__dirname, './'))); 

// Route for everything else.
/*
app.get('*', function(req, res){
  res.send('Hello World');
});
*/


