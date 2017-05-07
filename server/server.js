var express = require('express');
var concat = require('concat-stream');
var Stream = require('stream').Transform;
var fs = require('fs')
var app = express();
var port = process.env.PORT || 3000;

app.listen(port);

app.use (function(req, res, next) {
    req.rawBody = new Stream();
    req.on('data', function(chunk) {
      req.rawBody.push(chunk);
      next();
    });
});

app.post('/havefun', function (req, res, next) {
  const uuid = require('node-uuid');
  const reponse = {
    uuid: uuid.v4(),
  };
  var wstream = fs.createWriteStream(`keys/${reponse.uuid}.secret`);
  wstream.write(req.rawBody.read());
  wstream.end();
  return res.json(reponse);
});
