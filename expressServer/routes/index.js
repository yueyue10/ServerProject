var express = require("express");
var router = express.Router();
var path = require("path");
var pjson = require("../package.json");

/* GET home page. */
router.get("/", function (req, res, next) {
  let api_path = pjson.apidoc.url + "/apidoc/";
  res.render("index", {
    title: "Express Server",
    api_path: api_path,
    socketio_path: "/socketio",
    sockettest_path: "/sockettest",
    socketjade_path: "/socketjade",
  });
});

router.get("/socketio", function (req, res) {
  res.sendFile(
    path.join(path.resolve(__dirname, ".."), "public/socketio.html")
  );
});

router.get("/sockettest", function (req, res) {
  res.sendFile(path.join(path.resolve(__dirname, ".."), "public/socket.html"));
});

router.get("/socketjade", function (req, res, next) {
  res.render("socket", { title: "socket测试" });
});

module.exports = router;
