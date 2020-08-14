const express = require("express");
const router = express.Router();
const path = require("path");
const fs = require("fs");

/**
 * @apiDescription 获取grade的诗词列表
 * @api {get} /poetry/grade/poetryList 获取grade的诗词列表
 * @apiName /grade/poetryList
 * @apiGroup poetry
 * @apiSuccess {json} result
 * @apiSampleRequest http://localhost:3000/poetry/grade/poetryList
 * @apiVersion 0.0.0
 */
router.get("/grade/poetryList", function (req, res, next) {
    let file = path.join(__dirname, "../public/data/grade.json");
    let fileStr = fs.readFileSync(file, "utf-8");
    let result = JSON.parse(fileStr);
    res.json(result);
});

/**
 * @apiDescription 获取诗词排行榜内容
 * @api {get} /poetry/rank/poetryList 获取诗词排行榜内容
 * @apiName /rank/poetryList
 * @apiGroup poetry
 * @apiSuccess {json} result
 * @apiSampleRequest http://localhost:3000/poetry/rank/poetryList
 * @apiVersion 0.0.0
 */
router.get("/rank/poetryList", function (req, res, next) {
    let file = path.join(__dirname, "../public/data/rank.json");
    let fileStr = fs.readFileSync(file, "utf-8");
    let result = JSON.parse(fileStr);
    res.json(result);
});

/**
 * @apiDescription 获取诗词分类内容
 * @api {get} /poetry/mark/typeList 获取诗词分类内容
 * @apiName /mark/typeList
 * @apiGroup poetry
 * @apiSuccess {json} result
 * @apiSampleRequest http://localhost:3000/poetry/mark/typeList
 * @apiVersion 0.0.0
 */
router.get("/mark/typeList", function (req, res, next) {
    let file = path.join(__dirname, "../public/data/mark_type.json");
    let fileStr = fs.readFileSync(file, "utf-8");
    let result = JSON.parse(fileStr);
    res.json(result);
});

/**
 * @apiDescription 获取诗词分类-诗词内容
 * @api {get} /poetry/mark/poetryList 获取诗词分类-诗词内容
 * @apiName /mark/poetryList
 * @apiGroup poetry
 * @apiSuccess {json} result
 * @apiSampleRequest http://localhost:3000/poetry/mark/poetryList
 * @apiVersion 0.0.0
 */
router.get("/mark/poetryList", function (req, res, next) {
    let file = path.join(__dirname, "../public/data/mark.json");
    let fileStr = fs.readFileSync(file, "utf-8");
    let result = JSON.parse(fileStr);
    res.json(result);
});

/**
 * @apiDescription 获取作者合称内容
 * @api {get} /poetry/hecheng/infos 获取作者合称内容
 * @apiName /hecheng/infos
 * @apiGroup poetry
 * @apiSuccess {json} result
 * @apiSampleRequest http://localhost:3000/poetry/hecheng/infos
 * @apiVersion 0.0.0
 */
router.get("/hecheng/infos", function (req, res, next) {
    let file = path.join(__dirname, "../public/data/hecheng.json");
    let fileStr = fs.readFileSync(file, "utf-8");
    let result = JSON.parse(fileStr);
    res.json(result);
});

/**
 * @apiDescription 获取史书典籍数据
 * @api {get} /poetry/oldbook/infos 获取史书典籍数据
 * @apiName /oldbook/infos
 * @apiGroup poetry
 * @apiSuccess {json} result
 * @apiSampleRequest http://localhost:3000/poetry/oldbook/infos
 * @apiVersion 0.0.0
 */
router.get("/oldbook/infos", function (req, res, next) {
    let file = path.join(__dirname, "../public/data/oldbook.json");
    let fileStr = fs.readFileSync(file, "utf-8");
    let result = JSON.parse(fileStr);
    res.json(result);
});

/**
 * @apiDescription 获取史书典籍-章节数据
 * @api {get} /poetry/oldbook/chapters 获取史书典籍-章节数据
 * @apiName /oldbook/chapters
 * @apiGroup poetry
 * @apiSuccess {json} result
 * @apiSampleRequest http://localhost:3000/poetry/oldbook/chapters
 * @apiVersion 0.0.0
 */
router.get("/oldbook/chapters", function (req, res, next) {
    let file = path.join(__dirname, "../public/data/oldbk_chapter.json");
    let fileStr = fs.readFileSync(file, "utf-8");
    let result = JSON.parse(fileStr);
    res.json(result);
});

/**
 * @apiDescription 获取史书典籍-内容数据
 * @api {get} /poetry/oldbook/content 获取史书典籍-内容数据
 * @apiName /oldbook/content
 * @apiGroup poetry
 * @apiSuccess {json} result
 * @apiSampleRequest http://localhost:3000/poetry/oldbook/content
 * @apiVersion 0.0.0
 */
router.get("/oldbook/content", function (req, res, next) {
    let file = path.join(__dirname, "../public/data/oldbk_content.json");
    let fileStr = fs.readFileSync(file, "utf-8");
    let result = JSON.parse(fileStr);
    res.json(result);
});
module.exports = router;
