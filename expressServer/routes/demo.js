var express = require('express');
var router = express.Router();
var path = require('path');
var fs = require("fs");
var html = require('./html.js')
const db = require("../db"); //引入数据库封装模块

/**
 * @apiDescription 下载文件
 * @api {get} /demo/download 下载文件
 * @apiName download
 * @apiGroup demo
 * @apiSampleRequest http://81.68.145.189:3000/demo/download
 * @apiVersion 0.0.0
 */
router.get('/download', function (req, res, next) {
    let file = path.join(__dirname, '../public/data/1-202005181147.log');
    var f = fs.createReadStream(file);
    res.writeHead(200, {
        'Content-Type': 'application/force-download',
        'Content-Disposition': 'attachment; filename=202005181147.log'
    });
    f.pipe(res);
});

/**
 * @apiDescription 设置本地url
 * @api {get} /demo/setUrl 设置本地url
 * @apiName setUrl
 * @apiGroup demo
 * @apiParam {string} url 路径
 * @apiSuccess {json} result
 * @apiSuccessExample {json} Success-Response:
 *  {
 *    "url" : ""
 *  }
 * @apiSampleRequest http://81.68.145.189:3000/demo/setUrl
 * @apiVersion 0.0.0
 */
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

/**
 * @apiDescription 获取本地保存的url
 * @api {get} /demo/getUrl 获取本地保存的url
 * @apiName getUrl
 * @apiGroup demo
 * @apiSuccess {json} result
 * @apiSuccessExample {json} Success-Response:
 *  {
 *    "url" : ""
 *  }
 * @apiSampleRequest http://81.68.145.189:3000/demo/getUrl
 * @apiVersion 0.0.0
 */
router.get('/getUrl*', function (req, res, next) {
    let file = path.join(__dirname, '../public/data/url.json');
    let fileStr = fs.readFileSync(file, 'utf-8')
    let result = JSON.parse(fileStr);
    res.writeHeader(200, {"Content-Type": "text/html;charset:utf-8"});
    res.write('<head><meta charset="utf-8"/></head>');
    console.log("getUrl", result);
    res.end(fileStr);
});

/**
 * @apiDescription 获取mysql数据
 * @api {get} /demo/mysql/data 获取mysql数据
 * @apiName /mysql/data
 * @apiGroup demo
 * @apiSuccess {json} result
 * @apiSuccessExample {json} Success-Response:
 *  {
 *    "url" : ""
 *  }
 * @apiSampleRequest http://81.68.145.189:3000/demo/mysql/data
 * @apiVersion 0.0.0
 */
router.get('/mysql/data', function (req, res, next) {
    //查询users表
    db.query("SELECT * FROM account", [], function (results, fields) {
        console.log(results);
        res.json(results);
    })
});


/**
 * @apiDescription 获取微信公众号网页内容
 * @api {get} /demo/getWeiXinHtml 获取微信公众号网页内容
 * @apiName getWeiXinHtml
 * @apiGroup demo
 * @apiParam {string} url 路径
 * @apiSuccess {json} result
 * @apiSuccessExample {json} Success-Response:
 *  {
 *    "url" : ""
 *  }
 * @apiSampleRequest http://81.68.145.189:3000/demo/getWeiXinHtml
 * @apiVersion 0.0.0
 */
router.get('/getWeiXinHtml*', function (req, res, next) {
    let result = {msg: '参数错误'}
    if (req.query.url) {
        console.log(req.query.url)
        return html.getWeiXinHtml(res, req.query.url)
    } else {
        return res.json(result)
    }
})

module.exports = router;
