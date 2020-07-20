var express = require('express');
var router = express.Router();
var path = require('path');
var fs = require("fs");

/* 下载文件 */
router.get('/download', function (req, res, next) {
    let file = path.join(__dirname, '../public/data/1-202005181147.log');
    var f = fs.createReadStream(file);
    res.writeHead(200, {
        'Content-Type': 'application/force-download',
        'Content-Disposition': 'attachment; filename=202005181147.log'
    });
    f.pipe(res);
});

/* 写入文件 */
router.get('/setUrl*', function (req, res, next) {
    console.log(req.method, req.query);
    let result = {msg: '参数错误'}
    if (req.query.url) {
        let file = path.join(__dirname, '../public/data/url.json');
        let fileStr = fs.readFileSync(file, 'utf-8')
        result = JSON.parse(fileStr);
        result.url = req.query.url
        fs.writeFile(file, JSON.stringify(result), {'flag': 'w'}, function (err) {
            if (err) result = err;
        })
    }
    res.writeHeader(200, {"Content-Type": "text/html;charset:utf-8"});
    res.write('<head><meta charset="utf-8"/></head>');
    console.log("getUrl", result);
    res.end(JSON.stringify(result));
});

/* 读取文件 */
router.get('/getUrl*', function (req, res, next) {
    let file = path.join(__dirname, '../public/data/url.json');
    let fileStr = fs.readFileSync(file, 'utf-8')
    let result = JSON.parse(fileStr);
    res.writeHeader(200, {"Content-Type": "text/html;charset:utf-8"});
    res.write('<head><meta charset="utf-8"/></head>');
    console.log("getUrl", result);
    res.end(fileStr);
});

module.exports = router;
