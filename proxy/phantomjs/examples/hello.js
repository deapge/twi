//console.log('Hello, world!');
//phantom.exit();

// Example using HTTP GET operation

var page = require('webpage').create(),
    system = require('system'),
    url;

if (system.args.length != 3) {
    console.log('Usage: get.js URL');
    console.log('GET 请求数据!');
    phantom.exit(1);
} else {
   url = system.args[1];
   page.open(url, function (status) {
     if (status !== 'success') {
        console.log('Unable to post!');
     } else {
        console.log(page.content);
     }
     phantom.exit();
   });
}

