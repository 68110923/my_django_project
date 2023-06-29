import {parse} from "@babel/parser";
import traverse from "@babel/traverse";
import generate from "@babel/generator";
import * as types from "@babel/types";
import fs from "fs";

// var file_list = ['code/source.js','code/1反控制流平坦化.js','code/2去除僵尸代码.js','code/3字符串还原.js','code/4表达式还原.js']
var file_list = ['code/source.js', '', '','code/3字符串还原.js','code/4表达式还原.js']

//--------------------------------反控制流平坦化----------------------------------
var source_name = ''   //等待解混淆的文件   
var save_file = ""      //解混淆存储到哪个文件
source_name = file_list[0]
save_file = file_list[1]
if (save_file != '') { //需要做当前的混淆
    source_name = file_list[0]
    console.log("源文件是---------" + source_name)
    console.log("存储文件是---------" + save_file)
    const code = fs.readFileSync(source_name, "utf-8");
    let ast = parse(code);
    traverse(ast, {
        //反控制流平坦化
        WhileStatement(path) {
            const {node, scope} = path;
            const {test, body} = node;
            let switchNode = body.body[0];
            let {discriminant, cases} = switchNode;
            let {object, property} = discriminant;
            let arrName = object.name;
            let binding = scope.getBinding(arrName);
            let {init} = binding.path.node;

            object = init.callee.object;
            property = init.callee.property;
            let argument = init.arguments[0].value;
            let arrayFlow = object.value[property.name](argument);

            // console.log(object.value[property.name])
            // console.log(argument)
            // console.log(arrayFlow)
            let resultBody = [];
            arrayFlow.forEach((index) => {
                let switchCase = cases.filter((c) => c.test.value == index)[0];
                let caseBody = switchCase.consequent;
                if (types.isContinueStatement(caseBody[caseBody.length - 1])) {
                    caseBody.pop();
                }
                resultBody = resultBody.concat(caseBody);
            });
            path.replaceWithMultiple(resultBody);
        },
    });
    const {code: output} = generate(ast);
    fs.writeFileSync(save_file, output, "utf-8");
    source_name = file_list[1]
}


//--------------------------------去除僵尸代码----------------------------------
save_file = file_list[2]
if (save_file != '') { //需要做当前的混淆
    console.log("源文件是---------" + source_name)
    console.log("存储文件是---------" + save_file)
    const code1 = fs.readFileSync(source_name, "utf-8");
    let ast1 = parse(code1);
    traverse(ast1, {
        IfStatement(path) {
            let result = path.get("test").evaluateTruthy(); //计算test路径下代码的结果是否为真  返回布尔值
            let consequent = path.get("consequent")
            let alternate = path.get("alternate")
            if (result === true) {
                if (consequent.isBlockStatement()) {
                    path.replaceWith(consequent.node)
                }
            } else if (result === false) {
                if (alternate.isBlockStatement()) {
                    path.replaceWith(alternate.node)
                }
            } else {
                // path.remove()   #未知结果的时候使用
            }
        },
    });
    const {code: output1} = generate(ast1);
    fs.writeFileSync(save_file, output1, "utf-8");
    source_name = file_list[2]
}


//--------------------------------字符串还原----------------------------------
save_file = file_list[3]
if (save_file != '') { //需要做当前的混淆
    console.log("源文件是---------" + source_name)
    console.log("存储文件是---------" + save_file)
    const code2 = fs.readFileSync(source_name, "utf-8");
    let ast2 = parse(code2);
    traverse(ast2, {
//     //此处的{ node } 写法就等价于 { node } = path  等价于 node = path.node
        StringLiteral(path) {
            //    /正则内容/gi.test(要匹配的字符串)    这个写法是JS中正则的写法，返回值是布尔值  详情可见https://www.runoob.com/jsref/jsref-obj-regexp.html
            // if (node.extra && /\\[ux]/gi.test(node.extra.raw)) {
            //     node.extra.raw = node.extra.rawValue;
            // }
            if (path.node.extra.raw !== path.node.extra.rawValue){
                delete path.node.extra
                // 以下方法均可
                // path.node.extra.raw = path.node.rawValue
                // path.node.extra.raw = '"' + path.node.value + '"'
                // delete path.node.extra
                //     delete path.node.extra.raw
            }
        },
        NumericLiteral(path) {
            if (path.node.extra.raw !== path.node.extra.rawValue){
                delete path.node.extra
            }
        },


    });
    const {code: output2} = generate(ast2);
    fs.writeFileSync("code/3字符串还原.js", output2, "utf-8");
    source_name = file_list[3]
}


//--------------------------------表达式还原----------------------------------
save_file = file_list[4]
if (save_file != '') { //需要做当前的混淆
    console.log("源文件是---------" + source_name)
    console.log("存储文件是---------" + save_file)
    const code3 = fs.readFileSync(source_name, "utf-8");
    let ast3 = parse(code3);
    traverse(ast3, {
        //下面对应的是一元表达式、二元表达式、条件表达式、调用表达式
        "UnaryExpression|BinaryExpression|ConditionalExpression|CallExpression": (
            path
        ) => {
            // if(path?.parentPath?.parentPath?.node?.kind === "const"){  //只筛选数据类型是常量的
                //执行path对应的语句，并将结果中的value属性赋值给value变量，将confident属性赋值给confident变量
                //confident 是可信度  value是计算结果
                const {confident, value} = path.evaluate();
                console.log(value)
                //如果表达式计算的结果是正负无穷大，则return不做任何处理
                if (value == Infinity || value == -Infinity) return;
                //如果结果可信，将结果转换为节点替换当前节点
                if (value == undefined)return;  //结果是未定义，就不管
                confident && path.replaceWith(types.valueToNode(value));
            // }


        },
    });
    const {code: output3} = generate(ast3);
    fs.writeFileSync("code/4表达式还原.js", output3, "utf-8");
    source_name = file_list[4]
}

// //     //在此之前，先了解下path和node
// //     /*
// //     path指的是路径  其常用的方法
// //     当前路径所对应的源代码 : path.toString
// //     判断path是什么type，使用path.isXXX 这个方法  : if(path.isStringLiteral()){}
// //     获取path的上一级路径 : let parent = path.parentPath;
// //     获取path的子路径 : path.get('test');
// //     删除path : path.remove()
// //     替换path（一个节点） : path.replaceWith({type:"NumericLiteral",value:3});
// //     替换path(多个节点) : path.replaceWithMultiple([{type:"NumericLiteral",value:3}]);
// //     插入path : path.insertAfter({type:"NumericLiteral",value:3});
// //
// //     node指的是节点  是path的一个属性 可以通过path.node来获取node  本质是一个json结果的数据
// //     获取原码 ：
// //         const generator = require("@babel/generator").default;
// //         let {code} = generator(node);
// //     删除节点 ： path.node.init = undefined;
// //     访问子节点的值（init节点的value属性） ： console.log(path.node.init.value);
// //     节点的类型判断 ： 先引入types  if(types.isBlockStatement(path.node)){}
// //
// //     path和node关系： node是path的一个属性
// //     举例： path.node.test === path.get("test").node  结果是True
// //      */
// //
