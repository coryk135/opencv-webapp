var express = require('express');
var router = express.Router();
var zerorpc = require("zerorpc");

var client = new zerorpc.Client();
client.connect("tcp://127.0.0.1:4242");

/* POST image. */
router.post('/', function(req, res, next) {
  console.log("Image size: " + req.files.fileToUpload.size + " Bytes");
  if(req.files.fileToUpload.size > 2.5 * 1000 * 1000)
    return res.sendStatus(413);
    
  console.log('about to invoke hello');
  client.invoke("hello", req.files.fileToUpload.buffer, req.files.fileToUpload.name, function(error, data, more) {
    if(error) console.log(error.message);
    if(more)  console.log("more: " + more);
//    console.log(data);
    res.send(data);
  });
});

module.exports = router;
