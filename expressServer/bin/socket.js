var app = require("../app");
// 写法一1
var server = require("http").createServer(app);
// 写法二1
// var server = require("http").Server(app);

var socketIO = require("socket.io")(server);

socketIO.on("connection", function (socket) {
  console.log("===========a user connected==============");

  socket.on("disconnect", function () {
    console.log("===========user disconnected===========");
  });

  socket.on("chat message", function (msg) {
    console.log("===========message: " + msg + " ===========");

    socketIO.emit("chat message", msg);
  });
});

app.set("port", process.env.PORT || 3000);

// 写法一2
server.listen(app.get("port"));
// 写法二2
// var service = server.listen(app.get("port"), function () {
//   console.log("start at port:" + service.address().port);
// });

module.exports = server;
