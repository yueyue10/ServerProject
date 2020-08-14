var express = require('express');
var router = express.Router();
var pjson = require('../package.json');

/* GET home page. */
router.get('/', function (req, res, next) {
    let api_path = pjson.apidoc.url + '/apidoc/'
    res.render('index', {title: 'Express Server', api_path: api_path});
});

module.exports = router;
