module.exports = function (server) {
    var socketIO = require("socket.io")(server);

    socketIO.on("connection", (socket) => {
        console.log("===========a user connected==============");

        socket.on("disconnect", function () {
            console.log("===========user disconnected===========");
        });

        socket.on("chatMsg", function (msg) {
            console.log("===========message: " + msg + " ===========");

            // socket.emit("chat message", msg);//这个只对自己的连接进行回复
            socketIO.emit('chatMsg', msg);//所有用户都回复
        });
    });
}
