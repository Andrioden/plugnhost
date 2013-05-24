/** SECTION X: Get port input **/
/*************************************************************/
var PORT = process.argv[2];

/** SECTION 1: Create the node, express and socket.io setup **/
/*************************************************************/

var express = require('express')
, http = require('http');
var app = express();
app.use(express.bodyParser());
var server = http.createServer(app);
//var io = require('socket.io').listen(server);
//io.set('log level', 1);

console.log("Starting Node.js Worker Server on port "+PORT);
server.listen(PORT);


/** SECTION 3: Http request handling **/
/*************************************************************/

// Manual urls
app.get('/', function (req, res) {
	console.log("Request at port "+PORT);
	res.send("Hello, welcome to port "+PORT);
	//res.sendfile(__dirname + '/public/index.html');
});

// Setting static folders, all files (recursively) in these will be public
app.use(express.static(__dirname + '/public'));


/** SECTION X: Finaly **/
/*************************************************************/
console.log("READY"); // Signals the python starter process that it is ready to accept connections