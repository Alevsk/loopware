var express = require('express');
var concat = require('concat-stream');
var Stream = require('stream').Transform;
var fs = require('fs');
var app = express();
var port = process.env.PORT || 3000;
var hbs = require('express-handlebars');
var path = require('path');
var uuid = require('node-uuid')

app.listen(port);

app.engine('hbs', hbs({
  extname: 'hbs',
  defaultLayout: 'main',
  layoutsDir: __dirname + '/views/layouts',
}));

app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'hbs');

app.get('/', function (req, res, next) {

  let key = req.query.id || null;
  const pattern = /^[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i;

  if (key) {
    if (pattern.test(key) && fs.existsSync(`keys/${key}.secret`)) {
      console.log('secret exists');
    } else {
      key = null;
    }
  }
  res.render('index', {
    title: 'loopware',
    key: key,
  });
});

app.use (function(req, res, next) {
    req.rawBody = new Stream();
    req.on('data', function(chunk) {
      req.rawBody.push(chunk);
      next();
    });
});

app.post('/havefun', function (req, res, next) {
  const reponse = {
    uuid: uuid.v4(),
  };
  var wstream = fs.createWriteStream(`keys/${reponse.uuid}.secret`);
  wstream.write(req.rawBody.read());
  wstream.end();
  return res.json(reponse);
});
