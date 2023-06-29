// hook大全：
// https://blog.csdn.net/qq_40558166/article/details/123525365

// cookie hook  1
(function (){
    var org = document.cookie.__lookupSetter__('cookie');
    document.__defineSetter__("cookie",function (cookie){
        if(cookie.indexOf("m")>-1){
            debugger;
        }
        org = cookie;
    });
    document.__defineGetter__("cookie",function (){return org;});
})();

// cookie hook  2
(function () {
  'use strict';
  var cookieTemp = '';
  Object.defineProperty(document, 'cookie', {
    set: function (val) {
      if (val.indexOf('m') != -1) {
        debugger;
      }
      console.log('Hook捕获到cookie设置->', val);
      cookieTemp = val;
      return val;
    },
    get: function () {
      return cookieTemp;
    },
  });
})();


// Hook Header  hook到Authorization下断点
(function () {
    var org = window.XMLHttpRequest.prototype.setRequestHeader;
    window.XMLHttpRequest.prototype.setRequestHeader = function (key, value) {
        if (key == 'Authorization') {
            debugger;
        }
        return org.apply(this, arguments);
    };
})();

//URL Hook     用于定位请求 URL 中关键参数生成位置，以下代码演示了当请求的 URL 里包含 login 关键字时，则插入断点：
(function () {
    var open = window.XMLHttpRequest.prototype.open;
    window.XMLHttpRequest.prototype.open = function (method, url, async) {
        if (url.indexOf("login") != -1) {
            debugger;
        }
        return open.apply(this, arguments);
    };
})();

//Hook  JSON.stringify() 方法用于将 JavaScript 值转换为 JSON 字符串，在某些站点的加密过程中可能会遇到，以下代码演示了遇到 JSON.stringify() 时，则插入断点：
(function() {
    var stringify = JSON.stringify;
    JSON.stringify = function(params) {
        console.log("Hook JSON.stringify ——> ", params);
        debugger;
        return stringify(params);
    }
})();

//hook  JSON.parse() 方法用于将一个 JSON 字符串转换为对象，在某些站点的加密过程中可能会遇到，以下代码演示了遇到 JSON.parse() 时，则插入断点：
(function() {
    var parse = JSON.parse;
    JSON.parse = function(params) {
        console.log("Hook JSON.parse ——> ", params);
        debugger;
        return parse(params);
    }
})();

//Hook eval   JavaScript eval() 函数的作用是计算 JavaScript 字符串，并把它作为脚本代码来执行。如果参数是一个表达式，eval() 函数将执行表达式。如果参数是 Javascript 语句，eval() 将执行 Javascript 语句，经常被用来动态执行 JS。以下代码执行后，之后所有的 eval() 操作都会在控制台打印输出将要执行的 JS 源码：
(function() {
    // 保存原始方法
    window.__cr_eval = window.eval;
    // 重写 eval
    var myeval = function(src) {
        console.log(src);
        console.log("=============== eval end ===============");
        debugger;
        return window.__cr_eval(src);
    }
    // 屏蔽 JS 中对原生函数 native 属性的检测
    var _myeval = myeval.bind(null);
    _myeval.toString = window.__cr_eval.toString;
    Object.defineProperty(window, 'eval', {
        value: _myeval
    });
})();

// Hook Function  以下代码执行后，所有的函数操作都会在控制台打印输出将要执行的 JS 源码：
(function() {
    // 保存原始方法
    window.__cr_fun = window.Function;
    // 重写 function
    var myfun = function() {
        var args = Array.prototype.slice.call(arguments, 0, -1).join(","),
            src = arguments[arguments.length - 1];
        console.log(src);
        console.log("=============== Function end ===============");
        debugger;
        return window.__cr_fun.apply(this, arguments);
    }
    // 屏蔽js中对原生函数native属性的检测
    myfun.toString = function() {
        return window.__cr_fun + ""
    }
    Object.defineProperty(window, 'Function', {
        value: myfun
    });
})();
